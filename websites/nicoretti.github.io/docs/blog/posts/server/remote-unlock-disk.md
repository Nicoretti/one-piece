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

## TL;DR

Unlocking encrypted root partion of a Debian based system (Ubuntu 22.04) via ssh.

1. Install `dropbear-initramfs` package
2. Adjust configuration `/etc/dropbear/initramfs/dropbear.conf`
3. Create or add key to `/etc/dropbear/initramfs/authorized_keys`
4. Update the `initramfs`: `sudo update-initramfs -u`
5. Reboot `sudo systemctl reboot`
6. Connect to the booting machine (`ssh root@<host>`) and unlock the encrypted partion using `cryptroot-unlock`

## Background

I recently came back to doing some server management, setting up a basic home server and opting for hosting some services myself. While encrypting the drives of laptops or desktops is a no brainer, applying similar security measures to a server might not seem as obvious or easy to everyone, even though it can be.

### Why Encrypt Your Server Disk?

The rationale behind encrypting a server disk might vary, but there are two primary benefits I believe make it indispensable:

- **Data Erasure Security:** Ensuring that data is irrecoverable when I choose to delete it helps maintain online privacy and security. It's about making sure that the internet has the ability to "forget."
- **Protection Against Unauthorized Access:** Encrypting the disk offers a fundamental layer of security against potential theft or unauthorized access to the disk storage by the hosting provider or others.

!!! warning "Disclaimer" 

    It's crucial to recognize that lacking physical control over the machine introduces additional attack vectors,
    potentially reducing some of the security guarantees. However, in my opinion, the benefits of disk encryption still outweigh the effort.


## Compatibility and System Requirements

This walkthrough is tailored for Debian-based systems, specifically highlighting **Ubuntu 22.04**.
Although the general workflow should be consistent, package names and paths may differ across distributions and versions.

