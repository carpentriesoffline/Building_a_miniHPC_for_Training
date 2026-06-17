# Building a mini-HPC for Training

A [Carpentries Incubator][incubator] lesson on configuring a small cluster of
Raspberry Pis to use as a self-contained HPC in a workshop setting.

**View the course online:** https://carpentriesoffline.github.io/Building_a_miniHPC_for_Training/

## Overview

Running HPC training on a real cluster is difficult: access is restricted,
accounts must be arranged in advance, shared resources are always in demand,
and an internet outage can derail the whole session. A mini-HPC built from
Raspberry Pis is the option we've been working on for teaching HPC classes. It
is cheap enough to own outright, physically portable, and completely
self-contained.

This lesson guides instructors through building and configuring a two-node
Raspberry Pi cluster from scratch. By the end, learners will have a working
HPC with a login node, a compute node, a shared filesystem, Slurm job
scheduling, and EESSI software modules: everything needed to run a realistic
HPC skills workshop such as the Carpentries Incubator course
[Introduction to High-Performance Computing](https://carpentries-incubator.github.io/hpc-intro/).

## Target audience

This lesson is aimed at **workshop instructors and system administrators** who
want to run hands-on HPC training without relying on access to a production
cluster. It's also applicable to hobbyists and people generally interested in
building a Raspberry Pi HPC cluster. Some Linux command-line experience is
assumed; prior HPC administration experience is not required. At a minimum,
learners should be familiar with the
[Unix Shell](https://swcarpentry.github.io/shell-novice/).

## Hardware

The minimum setup requires:

- 2 × Raspberry Pi 4 or 5 (2 GB RAM or more): one login node, one compute node
- 1 × network switch with enough ports for all nodes
- Ethernet cables (one per Pi)
- Power supplies for each Pi (or a PoE switch)
- 2 × microSD cards (32 GB recommended)

Most of the content can work on any old Pi, though older models may be too slow
to be tolerable in a workshop format, and have package differences on older
32-bit `armv6l` and `armv7l` SoCs. EESSI is not supported at all on 32-bit ARM
architectures.

Optional but useful: a USB flash drive for shared storage, cooling (e.g. a
small fan), and 3D-printed cases or a DIN rail mount.

## Lesson episodes

| Episode | Topic |
| ------- | ----- |
| 1. Introduction | Why a mini-HPC? Hardware requirements and lesson overview |
| 2. Preparing an SD card | Writing a Raspberry Pi OS image with the Pi Imager, pre-configuring hostname, user, SSH, and WiFi |
| 3. Booting and updating | First login via SSH, updating packages |
| 4. Configuring the login node | Static IP, NAT gateway (iptables), DHCP/DNS (dnsmasq), NFS shared filesystem, munge, Slurm controller, EESSI |
| 5. Configuring a compute node | Installing Slurm and munge, copying config from the login node, mounting NFS, disabling WiFi |
| 6. Extra: PXE booting | Creating a compute node disk image and booting additional nodes over the network |
| 7. Testing: your first job | Checking cluster health with `sinfo`, submitting batch jobs with `sbatch`, running interactive jobs with `srun` |
| 8. Loop devices for EESSI | Creating virtual disks with `losetup` so diskless compute nodes can run EESSI software |

## Contributing

Contributions are welcome. This lesson is maintained by the
[CarpentriesOffline][carpentriesoffline] community. Please open an issue or
pull request on GitHub, or join the discussion in The Carpentries Slack
(`#carpentriesoffline` channel).

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## Licence

This lesson is made available under the [Creative Commons Attribution
licence][cc-by] (CC-BY 4.0). See [LICENSE.md](LICENSE.md) for details.

[incubator]: https://carpentries-incubator.org/
[carpentriesoffline]: https://carpentriesoffline.org/
[cc-by]: https://creativecommons.org/licenses/by/4.0/

