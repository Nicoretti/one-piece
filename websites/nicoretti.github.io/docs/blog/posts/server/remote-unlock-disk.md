---
draft: true
date: 2024-03-03
categories:
  - Server
  - Linux
  - LUKS
  - SSH
  - Dropbear
  - initramfs
---


# Remote Unlocking Encrypted Linux System Partition

![Unlocking LUKS vis Dropbear](../../../images/DALL-E/unlocking-luks-via-dropbear.webp)

:material-information-outline:{ title="Craft an image of a server and its data disk under the vigilant protection of a formidable bear, symbolizing an unbreakable lock, all set within a vivid digital realm. The path to this secure server is a digital highway, encrypted with cryptic data, emphasizing the fortified access against unauthorized intrusion, with the entire scenery unfolding in a visually rich, digital landscape." } *Image created by DALL-E, OpenAI's image generation model.*

### TL;DR

Unlocking encrypted root partion of a Debian based system (Ubuntu 22.04) via ssh.

* Install `dropbear-initramfs` package
* Adjust configuration `/etc/dropbear/initramfs/dropbear.conf`
* Create or add key to `/etc/dropbear/initramfs/authorized_keys`
* Update the `initramfs`: `sudo update-initramfs -u`
* Reboot `sudo systemctl reboot`
* Connect to the booting machine (`ssh root@<host>`) and unlock the encrypted partion using `cryptroot-unlock`

