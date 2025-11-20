#!/usr/bin/env bash

dd if=/dev/zero of=valid.img bs=1M count=20
parted -s --align optimal valid.img --script mklabel gpt
parted -s --align optimal valid.img --script mkpart primary ext4 0% 100%
sudo losetup -fP valid.img
LOOPDEV=$(losetup -j valid.img | cut -d: -f1)
PARTITION1="${LOOPDEV}p1"
sudo mkfs.ext4 $PARTITION1
sudo rm -rf /mnt/valid*
sudo mkdir /mnt/valid
sudo mount ${PARTITION1} /mnt/valid
sudo mkdir /mnt/valid/empty_dir
sudo umount /mnt/valid
sudo losetup -d ${LOOPDEV}
sudo rm -rf /mnt/valid* *.vmdk
qemu-img convert valid.img -O vmdk malicious.vmdk
