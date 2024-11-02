---
title: Configuring a compute node
layout: default
---

This is a step by step guide on how to set up a miniHPC using Raspberry Pis.

## Install required packages

Flash another SD card for a Raspberry Pi. Boot it up with internet access and run the following:

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


