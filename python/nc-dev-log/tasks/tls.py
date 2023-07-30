import sys
from inspect import cleandoc
from pathlib import Path
from shutil import which
from tempfile import TemporaryDirectory
from contextlib import contextmanager
from functools import wraps
from tasks.terminal import stderr
from rich.rule import Rule

from invoke import Collection, task


def requires_openssl(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not which("openssl"):
            error_msg = "Could not execute command: {name} (details: `openssl` is not available!)".format(
                name=f.__name__
            )
            stderr.print(error_msg, style="error")
            sys.exit(-1)
        return f(*args, **kwargs)

    return wrapper


_DEFAULT_DESTINATION = "./certs"
_ROOT_KEY = "RootCA.key"
_ROOT_CERT = "RootCA.crt"


@task
@requires_openssl
def ca(context, name="TestCA", destination=_DEFAULT_DESTINATION):
    """
    Create all artifacts required for a CA
    """
    destination = Path(destination)
    destination.mkdir(exist_ok=True)

    keyfile = destination / _ROOT_KEY
    certificate = destination / _ROOT_CERT

    # create key pair for the CA
    context.run(f"openssl genrsa -aes256 -out {keyfile} 4096")
    # create the CA certificate
    subject = "/CN=TEST CA/C=DE/L=Bavaria/O=Test Organization"
    context.run(
        f"openssl req -x509 -new -nodes -key {keyfile} -sha256 -days 365 -out {certificate} -subj '{subject}'"
    )


_SAN_CONFIG_TEMPLATE = (
    cleandoc(
        """
            [req]
            default_bits  = 4096
            distinguished_name = req_distinguished_name
            req_extensions = req_ext
            x509_extensions = v3_req
            prompt = no
            [req_distinguished_name]
            countryName = XX
            stateOrProvinceName = N/A
            localityName = N/A
            organizationName = Self-signed certificate
            commonName = {name} 
            [req_ext]
            subjectAltName = @alt_names
            [v3_req]
            subjectAltName = @alt_names
            [alt_names]
            {dns_entries}
            {ip_entries}
        """
    )
    + "\n"
)


@contextmanager
def san_config(name, dns_entries=None, ip_entries=None):
    dns_entries = dns_entries if dns_entries else []
    ip_entries = ip_entries if ip_entries else []
    with TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)
        config = tmpdir / "san.cnf"
        with open(config, "w") as f:
            f.write(
                _SAN_CONFIG_TEMPLATE.format(
                    name=name,
                    dns_entries="\n".join(
                        (f"DNS.{i} = {e}" for i, e in enumerate(dns_entries, 1))
                    ),
                    ip_entries="\n".join(
                        (f"IP.{i} = {e}" for i, e in enumerate(ip_entries, 1))
                    ),
                )
            )
        yield config


@task(iterable=["dns", "ip"])
@requires_openssl
def server(
    context,
    name="Test Server",
    destination=_DEFAULT_DESTINATION,
    dns=None,
    ip=None,
    root_cert=None,
    root_key=None,
):
    """
    Create all artifacts required for a server to do tls.
    """
    destination = Path(destination)
    destination.mkdir(exist_ok=True)

    keyfile = destination / "Server.key"
    signing_request = destination / "Server.csr"
    certificate = destination / "Server.crt"

    # create a server key without password
    context.run(f"openssl genrsa -out {keyfile} 4096")

    with san_config(name, dns, ip) as config:
        # create singing request
        context.run(
            f"openssl req -new -sha256 -key {keyfile} -out {signing_request} -config {config} -extensions v3_req"
        )

        # create signed server certificate
        root_cert = Path(root_cert) if root_cert else Path(destination / _ROOT_CERT)
        root_key = Path(root_key) if root_key else Path(destination / _ROOT_KEY)
        command = (
            f"openssl x509 -req -in {signing_request} -CA {root_cert} -CAkey {root_key} "
            f"-CAcreateserial -out {certificate} -days 90 -sha256 "
            f"-extfile {config} -extensions v3_req"
        )
        context.run(command)


@task
@requires_openssl
def tutorial(context, destination=_DEFAULT_DESTINATION):
    """
    Creates a full set of certificates (CA, Server, ...) according to the exasol TLS tutorial.

    (see also: https://github.com/exasol/exasol-java-tutorial/blob/main/tls-tutorial/doc/use_your_own_certificate.md)

    Args:
        destination:
    """
    destination = Path(destination)
    destination.mkdir(exist_ok=True)

    root_key = destination / _ROOT_KEY
    root_cert = destination / _ROOT_CERT

    from rich.prompt import Prompt

    stderr.print(Rule("Creating CA artifacts", style="info"), style="info")
    ca_key_password = Prompt.ask("Please enter a PEM pass phrase", password=True)

    stderr.print("Creating CA keys", style="info")
    context.run(
        f"openssl genrsa -passout pass:'{ca_key_password}' -aes256 -out {root_key} 4096"
    )

    stderr.print("Creating CA certificate", style="info")
    context.run(
        f"openssl req -x509 -new -nodes -key {root_key} "
        f"-sha256 -days 365 -out {root_cert} "
        f"-passin pass:'{ca_key_password}' "
        "-subj '/CN=TLS Tutorial CA/C=DE/L=Bavaria/O=Tutorial Organization'"
    )

    server_key = destination / "Server.key"
    signing_req = destination / "Server.csr"
    server_cert = destination / "Server.crt"

    stderr.print(Rule("Creating Server artifacts", style="info"), style="info")
    stderr.print("Creating server keys")
    context.run(f"openssl genrsa -out {server_key} 4096")

    stderr.print("Creating signing request")
    context.run(
        f"openssl req -new -nodes -key {server_key} "
        f"-sha256 -out {signing_req} "
        "-subj '/CN=TLS Tutorial XYZ Server/C=DE/L=Bavaria/O=Tutorial Organization'"
    )

    stderr.print(
        Rule("Create server certificate from signing request", style="info"),
        style="info",
    )
    with TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)
        config = tmpdir / "server_cert_extensions.cfg"
        with open(config, "w") as f:
            f.write(
                cleandoc(
                    """
                [extensions]
                keyUsage = critical, nonRepudiation, digitalSignature, keyEncipherment, keyAgreement
                basicConstraints = CA:false
                """
                )
            )
        context.run(
            f"openssl x509 -req -in {signing_req} "
            f"-CA {root_cert} -CAkey {root_key} -CAcreateserial "
            f"-out {server_cert} -days 90 -sha256 "
            f"-passin pass:'{ca_key_password}' "
            f"-extfile {config} -extensions extensions"
        )


namespace = Collection()
namespace.add_task(ca)
namespace.add_task(server)
namespace.add_task(tutorial)
