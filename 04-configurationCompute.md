---
title: Configuring a compute node
layout: default
---

This is a step by step guide on how to set up a miniHPC using Raspberry Pis.

Flash an SD card as described in episode 2 and give it a name of <<nodename>>002 where <<nodename>> is the
name that you use for all your nodes in your HPC.

Run and update and an upgrade
```bash
sudo apt update -y
sudo apt full-upgrade -y
```

## Disable WiFi and Bluetooth
Open `/boot/firmware/config.txt` and add the following two lines at the bottom in the `[all]` section.
```
dtoverlay=disable-wifi
dtoverlay=disable-bt
```
Save the file and reboot

## Create a mount point for the shared drive

```bash
sudo mkdir /sharedfs
```

## Install required packages

```bash
sudo apt-get install -y slurmd slurm-client munge vim ntp ntpdate lmod
```

- Copy the `/etc/hosts` from the login node to the compute node
- Copy the slurm config of the login node to `/etc/slurm/slurm.conf`
- Copy the `/etc/munge/munge.key` from the login node to the compute node
- Copy the /etc/cgroup.conf and /etc/cgroup_allowed_devices_file.conf from the login node to the compute node
- Update /etc/fstab to show the following:

```
proc            /proc           proc    defaults          0       0
PARTUUID=3e3e7392-01  /boot/firmware  vfat    defaults          0       2
PARTUUID=3e3e7392-02  /               ext4    defaults,noatime  0       1
192.168.5.101:/sharedfs    /sharedfs    nfs    defaults   0 0
192.168.5.101:/home    /home    nfs    defaults   0 0

```

## Install ESSI

```bash
mkdir essi
cd essi
wget https://raw.githubusercontent.com/EESSI/eessi-demo/main/scripts/install_cvmfs_eessi.sh
sudo bash ./install_cvmfs_eessi.sh

source /cvmfs/software.eessi.io/versions/2023.06/init/lmod/bash
# We don't do this one anymore:
# echo "source /cvmfs/software.eessi.io/versions/2023.06/init/bash" | sudo tee -a /etc/profile
```


