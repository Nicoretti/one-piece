# Let's Encrypt setup

## Disable Certbot login

## Add SSL/TLS group to system (acme)

```shell
sudo useradd cerbot
sudo groupadd -U certbot acme
sudo groupmems -g acme -a nginx
```

## Create directories and setup right for non root configuration

```
sudo mkdir -m 0740  /etc/letsencrypt/ /var/log/letsencrypt/ /var/lib/letsencrypt/
sudo chown -R certbot:acme /etc/letsencrypt/ /var/log/letsencrypt/ /var/lib/letsencrypt/
```

## Run commands as certbot

- 3.1. Create/Activate virtual env
- 3.2. install certbot
- 3.3 run certbot

```shell
sudo su -s /bin/fish certbot
```

### Various Commands

```shell
certbot certonly -n --agree-tos --email nico.coretti@gmail.com --expand --webroot -d blog.nicoretti.dev -d syncthing.nicoretti.dev -d services.nicoretti.dev -d shop.nicoretti.dev -d nicoretti.dev
sudo chown root:acme /etc/nginx/nginx.conf
sudo chown root:acme /var/log/nginx/error.log
certbot certonly -n --agree-tos --email nico.coretti@gmail.com --webroot -w /usr/share/nginx/html -d nicoretti.dev -d blog.nicoretti.dev -d syncthing.nicoretti.dev -d shop.nicoretti.dev -d services.nicoretti.dev -d cli.nicoretti.dev
```

