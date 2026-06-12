---
title: Booting and Updating
layout: default
---

## Running the OS for the first time

Once you have written the operating system to the microSD card you can insert the card into 
the RPi and switch it on. If you configured the OS with a Wifi SSID and enabled ssh you 
should be able to access the RPi via the wireless network using your desktop or laptop computer.

- Login to the Pi
Use SSH or login with a local console (if you have a monitor attached). Use the login details you used above to log into the Pi.

```bash
ssh <USERNAME>@<IP-ADDRESS>
```

In this example, the username would be `cw24`, and the password the password we set in the Raspberry Pi Imager.

### How do I find my IP address?

In the setup stage, you connected your Pi to the `CarpentriesOffline` WiFi network and gave each node a name, for example `node01`. You can use the `ping` command to check it is connected to the network:

```bash
❯ ping -c3 node001.local
PING node001.local (192.168.1.4): 56 data bytes
64 bytes from 192.168.1.4: icmp_seq=0 ttl=64 time=8.019 ms
64 bytes from 192.168.1.4: icmp_seq=1 ttl=64 time=11.158 ms
64 bytes from 192.168.1.4: icmp_seq=2 ttl=64 time=8.964 ms

--- node001.local ping statistics ---
3 packets transmitted, 3 packets received, 0.0% packet loss
round-trip min/avg/max/stddev = 8.019/9.380/11.158/1.315 ms
```

### Updating the software

Now you are connected, do an update and a full-upgrade:

```bash
sudo apt update
sudo apt full-upgrade
```
