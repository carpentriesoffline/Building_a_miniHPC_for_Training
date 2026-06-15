---
layout: default
title: Configuring the login node
---

> **Configure the login node first.** The compute node configuration (next
> page) depends on files generated here (munge key, slurm.conf, /etc/hosts),
> and the login node must be up and running as the DHCP/DNS server before the
> compute node can reach the network.

> **Tip:** We won't configure a separate control node in this tutorial: the
> login node will act as the SLURM controller, the NFS backing filesystem, and
> the cluster's internet gateway, too. In a production cluster these would
> typically be separate machines, but combining them means we can demonstrate
> all the techniques using just two nodes. We'll also leave multi-user systems
> and authentication (Kerberos, LDAP and friends) as an exercise to the reader.

In this section, we will configure our login node. This is the node through
which we will interface with our cluster.

## Start with an update

```bash
sudo apt update
sudo apt upgrade -y
```

## Install required packages

This command will install the required packages (and some suggested ones we like
to have on hand) onto your Pi:

```bash
sudo apt-get install -y nfs-kernel-server nfs-common slurm slurm-wlm munge \  
  libmunge-dev libmunge2 iptables iptables-persistent dnsmasq libopenmpi-dev \
  libopenmpi3t64 lmod build-essential python3-pip net-tools bind9-dnsutils \
  ansible nmap git htop screen vim 
```

A dialog block will appear on the screen. Answer yes to both questions.

> **Note:** On older Raspberry Pi OS releases, `libpmix2`, `libpmix-bin`, and
> `libpmix-dev` were separate packages. PMIx packages were merged into OpenMPI
> in Debian Bookworm: use `libopenmpi3t64` and `libopenmpi-dev` instead.

| Package                           | Purpose                                                                  |
| --------------------------------- | ------------------------------------------------------------------------ |
| `nfs-kernel-server`               | NFS server: exports the shared filesystem to compute nodes               |
| `nfs-common`                      | NFS client utilities, also needed on the login node                      |
| `slurm` `slurm-wlm`               | Slurm workload manager: schedules and dispatches jobs across the cluster |
| `munge`                           | Authentication service used by Slurm daemons to verify messages          |
| `libmunge2` `libmunge-dev`        | MUNGE shared library and development headers                             |
| `iptables` `iptables-persistent`  | Firewall and NAT rules: persistent saves them across reboots             |
| `dnsmasq`                         | Lightweight DHCP and DNS server: assigns IPs to compute nodes            |
| `libopenmpi-dev` `libopenmpi3t64` | OpenMPI runtime and headers: provides PMIx support for Slurm job launch  |
| `python3-pip`                     | Python package installer                                                 |
| `lmod`                            | Lua-based module system for managing software environments (e.g. EESSI)  |
| `build-essential`                 | Compilers and build tools (`gcc`, `make`, etc.)                          |
| `net-tools`                       | Legacy networking tools (`ifconfig`, `netstat`, etc.)                    |
| `bind9-dnsutils`                  | DNS utilities (`dig`, `nslookup`): useful for verifying DNS resolution   |
| `ansible`                         | Automation tool for configuring compute nodes in bulk                    |
| `nmap`                            | Network scanner: useful for verifying compute nodes are reachable        |
| `git`                             | Version control                                                          |
| `htop`                            | Interactive process viewer                                               |
| `screen`                          | Terminal multiplexer: keeps sessions alive over SSH                      |
| `vim`                             | Text editor                                                              |

Now, we can remove any redundant packages left over after our upgrades and package installations:

```bash
sudo apt-get -y autoremove
```

> **Note:** This stage can take quite a long time on older hardware (Pi 2Bs or Pi 3s, for instance).
> The hardware in the workshop uses Raspberry Pi 5s, so shouldn't keep you waiting too long.

## Set up cluster networking

Compute clusters are usually set up so that users cannot access compute nodes
directly from the public internet. We'll do that too. Our login node's WiFi
connection will be used as the gateway to the world, and we'll later disable
WiFi on our compute nodes. This means that our login node is also acting as a
router / internet gateway for the purposes of our tutorial. 

