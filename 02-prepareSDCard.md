---
layout: default
title: Preparing an SD Card
---

Every computer needs to load an operating system when you switch it on.
Therefore it will usually have a default place where it will look for an
operating system in the first place. The process of loading the operating system
is called **booting**. In general, if someone tells you to reboot your computer
it means to switch is off and switch it back on again so that the operating
system can be loaded from scratch. In the case of your desktop or laptop
computers you will have a hard drive built into the computer or alternatively
you might be able to boot from a USB device.

In the case of the Raspberry Pi its default booting device is an SD card.
Pre-RPi3 used a mini-SD card but RPi3 and RPi4 use micro-SD cards. SD cards are
available in various capacities, ie. the amount of information that can be
stored on it. A basic operating system for the Pi will probably take about 2GB
but then you will also need space for all the Carpentries lesson files and other
software that you want to make available to the learners.

Usually when you buy a RPi you can also buy an SD card with the operating system
pre-loaded. Alternatively you can buy an empty SD card and prepare it yourself.
Preparing the SD card involves downloading an **image** of the operating system
(and there are various versions available), downloading the software, Raspberry
Pi Imager, required for writing the image to the SD card and then using the
software to write the image to the SD card.

Internet connectivity might prove to be a problem during this workshop so your
instructor might bring an image along that can be copied or perhaps they will
provide pre-prepared microSD cards.


The Raspberry Pi can run several operating systems including several flavours
of Linux. The official Raspberry Pi OS is based on Debian Linux.

If you have not already done so you have to download and install the Raspberry
Pi Imager. Using your browser, navigate to the Raspberry Pi [download
page](https://www.raspberrypi.com/software/). You should now be able to select
the download for your operating system. Click on the appropriate link and save
the installation file to your computer. The web page will provide further
information for installing the software on your computer.
Once the installation is complete you should be able to run the Imager which
will open with the following screen:


## Creating an SD card image: step-by-step

###  Setting up a Raspberry Pi

The official [Set up your SD card](https://projects.raspberrypi.org/en/projects/raspberry-pi-setting-up/2) is up to date as of 2nd of May 2024.

When using the The Raspberry Pi Imager, select the Device and OS.

The OS selection should be `Raspberry Pi OS (other)` -> `Raspberry Pi OS Lite (64-bit)`.

![image alt >](/fig/screenshots/imager-hero-shot.png)

Selecting the device:

![image alt >](/fig/screenshots/imager-device-selection.png)


Selecting the OS:

![](/fig/screenshots/imager-OS-selection-1.png)

![](/fig/screenshots/imager-OS-selection-2.png)

After this, please select the sdcard you would like to flash the image on, Then press `NEXT`.

![](/fig/screenshots/imager-sd-card-selection.png)

it will ask if the user wants to do any customisation, select `EDIT SETTINGS`.

![](/fig/screenshots/imager-customiser-dialog.png)

This will show a pop-up window where the following configuration options can be defined for your set-up (below are examples) such that your OS is pre-configured upon first boot.

1. Hostname: `CW24miniHPC`
1. Username: `cw24`
1. Password: `*****`
1. WiFI SSID and Password: Enter your WiFi details

![](/fig/screenshots/imager-os-config.png)

Then go to the `SERVICES` tab and enable SSH with password authentication (alternatively, adding a ssh public key). If you would like to set up easy access to the Pi via an ssh key, please see [here](ssh-setup.md).

_TODO: Section on generating an ssh key-pair._

![](/fig/screenshots/imager-pwd-setup.png)


After, saving this, select `YES` to apply the configuration.

![](/fig/screenshots/imager-os-config-apply.png)

Confim writing to the sdcard (please backup any data on the sdcard, any existing data will be **LOST!**)

![](/fig/screenshots/imager-confirm-sdcard-write.png)














---

{% include image.html max-width="400px" file="fig/RaspberryPiImager.png" alt=
"The Raspberry Pi Imager" caption="The Raspberry Pi Imager" %}

You can now click on the **Choose OS** button which will open a window for
selecting the image you want to write to the SD card. Scroll down to the bottom
where you should find an option **Raspberry Pi OS (other)**. Click on that option:

{% include image.html max-width="400px" file="fig/ChooseImage.png" alt=
"Selecting an image to write to the SD card" caption="n image
of the RPi Imager software screen for selecting an image to be written to the SD
card" %}

Select **Raspberry Pi OS Lite (64 bit)**. Make
sure you have inserted the SD card into your computer. Now click on the **Choose
Storage** button and select the device you want to write the image to: 

{% include image.html max-width="400px" file="fig/SelectDevice.png" alt=
"Select a device to write the image to" caption="An image of the
RPi Imager software screen for selecting the device to be written to" %}

Once you have selected the Storage device, click the **WRITE** button. You will
be prompted to overwrite the information on the SD card, click on **YES** to
accept.

{% include image.html max-width="400px" file="fig/PromptToOverwrite.png" alt=
"Prompt to overwrite the SD card" caption="An image of
the RPi Imager software screen for confirming to overwrite the SD card" %}

The image will now be written to the SD card.

{% include image.html max-width="400px" file="fig/Writing.png" alt=
"Overwriting the SD card" caption="An image of the RPi Imager
software screen while writing the image to the SD card" %}

Once the image has been written to the SD card a **Write Successful** message
will be displayed.

{% include image.html max-width="400px" file="fig/ImageWritten.png" alt=
"Write Successful" caption="An image of the RPi Imager
software screen after the image has been written succesfully.d" %}

You can now remove the SD card from your computer and insert it into the
Raspberry Pi.

