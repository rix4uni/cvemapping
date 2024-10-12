# sudo apt update
# sudo apt install build-essential libncurses-dev bison flex libssl-dev libelf-dev bc
# sudo apt install git qemu-system-x86

git clone https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git
cd linux
git checkout v6.4

make defconfig

# debug info
scripts/config --enable CONFIG_DEBUG_INFO_DWARF4
scripts/config --enable CONFIG_DEBUG_INFO_DWARF5

# User Namespace
scripts/config --enable CONFIG_USER_NS

make -j$(nproc)

# cp linux/arch/x86/boot/bzImage .
# cp linux//vmlinux .