> **Tip:** We don't have to use `wlan0` for this: we could connect a USB
> Ethernet dongle and use `eth1` as our upstream link instead. In any case, the
> concept to demonstrate here is that our compute nodes are physically isolated
> from HPC users at a network level.

### Enable IP forwarding

By default, Linux drops packets that arrive on one interface but are destined
for another network. Enabling IP forwarding tells the kernel to route those
packets instead of discarding them.

Create a drop-in configuration file so the system setting is not mixed with distribution defaults:

```bash
echo "net.ipv4.ip_forward=1" | sudo tee /etc/sysctl.d/99-ip-forward.conf
sudo sysctl --system
```

`sudo sysctl --system` applies all drop-in files immediately, so a reboot is not required.

### Configure IP-tables

We will configure NAT masquerading to control the network topology of our cluster.

```bash
sudo iptables -t nat -A POSTROUTING -o wlan0 -j MASQUERADE
sudo iptables -A FORWARD -i eth0 -o wlan0 -j ACCEPT
sudo iptables -A FORWARD -i wlan0 -o eth0 -m state --state RELATED,ESTABLISHED -j ACCEPT
sudo netfilter-persistent save
```

Here's what each rule does:

`sudo iptables -t nat -A POSTROUTING -o wlan0 -j MASQUERADE`  
This is NAT masquerading. Packets leaving via `wlan0` (the upstream internet
interface) have their source IP rewritten to the login node's `wlan0` address.
This lets compute nodes reach the internet via `eth0` on the login node: their
traffic appears to come from the login node.

`sudo iptables -A FORWARD -i eth0 -o wlan0 -j ACCEPT`  
Allows packets to be forwarded from `eth0` (the cluster network) out to `wlan0`
(internet). Without this, the kernel would drop traffic trying to cross
interfaces even if IP forwarding is enabled in sysctl.

`sudo iptables -A FORWARD -i wlan0 -o eth0 -m state --state RELATED,ESTABLISHED -j ACCEPT`  
The return-traffic rule. Allows packets coming back from the internet (`wlan0`)
into the cluster (`eth0`), but only for connections that were already
established or are related to an existing connection (e.g. FTP data channels).
New inbound connections from the internet are dropped.

Together, these three rules implement a basic NAT gateway: compute nodes can
reach the internet through the login node, but the internet cannot initiate
connections into the cluster.

## Configure the network interfaces

> **Warning:** Do **not** edit `/etc/network/interfaces` on current Raspberry
> Pi OS (Bookworm).  That file is not used when NetworkManager is active, and
> mixing the two causes unpredictable behaviour. Use `nmcli` instead.

The login node needs a **fixed IP** on its ethernet interface (`eth0`) so the
compute nodes always reach it at the same address, and so dnsmasq can hand out
leases reliably.  Ethernet interfaces must be set to "unmanaged" in the sense
that they carry a static address rather than requesting one via DHCP:
NetworkManager still controls the interface, but DHCP is disabled for it.

```bash
sudo nmcli con add type ethernet ifname eth0 con-name eth0-static \
  ipv4.method manual \
  ipv4.addresses 192.168.5.101/24 \
  ipv4.dns 192.168.5.101 \
  connection.autoconnect yes
sudo nmcli con up eth0-static
```

> **Note:** Need to reverse this for any reason? `sudo nmcli con delete
> eth0-static` removes the static connection and returns eth0 to DHCP.

> **Warning:** Previous versions of this tutorial used `eth0` as the gateway
> interface, routing outgoing traffic back over `192.168.5.101`. This has been
> updated to use `wlan0` so that the cluster network can reach the
> internet. As such, we don't set an `ipv4.gateway` on this connection.

Verify the address is set:

```bash
ip addr show
```

You should see a static address of `192.168.5.101` assigned to `eth0`. Your SSH
connection to the Pi is running through `wlan0` at this point:

![`ip addr show` showing static IP assignment and WiFi connection](fig/static-ip.png)

