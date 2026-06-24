# AI-Container

Podman based container for isolating AI tooling for a individual project.

## Context

In the past, I have repeatedly observed and experienced coding agents accessing or using files and content which they either weren't supposed to, or even technically "did not have access to."

On one occasion, for example, file access was explicitly restricted (e.g., the path was blocked). However, the agent exploited its ability to run bash commands, using them to traverse and scan the restricted paths instead of relying on standard read/write methods.

For this reason, I believe it is essential to implement clear restrictions or a contextual sandbox that is shared with the AI, and which it cannot as easily circumvent by simply invoking a different command.


## Prerequisites

- **Podman** (>= 4.0) - Container runtime. [Install](https://podman.io/docs/installation)
- **Python** (>= 3.13) - Required for the CLI. [Install](https://www.python.org/downloads/)
- **uv** - Used to install and run the CLI. [Install](https://docs.astral.sh/uv/)

Image builds and volume creation are performed through the
[Podman Python SDK](https://github.com/containers/podman-py), which talks to
the Podman service socket. Make sure the socket is running:


## Installation

Install the `ai-container` package:

```bash
uv tool install ai-container
```

Or from source:

```bash
git clone https://github.com/yourusername/ai-container.git
cd ai-container
uv tool install .
```

The `ai` command will then be available.

## Usage

### Basic Commands

```bash
ai agent pi /path/to/project        # Run PI coding agent
ai agent opc /path/to/project       # Run OpenCode coding agent
ai agent aic /path/to/project       # Run aichat
ai agent llm /path/to/project       # Run llm
ai shell /path/to/project           # Interactive shell in container
```

`ai agent <tool> <path> [args]` is the single entry point for every tool.
Valid tools: `pi`, `opc`, `aic`, `llm`.

Pass additional arguments directly to the tool:
```bash
ai agent pi /path/to/project --verbose --model claude-3-sonnet
```

### Rebuilding the Container Image

The container image is built automatically on first use via the Podman SDK.
When you want to pull in the latest tool versions, force a rebuild with the
`image rebuild` command:

```bash
ai image rebuild
```

### Custom Environments

Need a specific toolchain (Rust, Go, an extra editor, ...)? Define a **custom
environment**: a thin image built `FROM aic:base` that adds your tooling on top
of everything the base image already provides.

Select an environment for any command with `-e/--env`:

```bash
ai -e rust shell .            # shell in the rust environment
ai -e rust agent pi .         # run pi in the rust environment
ai -e rust image rebuild      # (re)build the rust image (FROM aic:base)
```

Manage environment definitions with the `env` group:

```bash
ai env list                   # show environments and whether images are built
ai env new rust               # scaffold a Containerfile (FROM aic:base)
ai env new rust --edit        # scaffold and open it in $EDITOR
ai env edit rust              # edit the Containerfile
ai env path rust              # print the Containerfile path
ai env remove rust --purge    # delete the definition (and its image)
```

Definitions live under `~/.config/ai-container/environments/<name>/`
(honoring `XDG_CONFIG_HOME`). The directory is also the build context, so you
can `COPY` local files into your image. A scaffolded `Containerfile` looks like:

```dockerfile
# rust environment -- extends the ai-container base image.
FROM aic:base

RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs \
    | sh -s -- -y --default-toolchain stable
ENV PATH="/root/.cargo/bin:${PATH}"

WORKDIR /workspace
```

Without `-e`, the default `base` environment is used. Persistence volumes
(`config`, `state`, `share`, `pi-config`, `claude`) are shared across all
environments, so credentials and config are entered once and work everywhere.
### Provided Tools
- **[PI](https://shittycodingagent.ai)** - Coding agent for generation, analysis, and refactoring
- **[OpenCode](https://opencode.ai)** - AI-powered coding assistant
- **[aichat](https://github.com/sigoden/aichat)** - Interactive AI chat interface
- **[llm](https://github.com/simonw/llm)** - Command-line tool for LLM interaction

### Configuration & Persistence

**First run:** The container image is built (one-time, takes a few minutes).

**Tools use their standard configuration methods** (within the container):
- aichat: `~/.config/aichat/config.toml`
- llm: `~/.config/llm/` + environment variables
- PI: `~/.pi/`
- OpenCode: `~/.config/opencode/`

**Configuration persists automatically across all runs and containers** through named Podman volumes (`config`, `state`, `share`, `pi-config`). Configure once, use everywhere:

```bash
# First run: setup credentials
ai shell /path/to/project
# Inside container: aichat, llm keys set openai <key>, etc.

# Subsequent runs: credentials available automatically
ai agent pi /path/to/project
```

## Other/Previous Work
* [agent-containers](https://github.com/faileon/agent-containers)
* [agent-container](https://github.com/asfaload/agents_container)
* [opencode-dockerized](https://github.com/glennvdv/opencode-dockerized/tree/main)
