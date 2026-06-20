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
ai pi /path/to/project              # Run PI coding agent
ai opc /path/to/project             # Run OpenCode coding agent
ai aic /path/to/project             # Run aichat
ai llm /path/to/project             # Run llm
ai shell /path/to/project           # Interactive shell in container
```

Pass additional arguments directly to the tool:
```bash
ai pi /path/to/project --verbose --model claude-3-sonnet
```

### Rebuilding the Container Image

The container image is built automatically on first use via the Podman SDK.
When you want to pull in the latest tool versions, you can force a rebuild in
two ways:

**Standalone rebuild command** — rebuilds the image without running any tool:
```bash
ai rebuild-image
```

**Inline `--rebuild-image` flag** — rebuilds the image and then immediately runs the chosen tool:
```bash
ai pi /path/to/project --rebuild-image
ai opc /path/to/project --rebuild-image
ai aic /path/to/project --rebuild-image
ai llm /path/to/project --rebuild-image
ai shell /path/to/project --rebuild-image
```
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
ai pi /path/to/project
```

## Other/Previous Work
* [agent-containers](https://github.com/faileon/agent-containers)
* [agent-container](https://github.com/asfaload/agents_container)
* [opencode-dockerized](https://github.com/glennvdv/opencode-dockerized/tree/main)
