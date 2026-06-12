---
layout: default
title: Configuring the login node
---

> **Configure the login node first.** The compute node configuration (next page) depends on files
> generated here (munge key, slurm.conf, /etc/hosts), and the login node must be up and running
> as the DHCP/DNS server before the compute node can reach the network.

## Start with an update

```bash
sudo apt update -y
sudo apt upgrade -y
```

## Install required packages

```bash
sudo apt install -y nfs-kernel-server lmod ansible slurm munge nmap \
nfs-common net-tools build-essential htop net-tools screen vim python3-pip \
dnsmasq slurm-wlm iptables iptables-persistent libmunge-dev libmunge2 \
libpmix2 libpmix-bin libpmix-dev git
```

A dialog block will appear on the screen. Answer yes to both questions.

| Package.                          | Purpose                                                                    |
| --------------------------------- | -------------------------------------------------------------------------- |
| `nfs-kernel-server`               | NFS server — exports the shared filesystem to compute nodes                |
| `nfs-common`                      | NFS client utilities, also needed on the login node                        |
| `lmod`                            | Lua-based module system for managing software environments (e.g. ESSI)     |
| `ansible`                         | Automation tool for configuring compute nodes in bulk                      |
| `slurm-wlm`                       | Slurm workload manager — schedules and dispatches jobs across the cluster  |
| `munge`                           | Authentication service used by Slurm daemons to verify messages            |
| `libmunge2`, `libmunge-dev`       | MUNGE shared library and development headers                               |
| `libpmix2`, `libpmix-bin`, `libpmix-dev` | PMIx library for MPI job launch support                             |
| `dnsmasq`                         | Lightweight DHCP and DNS server — assigns IPs to compute nodes             |
| `iptables`, `iptables-persistent` | Firewall and NAT rules; persistent saves them across reboots               |
| `nmap`                            | Network scanner — useful for verifying compute nodes are reachable         |
| `net-tools`                       | Legacy networking tools (`ifconfig`, `netstat`, etc.)                      |
| `build-essential`                 | Compilers and build tools (`gcc`, `make`, etc.)                            |
| `htop`                            | Interactive process viewer                                                 |
| `screen`                          | Terminal multiplexer — keeps sessions alive over SSH                       |
| `vim`                             | Text editor                                                                |
| `python3-pip`                     | Python package installer                                                   |
| `git`                             | Version control                                                            |

## Enable IP forwarding

Create a drop-in configuration file so the system setting is not mixed with distribution defaults:

```bash
echo "net.ipv4.ip_forward=1" | sudo tee /etc/sysctl.d/99-ip-forward.conf
sudo sysctl --system
```

`sudo sysctl --system` applies all drop-in files immediately, so a reboot is not required.

## Configure IP-tables

```bash
sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
sudo iptables -A FORWARD -i wlan0 -o eth0 -j ACCEPT
sudo iptables -A FORWARD -i eth0 -o wlan0 -m state --state RELATED,ESTABLISHED -j ACCEPT
sudo netfilter-persistent save
```

## Configure the network interfaces

> **Warning:** Do **not** edit `/etc/network/interfaces` on current Raspberry Pi OS (Bookworm).
> That file is not used when NetworkManager is active, and mixing the two causes unpredictable
> behaviour. Use `nmcli` instead.

The login node needs a **fixed IP** on its ethernet interface (`eth0`) so the compute nodes
always reach it at the same address, and so dnsmasq can hand out leases reliably.
Ethernet interfaces must be set to "unmanaged" in the sense that they carry a static address
rather than requesting one via DHCP — NetworkManager still controls the interface, but DHCP
is disabled for it.

```bash
sudo nmcli con add type ethernet ifname eth0 con-name eth0-static \
  ipv4.method manual \
  ipv4.addresses 192.168.5.101/24 \
  ipv4.gateway 192.168.5.101 \
  ipv4.dns 192.168.5.101 \
  connection.autoconnect yes
sudo nmcli con up eth0-static
```

Verify the address is set:

```bash
ip addr show eth0
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

- Configure dnsmasq by entering the following in the file `/etc/dnsmasq.conf`. Replace
the MAC address on the sixth line with the MAC address of your compute node.

```bash
interface=eth0
bind-dynamic
domain-needed
bogus-priv
dhcp-range=192.168.5.102,192.168.5.200,255.255.255.0,12h
dhcp-host=ab:cd:12:34:ab:cd,192.168.5.102
dhcp-option=3,192.168.0.1 # default route

```

## Create a shared directory

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
127.0.0.1 localhost
::1       localhost ip6-localhost ip6-loopback
ff02::1   ip6-allnodes
ff02::2   ip6-allrouters

# This login node's hostname
127.0.1.1 pixie001

# IP and hostname of compute nodes
192.168.5.102 pixie002
```

## Configure Slurm

Add the following to /etc/slurm/slurm.conf. Change all occurences of `pixie` in this script to the name of your cluster.

```conf
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
SelectType=select/cons_tres
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

source /cvmfs/software.eessi.io/versions/2023.06/init/lmod/bash
# We don't do this one anymore:
# echo "source /cvmfs/software.eessi.io/versions/2023.06/init/bash" | sudo tee -a /etc/profile
```

## Disable WiFi and Bluetooth

Now that we have set our login node up as a DHCP server, we can disable WiFi.

Open `/boot/firmware/config.txt` and add the following two lines at the bottom in the `[all]` section.

```ini
dtoverlay=disable-wifi
dtoverlay=disable-bt
```

Save the file and reboot.