??? tip "Tip: Fedora and Dracut Users"

    For those using Fedora or systems that employ Dracut, a similar setup can be achived using Dracut and [dracut-crypt-ssh](https://github.com/dracut-crypt-ssh/dracut-crypt-ssh).

## Setting Up the Basic System

This section will guide you through the initial steps of setting up your system to unlock the LUKS disk encryption via SSH.

### Install Required Packages

```shell
sudo apt install dropbear-initramfs
```

??? tip "Tip: Systems != Ubunut 22.04"

    For systems which aren't `Ubuntu 22.04`, having a look into the dependencies of the [Package: dropbear-initramfs](https://packages.ubuntu.com/jammy/dropbear-initramfs) may reveal packages and/or tools required on your system for this setup.

### Generate SSH Key

!!! note 

    In case you already have a keypair you want to use for authentication you can skip this step.


```shell
ssh-keygen -t ed25519 -C "<servername> - disk encryption unlock key"
```
??? tip "Tip: What to use as comment"

    You can use an arbitrary string for the `-C` flag, just make sure that you put something there
    that helps you identifying purpose of that key. This usually is/gets relevant when you are using
    different keys for different prurposes (which is recommeded). Having a "Good" key easily 
    can be a single point of failure in your security archtiecture.


??? tip "Tip: Managing SSH-Keys"

    Using a password store like keepassxc or ... to manage your ssh-keys toghether with
    their built in ssh agent. Can simplify the usage of multiple keys while still adding
    a reasonable amount of protection.

### Configure Dropbear

If you navigate to the folder `/etc/dropbear/initramfs/` there should be a file named `dropbear.conf`,
whose content should look somewhat like this:
```ini
#
# Configuration options for the dropbear-initramfs boot scripts.
# You must run update-initramfs(8) to effect changes to this file (like
# for other files in the '/etc/dropbear/initramfs' directory).

#
# Command line options to pass to dropbear(8)
#
#DROPBEAR_OPTIONS=

#
# On local (non-NFS) mounts, interfaces matching this pattern are
# brought down before exiting the ramdisk to avoid dirty network
# configuration in the normal kernel.
# The special value 'none' keeps all interfaces up and preserves routing
# tables and addresses.
#
#IFDOWN=*

#
# On local (non-NFS) mounts, the network stack and dropbear are started
# asynchronously at init-premount stage.  This value specifies the
# maximum number of seconds to wait (while the network/dropbear are
# being configured) at init-bottom stage before terminating dropbear and
# bringing the network down.
# If the timeout is too short, and if the boot process is not blocking
# on user input supplied via SSHd (ie no remote unlocking), then the
# initrd might pivot to init(1) too early, thereby causing a race
# condition between network configuration from initramfs vs from the
# normal system.
#
#DROPBEAR_SHUTDOWN_TIMEOUT=60
```
As you can see all settings are commented out:

* `#DROPBEAR_OPTIONS=`
* `#IFDOWN=*`
* `#DROPBEAR_SHUTDOWN_TIMEOUT=60`

Still this setup should work in a lot of cases.

!!! danger

    If you are running this setup on a publicly available host, please read through the section
    **Enhancing Convenience and Security** make sure you lock down the endpoint as much
    as possible before you deploy your configuration.

### Add authorized_keys

Add or update an `authorized_keys` file to `/etc/dropbear/initramfs/` to enable those keys to login and therefore unlock the system.

```
```

??? question "What does the authorized\_keys file contain"
    
    ... public keys ...
    How does a keyfile look like

    ```ini
    key ..
    ```


### Generate Initramfs
Everytime you update the `dropbear.conf` or `authorized_keys` file you need to update your `initramfs`
using the command `udpate-initramfs`, see also: [update-initramfs(8)](https://manpages.ubuntu.com/manpages/jammy/en/man8/update-initramfs.8.html).

```shell
sudo update-initramfs -u -v
```

### Unlock
1. Connect to your host

    ```shell
    ssh root@HOST
    ```

2. Unlock the system

    ```shell
    cryptroot-unlock
    ```

3. Wait

    !!! note 

        After a few more seconds (depending) on your init and boot setup, the machine should be
        up and runnnning and you should be able to connect e.g. via ssh to it.jK:w


## Enhancing Convenience and Security

This section discusses enhancements convenience and security.

- **Dropbear Configuration/Security Tweaks:** Exploring flags and options for Dropbear.


## Gotchas and How to Tackle Them

This section addresses some of the typical challenges you might encounter when setting up or using the setup described obove.

- **Port Management:** Strategies for choosing different ports for Dropbear and OpenSSH to improve security, including considerations for duplication and subdomains.
- **Command Execution in Dropbear:** Ensuring Dropbear executes commands as expected.
- **Multi-Partition/Disk Encryption:** Strategies for managing multiple partitions or disks with different passwords.
- **User Access:** Connecting to Dropbear as a user other than `root` and its implications.
- **Key Management:** Handling different server keys for Dropbear and OpenSSH when using the same URL/endpoint, with a focus on strict checking.
- **Unlocking Mechanism:** Methods to allow only `cryptunlock` commands and scripts to enhance security.


## Links & Resources

* [Dropbear SSH](https://matt.ucc.asn.au/dropbear/dropbear.html)
* [Package: dropbear-initramfs](https://packages.ubuntu.com/jammy/dropbear-initramfs)
* [dropbear(8)](https://manpages.ubuntu.com/manpages/jammy/en/man8/dropbear.8.html)
* [cryptsetup(8)](https://manpages.ubuntu.com/manpages/jammy/en/man8/cryptsetup.8.html)
* [update-initramfs(8)](https://manpages.ubuntu.com/manpages/jammy/en/man8/update-initramfs.8.html)
* [dcracut-crypt-ssh](https://github.com/dracut-crypt-ssh/dracut-crypt-ssh)
* [ceremcem/unlock-luks-partition](https://github.com/ceremcem/unlock-luks-partition)
* [Remotely unlock a LUKS-encrypted Linux server using Dropbear (Debain 12)](https://www.dwarmstrong.org/remote-unlock-dropbear/)
* [UNLOCKING A LUKS FULLY ENCRYPTED DRIVE AND BOOTING INTO THE OS VIA DROPBEAR](https://swissmade.host/en/blog/unlocking-a-luks-fully-encrypted-drive-and-booting-into-the-os-via-dropbear-ssh)
* [How to unlock LUKS using Dropbear SSH keys remotely in Linux](https://www.cyberciti.biz/security/how-to-unlock-luks-using-dropbear-ssh-keys-remotely-in-linux/)

