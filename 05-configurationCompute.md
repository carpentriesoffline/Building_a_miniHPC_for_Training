---
title: Configuring a compute node
layout: default
---

This section demonstrates how to set up a compute node on your Raspberry Pi,
and add it to your cluster.

Flash an SD card as described in episode 2 and give it a name of `node02` where
`node` is the name that you use for all your nodes in your HPC (e.g. `orange`,
`black`, `green`, `blue`, `yellow`).

## Check the hostname (and fix if required)

> **Do this first.** Hostname resolution must be in place before running any
> `sudo` command, otherwise every `sudo` invocation will print `unable to
> resolve host node02`.

Back in section 3, we configured the hostname for the node in the imaging tool.
It's worth checking the hostname is set correctly: it should end `02`.

```bash
hostname
```

If you wrote the same image to SD card without customising the hostname, it
will be `node01`, which will conflict. If you need to modify it, run:

```bash
echo pixie02 | sudo tee /etc/hostname
```

No changes to `/etc/hosts` are needed on the compute node. Cluster-wide
hostname resolution (all nodes resolving each other by name) is provided by
dnsmasq on the login node and delivered to compute nodes via DHCP. The
hostname for the compute node is all that is needed locally.

> **Tip:** You can confirm the login node has seen this compute node and issued
> it a DHCP lease by running the following **on the login node**:
>
> ```bash
> cat /var/lib/misc/dnsmasq.leases
> ```
>
> Each line is an active lease: expiry timestamp, MAC address, assigned IP,
> hostname, and client ID. Your compute node should appear with the IP you
> reserved for it in `/etc/dnsmasq.conf` by setting a `dhcp-host` line with
> the MAC address for the compute node.
>
> This is also a useful way to check IP addresses assigned to cluster nodes
> if they aren't ending up where you expected, and you can even edit the file
> and delete lines to clear DHCP leases for clients if they have the wrong IP
> address (for example, if their MAC address wasn't added to `/etc/dnsmasq.conf`
> on the login node).

## Start with an update

We need to update packages on the compute nodes, too:

```bash
sudo apt-get update
sudo apt upgrade -y
```

> **Note:** During initial setup, while both `wlan0` and `eth0` are connected,
> your Pi can get confused about which interface to use for internet traffic.
> If packages aren't downloading, give `wlan0` a higher interface priority.
> Grab the device name from `nmcli`:
>
> ```bash
> pi@node02:~ $ nmcli con show
> NAME                              UUID                                  TYPE      DEVICE
> netplan-wlan0-CarpentriesOffline  e5799f3d-8920-3080-b93f-e6e5ac4ce778  wifi      wlan0
> netplan-eth0                      75a1216a-9d1a-30cd-8aca-ace5526ec021  ethernet  eth0
> lo                                c4c925ab-c23d-4a84-86f3-bb9133a05b92  loopback  lo
> ```
>
> Then give `wlan0` a higher interface metric:
>
> ```bash
> sudo nmcli con mod netplan-wlan0-CarpentriesOffline ipv4.route-metric 100
> sudo nmcli con down netplan-wlan0-CarpentriesOffline && sudo nmcli con up netplan-wlan0-CarpentriesOffline
> ```
>
> Once `wlan0` is disabled at the end of this tutorial, the compute node routes
> all traffic through `eth0` to the login node, which provides internet access
> via its own `wlan0`.

## Install required packages

```bash
sudo apt-get install -y slurmd slurm-client munge vim ntpsec ntpsec-ntpdate lmod nfs-common
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
| `nfs-common` | NFS client utilities — required to mount the shared filesystem from the login node |
| `vim` | Text editor |

Verify that `slurmd` installed and the service unit is present:

```bash
systemctl status slurmd
```

`systemctl` should show that Slurm is installed, but not configured yet. This
is OK for now! We haven't configured it yet, so it will be in a failure state:

![`systemctl` shows that Slurm is installed, but not configured
yet](fig/slurm-fail.png)

If `slurmd` is not found, the package may have been silently skipped during
install. Run the install command again with only `slurmd` to confirm:

```bash
sudo apt-get install -y slurmd
```

## Create a mount point for the shared drive

```bash
sudo mkdir /sharedfs
```

## Copy configuration files from the login node

- Copy the slurm config of the login node to `/etc/slurm/slurm.conf`
  - _On login node:_ `scp /etc/slurm/slurm.conf pi@node02.local:slurm.conf`
  - _On compute node:_ `sudo mv slurm.conf /etc/slurm/slurm.conf`
- Copy `/etc/munge/munge.key` from the login node to the compute node
  - _On login node:_ `scp /etc/munge/munge.key pi@node02.local:munge.key`
  - _On compute node:_
    - `sudo mv munge.key /etc/munge/munge.key`
    - `sudo chmod 400 /etc/munge/munge.key`
    - `sudo chown munge: /etc/munge/munge.key`
- Copy `/etc/cgroup.conf` and `/etc/cgroup_allowed_devices_file.conf` from the login node to the compute node using the same technique.
- Update `/etc/fstab` to show the following:

```bash
proc            /proc           proc    defaults          0       0
PARTUUID=3e3e7392-01  /boot/firmware  vfat    defaults          0       2
PARTUUID=3e3e7392-02  /               ext4    defaults,noatime  0       1
192.168.5.101:/sharedfs    /sharedfs    nfs    defaults   0 0
192.168.5.101:/home    /home    nfs    defaults   0 0
```

> **Note:** My `/etc/cgroup.conf` didn't get created automatically. I created it using:
>
> ```bash
> sudo tee /etc/cgroup.conf << 'EOF'
> CgroupPlugin=autodetect
> ConstrainCores=yes
> ConstrainRAMSpace=yes
> EOF
> ```
>
> Same for `/etc/slurm/cgroup_allowed_devices_file.conf`:
>
> ```bash
> sudo tee /etc/slurm/cgroup_allowed_devices_file.conf << 'EOF'
> /dev/null
> /dev/urandom
> /dev/zero
> /dev/sda*
> /dev/cpu/*/*
> /dev/pts/*
> /dev/shm
> EOF
> ```

## Start munge and slurmd

Now that the config files are in place, start munge first (slurmd depends on it), then slurmd:

```bash
sudo systemctl restart munge
sudo systemctl restart slurmd
sudo systemctl status slurmd
```

`slurmd` should now show `active (running)`. If it still fails, check the log for details:

```bash
sudo journalctl -u slurmd -n 30
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

Unlike the login node (which keeps `wlan0` as its internet uplink), the compute
node can now disable WiFi. All traffic will route through `eth0` to the login
node and out via its `wlan0` connection.

`sudo nmcli con down netplan-wlan0-CarpentriesOffline` should take down the
default network configured in the Raspberry Pi Imager software. However, we can
permanently disable the hardware for the built-in WiFi chip in the boot
configuration file.

Open `/boot/firmware/config.txt` and add the following two lines at the bottom
in the `[all]` section.

```ini
dtoverlay=disable-wifi
dtoverlay=disable-bt
```

Save the file and reboot
