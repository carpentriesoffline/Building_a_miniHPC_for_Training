---
title: 'Reference'
---

## Glossary

**apt**
: The package manager used on Debian-based Linux systems (including Raspberry Pi OS) to install, update, and remove software.

**Batch job**
: A non-interactive unit of work submitted to the scheduler via `sbatch`. It runs when resources become available and records output to a file.

**Cgroup (Control Group)**
: A Linux kernel feature used by SLURM to enforce CPU and memory limits on running jobs, preventing one job from consuming more than its allocated resources.

**Cluster**
: A group of computers (nodes) connected over a network and managed together as a single computing resource.

**Compute node**
: A node in the cluster dedicated to running jobs. Learners do not log in to compute nodes directly; work is submitted via the scheduler.

**DHCP (Dynamic Host Configuration Protocol)**
: A network service that automatically assigns IP addresses to devices when they join a network. The login node runs a DHCP server (dnsmasq) for the cluster's internal network.

**dnsmasq**
: Lightweight software running on the login node that provides both DHCP (IP address assignment) and DNS (hostname resolution) for the cluster's internal network.

**DNS (Domain Name System)**
: The service that translates human-readable hostnames (e.g. `node01.local`) into IP addresses so computers can route traffic to them.

**EESSI (European Environment for Scientific Software Installation)**
: A shared software repository providing pre-built scientific applications for HPC clusters across different processor architectures, accessed via CVMFS.

**eth0**
: The name given to the first wired Ethernet network interface on a Linux system. On the login node, `eth0` connects to the internal cluster switch.

**Ethernet**
: Wired network technology using Cat5/Cat6 cables. The cluster's internal network connects all nodes via an Ethernet switch.

**Head node**
: Another name for the login node — the primary node through which users interact with the cluster.

**HPC (High Performance Computing)**
: Computing using clusters of machines to solve problems that require more memory or processing power than a single computer can provide.

**hostname**
: The human-readable name assigned to a computer on a network (e.g. `node01`). Every node in the cluster must have a unique hostname.

**Interactive job**
: A SLURM job that gives the user a shell directly on a compute node, launched with `srun --pty bash`. Useful for testing and debugging.

**IP address**
: A numerical identifier (e.g. `192.168.5.101`) that uniquely identifies a device on a network. Used for routing traffic between nodes.

**Job**
: A unit of computational work submitted to SLURM for execution on the cluster. Jobs are described by a script specifying resources and commands.

**Login node**
: The node through which users access the cluster via SSH. It runs the SLURM controller, NFS server, and DHCP/DNS server. Also called the head node.

**mDNS (Multicast DNS)**
: A protocol allowing devices to advertise and discover hostnames ending in `.local` on a local network without a central DNS server. Built into macOS and Linux; less reliable on Windows.

**MPI (Message Passing Interface)**
: A standard library for writing programs that run in parallel across multiple processors or nodes, communicating by passing messages.

**microSD card**
: The small flash storage card that Raspberry Pis boot from. The OS image is written to it using the Raspberry Pi Imager.

**Munge**
: An authentication daemon that ensures only trusted SLURM daemons can communicate within the cluster. All nodes must share an identical `munge.key`.

**NAT (Network Address Translation)**
: A technique where the login node rewrites outgoing packets so that the compute nodes can reach the internet using the login node's external IP address.

**NFS (Network File System)**
: A protocol for sharing directories over the network. The login node exports `/home` and `/sharedfs` via NFS so that all compute nodes see the same files.

**nmcli**
: The command-line tool for NetworkManager on Raspberry Pi OS, used to configure static IP addresses, WiFi connections, and network interface settings.

**Node**
: An individual computer in the cluster. This workshop uses Raspberry Pis as nodes.

**NTP (Network Time Protocol)**
: Protocol for synchronising clocks across computers. All cluster nodes must have synchronised clocks for SLURM and logging to work correctly.

**OpenMPI**
: A widely-used open-source implementation of the MPI standard, providing the libraries and tools needed to compile and run parallel programs.

**Partition (SLURM)**
: A logical grouping of compute nodes used to organise job scheduling. Not to be confused with a disk partition. This workshop uses a single partition called `nodecluster`.

**PoE (Power over Ethernet)**
: Technology that delivers electrical power through Ethernet cables, allowing a single cable to supply both network connectivity and power to a device.

**Raspberry Pi**
: A low-cost single-board computer (SBC) used as the nodes in this mini-HPC cluster. This workshop targets the Raspberry Pi 4 (2 GB+) or newer.

**Raspberry Pi OS**
: The official Linux distribution for Raspberry Pis, based on Debian. This workshop uses the 64-bit Lite (headless) variant.

**sbatch**
: The SLURM command for submitting a batch job script. Resource requirements are specified with `#SBATCH` comment directives inside the script.

**SBC (Single Board Computer)**
: A complete computer built on a single circuit board, integrating CPU, RAM, and I/O. Raspberry Pis are SBCs.

**sinfo**
: A SLURM command that displays the status of cluster partitions and nodes.

**SLURM**
: The job scheduler and resource manager used in this workshop to submit, queue, and run jobs on the compute nodes.

**slurmd**
: The SLURM daemon running on each compute node. It receives jobs from the controller and executes them.

**slurmctld**
: The SLURM controller daemon running on the login node. It manages the job queue and allocates resources to submitted jobs.

**SQL**
: Not used in this workshop; mentioned only to contrast with SLURM's simpler accounting configuration.

**squeue**
: A SLURM command that shows the current state of the job queue, including running and pending jobs.

**srun**
: A SLURM command for running a command directly on a compute node. With `--pty bash` it opens an interactive shell.

**SSH (Secure Shell)**
: A protocol for securely logging in to and running commands on remote computers over a network. The primary way learners access the cluster.

**sudo**
: A command prefix that runs the following command with administrator (root) privileges. Required for system configuration changes.

**systemctl**
: The command-line tool for managing systemd services: starting, stopping, restarting, and checking the status of daemons such as `slurmd` and `munge`.

**systemd**
: The init system and service manager used by Raspberry Pi OS. It starts services at boot and monitors them during operation.

**wlan0**
: The name given to the first wireless network interface on a Linux system. On the login node, `wlan0` connects to the workshop WiFi router, providing internet access and learner connectivity.
