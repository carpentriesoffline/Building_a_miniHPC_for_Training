---
layout: default
title: Configuring the login node
---

## Install required packages.

```bash
sudo apt install -y nfs-kernel-server lmod ansible slurm munge nmap \
nfs-common net-tools build-essential htop net-tools screen vim python3-pip \
dnsmasq slurm-wlm iptables iptables-persistent
```

A dialog block will appear on the screen. Answer yes to both questions.

##  Configure IP-tables
```bash
sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
sudo iptables -A FORWARD -i wlan0 -o eth0 -j ACCEPT
sudo iptables -A FORWARD -i eth0 -o wlan0 -m state --state RELATED,ESTABLISHED -j ACCEPT
sudo netfilter-persistent save
```

## Configure the network interfaces

Place the following into `/etc/network/interfaces`

```bash
auto eth0
allow-hotplug eth0
iface eth0 inet static
  address 192.168.5.101
  netmask 255.255.255.0
source /etc/network/interfaces.d/*
```

## Modify the hostname

```bash
echo pixie001 | sudo tee /etc/hostname
```

## Configure DHCP

- Configure dhcp by entering the following in the file `/etc/dhcpd.conf`

```bash
interface eth0
static ip_address=192.168.5.101/24
static routers=192.168.5.101
static domain_name_servers=192.168.5.101
```

## Configure DNS masquerading

- Configure dnsmasq by entering the following in the file `/etc/dnsmasq.conf`

```bash
interface=eth0
bind-dynamic
domain-needed
bogus-priv
dhcp-range=192.168.5.102,192.168.5.200,255.255.255.0,12h
```

##  Create a shared directory.

```bash
sudo mkdir /sharedfs
sudo chown nobody:nogroup -R /sharedfs
sudo chmod 777 -R /sharedfs
```

## Configure NFS

- Configure shared drives by adding the following at the end of the file `/etc/exports`

```bash
/sharedfs    192.168.5.0/24(rw,sync,no_root_squash,no_subtree_check)
```

## Configure hosts

- The `/etc/hosts` file should contain the following. Make sure to change all occurences of `pixie` in the script to the name of your cluster:

```bash
127.0.0.1	localhost
::1		localhost ip6-localhost ip6-loopback
ff02::1		ip6-allnodes
ff02::2		ip6-allrouters

# This login node's hostname
127.0.1.1	pixie001

# IP and hostname of compute nodes
192.168.5.102	pixie002
```

## Configure Slurm

Add the following to /etc/slurm/slurm.conf. Change all occurences of `pixie` in this script to the name of your cluster.

```
SlurmctldHost=pixie001(192.168.5.101)
MpiDefault=none
ProctrackType=proctrack/cgroup
#ProctrackType=proctrack/linuxproc
ReturnToService=1
SlurmctldPidFile=/run/slurmctld.pid
SlurmctldPort=6817
SlurmdPidFile=/run/slurmd.pid
SlurmdPort=6818
SlurmdSpoolDir=/var/lib/slurm/slurmd
SlurmUser=slurm
StateSaveLocation=/var/lib/slurm/slurmctld
SwitchType=switch/none
TaskPlugin=task/affinity
InactiveLimit=0
KillWait=30
MinJobAge=300
SlurmctldTimeout=120
SlurmdTimeout=300
Waittime=0
SchedulerType=sched/backfill
SelectType=select/cons_res
SelectTypeParameters=CR_Core
AccountingStorageType=accounting_storage/none
# AccountingStoreJobComment=YES
AccountingStoreFlags=job_comment
ClusterName=pixie
JobCompType=jobcomp/none
JobAcctGatherFrequency=30
JobAcctGatherType=jobacct_gather/none
SlurmctldDebug=info
SlurmctldLogFile=/var/log/slurm/slurmctld.log
SlurmdDebug=info
SlurmdLogFile=/var/log/slurm/slurmd.log
PartitionName=pixiecluster Nodes=pixie[002-002] Default=YES MaxTime=INFINITE State=UP
RebootProgram=/etc/slurm/slurmreboot.sh
NodeName=pixie001 NodeAddr=192.168.5.101 CPUs=4 State=IDLE
NodeName=pixie002 NodeAddr=192.168.5.102 CPUs=4 State=IDLE
```

- Restart slurm

```bash
sudo systemctl restart slurmctld
```

## Configure munge

- Create munge key
  
```bash
sudo mkdir /etc/munge
dd if=/dev/urandom bs=1 count=1024 | sudo tee -a /etc/munge/munge.key
```

- Set ownership

 ```bash
sudo chown munge: /etc/munge/munge.key
sudo chmod 400 /etc/munge/munge.key
```

## Install ESSI

```bash
mkdir essi
cd essi
wget https://raw.githubusercontent.com/EESSI/eessi-demo/main/scripts/install_cvmfs_eessi.sh
sudo bash ./install_cvmfs_eessi.sh
echo "source /cvmfs/software.eessi.io/versions/2023.06/init/bash" | sudo tee -a /etc/profile
```



