---
layout: default
title: Some extra things that can be done
---

## Making an image of the compute node OS

- On a Linux laptop (or with a USB SD card reader) take an image of this:

```bash
dd if=/dev/mmcblk0 of=node.img
```

- Copy node.img to the master Raspberry Pi's home directory.


## Setup PXE booting

Download the pxe-boot scripts:

```bash
git clone https://github.com/carpentriesoffline/pxe-boot.git
cd pxe-boot
./pxe-install
```

Initalise a PXE node:
```
./pxe-add <serial number> ../node.img <IP address>  <node name> <mac address>
```

for example:
```
./pxe-add fa917c3a ../node.img 192.168.5.105 pixie002 dc:a6:32:af:83:d0
```

This will create an entry with the serial number in /pxe-boot and /pxe-root. 

- Copy the Slurm config to the node filesystems

```bash
cp /etc/slurm/slurm.conf /pxe-root/*/etc/slurm/
````
 

## Test PXE booting
* Boot up a client
* Run sinfo to see if the cluster is working
You should see something like

```bash
PARTITION     AVAIL  TIMELIMIT  NODES  STATE NODELIST
pixiecluster*    up   infinite      5   idle pixie[002-006]
```

# Links:
- https://www.clearlinux.org/clear-linux-documentation/tutorials/hpc.html
- https://www.quantstart.com/articles/building-a-raspberry-pi-cluster-for-qstrader-using-slurm-part-3/