## How to modify the hostname (*if required!*)

If you followed section 2 correctly, your hostname will already be set. However,
if you need to modify it for any reason, you can do so with the following command:

```bash
echo pixie01 | sudo tee /etc/hostname
```

> **Warning:** This hostname **must** match the value used in the config files below,
> particularly `/etc/hosts` and `/etc/slurm/slurm.conf`. Take extra care when editing these
> files that they match the values for your login and compute node hostnames.

## Configure DHCP

Configure dhcp by entering the following in the file `/etc/dhcpd.conf`

```bash
interface eth0
static ip_address=192.168.5.101/24
static routers=192.168.5.101
static domain_name_servers=192.168.5.101
```

> _Tip:_ You can populate the files in this section however you'd like. However,
> one of the easier patterns is using heredocs with `sudo tee filename`, e.g.:
>
> ```bash
> sudo tee /etc/somefile.conf <<EOF
>   <paste your lines here, then type "EOF" to end>
> EOF
> ```

## Configure DNS masquerading

First, retrieve the ethernet MAC address of your compute node. If it is already on
the network over WiFi, you can do this from the login node, or from your laptop:

```bash
ssh node02.local "ip link show eth0"
```

Look for the `link/ether` line: the MAC address is the six colon-separated hex pairs,
e.g. `b8:27:eb:6e:7d:6d`.

Now configure dnsmasq by entering the following in `/etc/dnsmasq.conf`, substituting
your compute node's MAC address into the `dhcp-host` line:

```bash
interface=eth0
bind-dynamic
domain-needed
bogus-priv

dhcp-range=192.168.5.102,192.168.5.200,255.255.255.0,12h
dhcp-option=3,192.168.5.101 # default route (the login node)
dhcp-option=6,192.168.5.101 # DNS server

dhcp-host=b8:27:eb:6e:7d:6d,192.168.5.102 # compute node assignment
```

> **Warning:** Don't copy-and-paste this block without altering it to match
> your MAC address!

> **Note:** If you add more compute nodes, add one `dhcp-host` line per node,
> incrementing the IP each time:
>
> ```bash
> dhcp-host=<mac-of-node02>,192.168.5.102
> dhcp-host=<mac-of-node03>,192.168.5.103
> ```
>
> You'll also need a matching host entry in `/etc/cloud/templates/hosts.debian.tmpl` for each node.

Restart dnsmasq to apply the config:

```bash
sudo systemctl restart dnsmasq
```

Verify it is now listening on the DHCP port:

```bash
sudo ss -ulnp | grep :67
```

You should see `dnsmasq` bound to port 67.

## Configure NFS

Next we want to configure some shared filesystem space that all nodes can access.

