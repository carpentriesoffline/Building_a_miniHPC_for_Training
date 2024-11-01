---
title: Configuration
layout: default
---

This is a step by step guide on how to set up a miniHPC using Raspberry Pis.

# 1. Hardware requirement 

# 2. Initial configuration
_TODO From https://github.com/carpentriesoffline/CarpentriesOffline.github.io/blob/main/rpiimage_step_by_step.md_

# Installing SLURM/HPC

## Setting up the miniHPC login node

- Login to the Pi
Use SSH or login with a local console if you have a monitor attached. Use the login details you used above to log into the Pi.

```bash
ssh <USERNAME>@<IP-ADDRESS>
```

In this example, the username would be `cw24`

- Do an update and a full-upgrade:

```bash
sudo apt update
sudo apt full-upgrade
```

- Install required dependencies.

```bash
sudo apt install -y nfs-kernel-server lmod ansible slurm munge nmap \
nfs-common net-tools build-essential htop net-tools screen vim python3-pip \
dnsmasq slurm-wlm iptables

sudo apt install -y iptables-persistent
```

A dialog block will appear on the screen. Answer yes to both questions.

##  Configure IP-tables
```bash
sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
sudo iptables -A FORWARD -i wlan0 -o eth0 -j ACCEPT
sudo iptables -A FORWARD -i eth0 -o wlan0 -m state --state RELATED,ESTABLISHED -j ACCEPT
sudo netfilter-persistent save
```


## Setup the Cluster network

Place the following into `/etc/network/interfaces`

```bash
auto eth0
allow-hotplug eth0
iface eth0 inet static
  address 192.168.5.101
  netmask 255.255.255.0
source /etc/network/interfaces.d/*
```

- Modify the hostname

```bash
echo pixie001 | sudo tee /etc/hostname
```

- Configure dhcp by entering the following in the file `/etc/dhcpd.conf`

```bash
interface eth0
static ip_address=192.168.5.101/24
static routers=192.168.5.101
static domain_name_servers=192.168.5.101
```

- Configure dnsmasq by entering the following in the file `/etc/dnsmasq.conf`

```bash
interface=eth0
bind-dynamic
domain-needed
bogus-priv
dhcp-range=192.168.5.102,192.168.5.200,255.255.255.0,12h
```

- Create a shared directory.

```bash
sudo mkdir /sharedfs
sudo chown nobody:nogroup -R /sharedfs
sudo chmod 777 -R /sharedfs
```

- Configure shared drives by adding the following at the end of the file `/etc/exports`

```bash
/sharedfs    192.168.5.0/24(rw,sync,no_root_squash,no_subtree_check)
```

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

- Configure Slurm

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

- Install ESSI

```bash
mkdir essi
cd essi
wget https://raw.githubusercontent.com/EESSI/eessi-demo/main/scripts/install_cvmfs_eessi.sh
sudo bash ./install_cvmfs_eessi.sh
echo "source /cvmfs/software.eessi.io/versions/2023.06/init/bash" | sudo tee -a /etc/profile
```

### Configure munge

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



## Setting up a compute node

Flash another SD card for a Raspberry Pi. Boot it up with internet access and run the following:

```bash
sudo apt-get install -y slurmd slurm-client munge vim ntp ntpdate
```

- Copy the `/etc/hosts` from the login node to the compute node
- Copy the slurm config of the login node to `/etc/slurm/slurm.conf`
- Copy the `/etc/munge/munge.key` from the login node to the compute node

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
