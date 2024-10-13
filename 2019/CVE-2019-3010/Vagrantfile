Vagrant.configure("2") do |config|
  config.vm.box = "FEBO/solaris-11.4"
  config.vm.box_version = "0.1"
  config.vbguest.auto_update = false
  config.vm.synced_folder ".", "/vagrant", disabled: true

  config.vm.provision "shell", inline: <<-SHELL
    pkg install solaris-desktop
    pkg install gcc-dev


    SHELL
end