First we'll create a shared directory on our login node, which here is acting
as our backing filestore. This would be a separate filesystem server in 
reality, using an HPC-class filesystem like [Lustre](https://www.lustre.org/).

```bash
sudo mkdir /sharedfs
sudo chown nobody:nogroup -R /sharedfs
sudo chmod 777 -R /sharedfs
```

Configure shared drives by adding the following at the end of the file `/etc/exports`

```bash
/sharedfs    192.168.5.0/24(rw,sync,no_root_squash,no_subtree_check)
/home        192.168.5.0/24(rw,sync,no_root_squash,no_subtree_check)
```

Then apply the exports:

```bash
sudo exportfs -ra
sudo exportfs -v
```

You should see both `/sharedfs` and `/home` listed. We don't need to restart the
NFS service here.

## Configure hosts file

> **Warning:** On current Debian (Bookworm and later), cloud-init manages
> `/etc/hosts` and will overwrite direct edits on reboot. Edit the template
> instead: `/etc/cloud/templates/hosts.debian.tmpl`.

`dnsmasq` reads the login node's `/etc/hosts` and serves those entries as DNS
to all cluster nodes, so this is the only place you need to maintain
hostname-to-IP mappings for the cluster. Compute nodes will receive the login
node's address as their DNS server via DHCP.

The template already contains entries to create this node's hostname.  Append
the cluster IP entries below it. Add the following to
`/etc/cloud/templates/hosts.debian.tmpl`, substituting your cluster name:

```bash
# Cluster nodes
192.168.5.101 pixie01
192.168.5.102 pixie02
```

> **Warning:** Don't copy-and-paste this block without altering it to match
> your cluster name! (`orange`, `black`, `green`, etc.).

Now we can apply the template to `/etc/hosts` immediately, then reload
dnsmasq so it picks up the new entries:

```bash
sudo cloud-init single --name update_etc_hosts
sudo systemctl reload dnsmasq
```

## Configure munge

Munge is the authentication service we'll be using in our Pi HPC cluster. We
need to do some configuration here first.

Create the munge key using the `mungekey` tool, which handles size and permissions correctly:

```bash
sudo mungekey --create
```

Verify ownership and permissions:

```bash
sudo ls -la /etc/munge/munge.key
```

## Configure Slurm

Add the following to `/etc/slurm/slurm.conf`. Again, **change all occurences of 
`pixie` in this script to the name of your cluster.** We use a two-digit
node identifier here (`pixieNN`) for simplicity but SLURM can easily be 
configured to use more. 

```conf
SlurmctldHost=pixie01(192.168.5.101)
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
PartitionName=pixiecluster Nodes=pixie[02-02] Default=YES MaxTime=INFINITE State=UP
RebootProgram=/etc/slurm/slurmreboot.sh
NodeName=pixie01 NodeAddr=192.168.5.101 CPUs=4 State=IDLE
NodeName=pixie02 NodeAddr=192.168.5.102 CPUs=4 State=IDLE
```

> **Warning:** You're starting to get used to this warning, but please,
> don't copy-and-paste this block without altering it to match your hostname!

> **Tip:** If you're trying this at home with a mixed bag of hardware, bear in
> mind that only Pi 3 and later run a 64-bit OS. Pi 1Bs (ARMv6) and most Pi
> 2Bs (ARMv7) are 32-bit and can run `slurmd` but can't use EESSI. Slurm has
> features to work around this: `NodeName` entries accept a `Feature=` tag
> (e.g. `Feature=64bit`). Jobs can then request specific node types with
> `--constraint=64bit`, ensuring they are routed to capable nodes.

Next, restart slurm:

```bash
sudo systemctl restart munge
sudo systemctl restart slurmctld
sudo systemctl restart slurmd
```

> **Note:** `slurmd` must be restarted after the config is in place. It is 
> installed earlier but will be in a failed state until now. Munge must be 
> started first as both daemons depend on it.

At this point, you should see Slurm running if you check using `sudo systemctl status slurmctld`:

![Slurm running on the login node](fig/slurm-running.png)

## Install EESSI

```bash
mkdir eessi
cd eessi
wget https://raw.githubusercontent.com/EESSI/eessi-demo/main/scripts/install_cvmfs_eessi.sh
sudo bash ./install_cvmfs_eessi.sh

source /cvmfs/software.eessi.io/versions/2023.06/init/lmod/bash
```

> **Note:** Only Pi 3 and later are supported by EESSI, as it needs a 64-bit OS.

## What we learned

We have now configured the login node from a fresh Raspberry Pi OS install
into a functioning HPC head node.

- Updated packages and installed the software stack needed to run a cluster
- Configured the login node as a NAT gateway, using iptables to allow compute
  nodes to reach the internet through `wlan0` while keeping them hidden from
  inbound connections
- Assigned a static IP (`192.168.5.101`) to `eth0` and configured dnsmasq to
  serve DHCP and DNS to compute nodes on the `192.168.5.0/24` subnet
- Exported a shared `/home` filesystem over NFS so compute nodes can access
  user files without copying them
- Configured munge so that Slurm daemons on the login and compute nodes can
  authenticate each other
- Installed and configured Slurm (`slurmctld`) to schedule jobs across the
  cluster
- Installed EESSI to provide a shared, architecture-aware software environment

In the next section, we'll configure a compute node to perform computational work.
