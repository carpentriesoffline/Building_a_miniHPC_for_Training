---
layout: default
title: Setup
---

In this lesson you will learn how to create a high performance computer using
Raspberry Pi single board computers. The skills you learn will be transferrable
to any unix type operating system. The focus of this lesson is on the software
that is typically used on HPCs and not the hardware.

The minimum equipment you will need for this lesson would be:

- 2 x Raspberry Pi 4 or 5, one which will serve as the 
login node and one which will be a compute node. These do not need keyboards 
and screens but it is sometimes handy to have a keyboard and screen for when 
you run into trouble.
- One network switch.
- One laptop or computer which will serve as your workstation. It might prove
useful for this workstation to have an ethernet port.
- Three network cables.
- If your switch has Power over Ethernet (PoE) you might not need power supplies
for your two nodes. If they don't, don't forget the power supplies. Also don't 
forget the power supply for the switch itself.
- For starters you'll need two SD cards. One SD card will be used for the login
node and the other for the compute node. If, later on, you want to use PXE 
(i.e. boot over network), then you can use the compute node SD card to create
a template image for compute nodes

