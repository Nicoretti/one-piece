# AGENTS instructions

## General Guidelines

Beautiful is better than ugly.
Explicit is better than implicit.
Simple is better than complex.
Complex is better than complicated.
Flat is better than nested.
Sparse is better than dense.
Readability counts.
Special cases aren't special enough to break the rules.
Although practicality beats purity.
Errors should never pass silently.
Unless explicitly silenced.
In the face of ambiguity, refuse the temptation to guess.
There should be one-- and preferably only one --obvious way to do it.
Although that way may not be obvious at first unless you're Dutch.
Now is better than never.
Although never is often better than *right* now.
If the implementation is hard to explain, it's a bad idea.
If the implementation is easy to explain, it may be a good idea.
Namespaces are one honking great idea -- let's do more of those!

## Naming

Use short, clear, and precise names that follow general Python conventions.
Always prefer readability.

## Project overview

`ai-container` is a Podman-based CLI that isolates AI coding tools (PI,
OpenCode, aichat, llm) inside a container. The CLI is a Click/rich-click app.
All Podman setup (image build, image existence checks, volume creation) is done
through the **Podman Python SDK** (`podman` package); interactive container
launches use `podman run -it` via subprocess.

## Tooling: uv

This is a **uv-managed** Python project. Always use `uv`; never call `pip`,
`python`, or a manually activated venv directly.

| Task | Command |
|------|---------|
| Install/sync deps | `uv sync` |
| Add a dependency | `uv add <pkg>` |
| Add a dev dependency | `uv add --dev <pkg>` |
| Remove a dependency | `uv remove <pkg>` |
| Run the CLI | `uv run ai --help` |
| Run a script/module | `uv run python -m <module>` |
| Run a one-off tool | `uvx <tool>` |
| Build artifacts | `uv build` |
| Refresh the lockfile | `uv lock` |

- Dependencies are declared in `pyproject.toml`; the resolved set is pinned in
  `uv.lock`. **Commit `uv.lock`.**
- After editing dependencies in `pyproject.toml`, run `uv lock` then `uv sync`.
- Target Python is pinned in `.python-version` (3.13). Honor
  `requires-python = ">=3.13"`.

## Project layout

```
pyproject.toml              # project metadata + dependencies (uv)
uv.lock                     # locked dependency set (commit this)
.python-version             # pinned Python version
src/ai_container/
  cli.py                    # Click command definitions
  _podman.py           # Podman SDK helpers (build/volumes/run)
  Containerfile             # image definition, shipped as package data
README.md
```

## Conventions

- **CLI:** use `rich_click as click`. Add new commands in `cli.py` and register
  them with `ai.add_command(...)`. Call `_prepare(rebuild_image)` before any
  container run so the image and volumes exist.
- **Podman work:** put any image/volume/network logic in `_podman.py`
  using the SDK (`PodmanClient`). Only fall back to `podman run` subprocess for
  interactive TTY sessions.
- **Type hints:** all functions are typed; keep docstrings (Google style) on
  public functions.
- **Imports:** use absolute imports (`from ai_container._podman import ...`).

## Validation before finishing

Run these and make sure they pass:

```bash
uv sync
uv run ai --help                 # CLI loads
uv run python -c "from ai_container import cli, _podman"  # imports OK
uv build                         # packaging works
```

If you change dependencies, also run `uv lock` and confirm `uv.lock` is updated.

## Python idioms

### General
- **Named parameters** for inline primitives, to make call sites readable:
    GOOD: `twitter_search("@obama", retweets=False, numtweets=20, popular=True)`
    BAD: `twitter_search("@obama", False, 20, True)` - consider keyword-only args in APIs.
- **Unpacking** instead of index access:
    GOOD: `firstname, lastname, age, email = person`
    BAD: `firstname = person[0]; lastname = person[1]; ...`

### Strings
- **Concatenate with `.join`**, not `+=` in a loop:
    GOOD: `", ".join(names)`
    BAD: `output = ""; for name in names: output += name + ", "`
- **f-strings** for simple placeholders:
    GOOD: `f"Firstname: {user.first_name}, Age: {user.age}"`
    BAD: `"Firstname: {}, Age: {}".format(user.first_name, user.age)`
- **`str.format` with a template** for complex/multi-line output (named fields,
    `"\n".join(...)` generators) instead of incremental `+=` building.

### Looping
- **Iterate the collection**, not indices:
    GOOD: `for color in colors:` 
    BAD: `for i in range(len(colors)): colors[i]`
- **`range`** for number sequences: 
    GOOD: `for i in range(6):`
    BAD: `for i in [0,1,2,3,4,5]:`
- **`enumerate`** for index+value:
    GOOD: `for index, customer in enumerate(customers):`
    BAD: manual `index = 0; ...; index += 1`
- **`reversed`** to iterate backwards:
    GOOD: `for c in reversed(customers):`
    BAD: `for i in range(len(customers)-1, -1, -1):`
- **`zip`** for two collections:
    GOOD: `for name, color in zip(names, colors):`
    BAD: index loop with `min(len(...), len(...))`
- **Sentinel iter** instead of `while True: ... break`:
    GOOD: `for block in iter(partial(f.read, 32), ""):`

### Dictionaries
- **Build from pairs**:
    GOOD: `dict(enumerate(colors))`
    BAD: manual loop assigning `d[i]`
- **Count with `collections.Counter`**:
    GOOD: `Counter(colors)`
    BAD: `defaultdict(int)` + manual increment.
- **Layer with `collections.ChainMap`** (first map wins):
    GOOD: `ChainMap(cli_args, env_args, cfg_args)`
    BAD: `{}` + repeated `.update(...)` in priority order.

### Separation of concerns
- **Use `filter` / generator expressions** to separate selection from
  aggregation, instead of one loop with branching accumulators:
  GOOD: `odd = filter(lambda n: n % 2, numbers); even = (n for n in numbers if not n % 2)`
  BAD: single `for` loop with `if/else` accumulating `odd`/`even`.

## Notes / gotchas

- The Podman SDK needs the Podman service socket running
  (`systemctl --user enable --now podman.socket`). Code should fail gracefully
  with a helpful message when it is not reachable.
- Package data: the `Containerfile` must stay listed so `uv build` ships it in
  the wheel. Verify with:
  `uv run python -c "import zipfile,glob; print(zipfile.ZipFile(sorted(glob.glob('dist/*.whl'))[-1]).namelist())"`
