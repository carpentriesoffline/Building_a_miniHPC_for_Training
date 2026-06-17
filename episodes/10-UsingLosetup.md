---
title: Preparing compute nodes for eessi
---

:::questions
- What is a loop device and when is it needed?
- How do you create persistent storage for a diskless compute node?
:::

:::objectives
- Create a large file with `dd` to act as a virtual disk
- Map the file to a loop device using `losetup`
- Partition and format the loop device
- Mount the loop device for use by EESSI
:::

Credit to: <https://linuxconfig.org/how-to-create-loop-devices-on-linux>

To use `eessi` on diskless compute nodes, we need to create "pseudo" disk using

- `dd` for creating an empty file, the size of the disk we need.
- `losetup`
- `parted`
- `mkfs.ext4`
- `mount`

## Create file

`dd if=/dev/zero of=loopdevice bs=1M count=32768`

## Map the file to a block device

Determine the next available block device:  
: `sudo losetup -f`  
Map the file called `loopdevice` to the next available block device:  
: `sudo losetup -f loopdevice`  

## Create a partition and filesystem

- `sudo parted -s /dev/loop0 mklabel msdos`
- `sudo parted -s /dev/loop0 mkpart primary 0% 100%`
- `sudo mkfs.ext4 /dev/loop0p1`

## Mount the file as a drive

- `sudo mount /dev/loop0 /cvmfs`

:::keypoints
- Loop devices map regular files to block devices, allowing them to be partitioned and mounted like physical disks
- This provides EESSI with a mountable filesystem at `/cvmfs` on diskless compute nodes
:::
