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
## Install required packages

```bash
sudo apt-get install -y slurmd slurm-client munge vim ntp ntpdate
```

- Copy the `/etc/hosts` from the login node to the compute node
- Copy the slurm config of the login node to `/etc/slurm/slurm.conf`
- Copy the `/etc/munge/munge.key` from the login node to the compute node

## Install ESSI

```bash
mkdir essi
cd essi
wget https://raw.githubusercontent.com/EESSI/eessi-demo/main/scripts/install_cvmfs_eessi.sh
sudo bash ./install_cvmfs_eessi.sh
echo "source /cvmfs/software.eessi.io/versions/2023.06/init/bash" | sudo tee -a /etc/profile
```


