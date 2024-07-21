# Bind Priviledged Prots

## setcap

```shell
setcap 'cap_net_bind_service=+ep' /path/to/program
```

## autobind

see [man 1 autobind](https://manpages.ubuntu.com/manpages/oracular/en/man1/authbind.1.html)

## sysctl

```shell
sysctl net.ipv4.ip_unprivileged_port_start=80
```

or persistent

```shell
sysctl -w net.ipv4.ip_unprivileged_port_start=80.
```

!!! danger 

    Not a good idea; it allows binding of all ports starting at 80 as non-privileged. Instead, consider making exceptions for an app or for container binding.

## Resources & Links

* [StackOverflow](https://stackoverflow.com/questions/413807/is-there-a-way-for-non-root-processes-to-bind-to-privileged-ports-on-linux)
* [Superuser](https://superuser.com/questions/710253/allow-non-root-process-to-bind-to-port-80-and-443)

