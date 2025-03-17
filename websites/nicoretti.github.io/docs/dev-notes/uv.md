# UV

## Adding Packages From Authenticated Package Repositories

This writeup explains how to configure `uv` to access package repositories that require authentication, using the `keyring` tool and the `pyproject.toml` file.

### 1. Setup the Keyring Tool & Required plugins

You need to install both the `keyring` tool and a backend that supports your specific repository. For example, for Google Artifact Registry, you'll need `keyrings.google-artifactregistry-auth`.

There are various ways to do this e.g. via dev-dependencies or the `uv tool` command. In this example we will use the `uv tool` command.


#### 1. Install

```shell
uv tool install keyring --with keyrings.google-artifactregistry-auth
```

#### 2. Verify The Install

The command below should list all available keyring backends which should contain the one(s) you require.

```shell
uv run keyring --list-backends
```

#### 3. Authenticate

ATTENTION: It is cruciall, that you configure `keyring` with the credentials for your repositories before `uv` can access them.

The exact process here depends on the backend though.
E.g.: In the case of a google bucket you likely setup something like Default Credentials (details see [here](https://cloud.google.com/docs/authentication/application-default-credentials)).

Note: Depending on the backend, adding the credentials to the keyring already could be sufficient.

```bash
uv run keyring set ...
```


### 2. Add The `extra-index-url` And Configure A Keyring Provider.

Once setting up the keyring tool and the credentials is done, one needs to configure the project accordingly.
This can be achieved by adding the snippet bellow to the project configuration (`pyproject.toml`).

```toml
[tool.uv]
extra-index-url = [
    "https://your-private-repo.com/simple/",  # Replace with your repository URL(s)
    # ... add more URLs as needed
]
keyring-provider = "subprocess"
```

### 3. Installing Packages From The Authenticated Package Index

Now you should be able to just install any package hosted on the newly added index like every other package.

Example:

```bash
uv add <some-package-from-the-new-auth-reg>
```
