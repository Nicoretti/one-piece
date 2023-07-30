## Resources

### Reads

* [OpenLDAP Docker Image](https://hub.docker.com/r/bitnami/openldap)
* [How to setup OpenLdap](https://www.digitalocean.com/community/tutorials/how-to-install-and-configure-openldap-and-phpldapadmin-on-an-ubuntu-14-04-server)
* [Tutorial LDAP Utilis](https://www.digitalocean.com/community/tutorials/how-to-manage-and-use-ldap-servers-with-openldap-utilities)
* [Apply changes in LDAP](https://www.digitalocean.com/community/tutorials/how-to-use-ldif-files-to-make-changes-to-an-openldap-system)

### Libraries

* [python-ldap](https://www.python-ldap.org/en/python-ldap-3.4.3/index.html)

### Basic Queries

#### Basic anonymous query

```shell
 ldapsearch -H ldap://127.0.0.1:1389 -x -LLL -s base -b "dc=example,dc=org
```

```python
import ldap

client = ldap.initialize("ldap://127.0.0.1:1389")
status = client.simple_bind()
query_result = client.search_s("dc=example,dc=org", ldap.SCOPE_SUBTREE)
```

#### Basic authenticated query

```shell
ldapsearch -H ldap://127.0.0.1:1389 -x -LLL -s base -D "cn=admin,dc=example,dc=org" -w pw -b "ou=users,dc=example,dc=org" -v
```

```python
import ldap

client = ldap.initialize("ldap://127.0.0.1:1389")
status = client.simple_bind("admin", "pw")
query_result = client.search_s("dc=example,dc=org", ldap.SCOPE_SUBTREE)
```

#### Basic authenticated query interactive password

```shell
ldapsearch -H ldap://127.0.0.1:1389 -x -LLL -s base -D "cn=admin,dc=example,dc=org" -W
```

#### Basic tls secured query

