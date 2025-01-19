---
layout: default
title: Preparing compute nodes for eessi
---

Credit to: https://linuxconfig.org/how-to-create-loop-devices-on-linux

To use `eessi` on diskless compute nodes, we need to create "pseudo" disk using 
- `dd` for creating an empty file, the size of the disk we need.
- `losetup`
- `parted`
- `mkfs.ext4`
- `mount`

### Create file 

`dd if=/dev/zero of=loopdevice bs=1M count=32768`

### Map the file to a block device

- `sudo losetup -f` # determine the next available block device
- `sudo losetup -f loopdevice` # map the file called loopdevice to the next available block device

### Create a partition and filesystem

- `sudo parted -s /dev/loop0 mklabel msdos`
- `sudo parted -s /dev/loop0 mkpart primary 0% 100%`
- `sudo mkfs.ext4 /dev/loop0p1 

### Mount the file as a drive

- `sudo mount /dev/loop0 /cvmfs`


