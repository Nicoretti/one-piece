# Setting up a technical user

## Add user

```shell
useradd <name>
```

## Disable login shell

```
usermod -s /bin/false <name>
```

!!! info
    Consider SSH Allow and Deny lists, as well as permitting only certificate-based logins.

## Execute commands as user

```shell
sudo su -s <shell> <username>
```
