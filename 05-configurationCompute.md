---
title: Configuring a compute node
layout: default
---

This is a step by step guide on how to set up a miniHPC using Raspberry Pis.

Flash an SD card as described in episode 2 and give it a name of <`nodename`>02 where <`nodename`> is the
name that you use for all your nodes in your HPC (e.g. `orange`, `black`, `green`, `blue`, `yellow`).

## Configure the hostname and hosts file

> **Do this first.** Hostname resolution must be in place before running any `sudo` command,
> otherwise every `sudo` invocation will print `unable to resolve host node001`. Copy `/etc/hosts`
> from the login node before proceeding.

- Copy `/etc/hosts` from the login node to `/etc/hosts` on the compute node

## Install required packages

```bash
sudo apt-get install -y slurmd slurm-client munge vim ntpsec ntpsec-ntpdate lmod
```

> **Note:** `ntp` and `ntpdate` are no longer available on current Raspberry Pi OS. Use `ntpsec`
> and `ntpsec-ntpdate` instead; they provide the same functionality.

| Package | Purpose |
| --- | --- |
| `slurmd` | Slurm compute node daemon — executes jobs dispatched by the login node |
| `slurm-client` | Slurm client tools (`srun`, `sbatch`, `squeue`, etc.) |
| `munge` | Authentication service used by Slurm to verify inter-node messages |
| `ntpsec` | NTP time synchronisation daemon — keeps node clocks in sync with the login node |
| `ntpsec-ntpdate` | One-shot time sync command, useful for initial clock correction on first boot |
| `lmod` | Lua-based module system for loading software environments (e.g. ESSI) |
| `vim` | Text editor |

Verify that `slurmd` installed and the service unit is present:

```bash
systemctl status slurmd
```

If `slurmd` is not found, the package may have been silently skipped during install. Run the
install command again with only `slurmd` to confirm:

```bash
sudo apt-get install -y slurmd
```

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

```bash
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

## Disable WiFi and Bluetooth

Open `/boot/firmware/config.txt` and add the following two lines at the bottom in the `[all]` section.

```ini
dtoverlay=disable-wifi
dtoverlay=disable-bt
```

Save the file and reboot
