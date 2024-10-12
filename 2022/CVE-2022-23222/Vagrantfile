# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/focal64"
  config.vm.provision "shell", inline: <<-SHELL

    apt-get update
    apt install -y linux-image-5.13.0-27-generic libbpf-dev make build-essential
    cd /home/vagrant && git clone https://github.com/PenteraIO/CVE-2022-23222-POC.git
    cd CVE-2022-23222-POC && make
    mv ./exploit /home/vagrant/
    chown vagrant:vagrant /home/vagrant/exploit
    chmod +x /home/vagrant/exploit

    echo "@reboot echo 0 > /proc/sys/kernel/unprivileged_bpf_disabled" > ourcrontab
    crontab ourcrontab
    rm ourcrontab

    reboot -h now

  SHELL
end
