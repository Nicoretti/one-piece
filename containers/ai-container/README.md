# AI-Container

Podman based container for isolating AI tooling for a individual project.

## Context

In the past, I have repeatedly observed and experienced coding agents accessing or using files and content which they either weren't supposed to, or even technically "did not have access to."

On one occasion, for example, file access was explicitly restricted (e.g., the path was blocked). However, the agent exploited its ability to run bash commands, using them to traverse and scan the restricted paths instead of relying on standard read/write methods.

For this reason, I believe it is essential to implement clear restrictions or a contextual sandbox that is shared with the AI, and which it cannot as easily circumvent by simply invoking a different command.

## Other/Previous Work
* [agent-containers](https://github.com/faileon/agent-containers)
* [agent-container](https://github.com/asfaload/agents_container)
* [opencode-dockerized](https://github.com/glennvdv/opencode-dockerized/tree/main)
