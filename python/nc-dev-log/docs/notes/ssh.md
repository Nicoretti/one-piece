# Create a SSH Keypair

```
ssh-keygen -t ed25519
```

# Deploy key on server

```
ssh-copy-id -i .ssh/path_to_id user@host
```

# Disable Password authentication

# Edit config file

file: /etc/ssh/sshd_config

```
PubkeyAuthentication yes
PassowrdAuthentication no
```

## Restart sshd

```
systemctl restart sshd.service 
```


