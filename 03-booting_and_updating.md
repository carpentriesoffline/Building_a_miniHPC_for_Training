---
title: Booting and Updating
layout: default
---

## Running the OS for the first time

Once you have written the operating system to the microSD card you can insert the card into 
the RPi and switch it on. If you configured the OS with a Wifi SSID and enabled ssh you 
should be able to access the RPi via the wireless network using your desktop or laptop computer.

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

