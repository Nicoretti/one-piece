import sys
from pathlib import Path
from subprocess import run, PIPE

CURRENT_DIR = Path(__file__).parent.resolve()
sys.path.insert(0, f"{CURRENT_DIR.parent}")


def current_version():
    command = ['poetry', 'version', '-s']
    result = run(command, stderr=PIPE, stdout=PIPE, check=True)
    return result.stdout.decode().strip()


# -- Project information -----------------------------------------------------

project = "{{ cookiecutter.project_name }}"
author = "{{ cookiecutter.full_name }}"
copyright = author
# The full version, including alpha/beta/rc tags
release = f"{current_version()}"

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = []

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "furo"
html_title = f"{{ cookiecutter.project_name }} {release}"
html_context = {
    "display_github": True,
    "github_user": "{{ cookiecutter.github_username }}",
    "github_repo": project,
    "github_version": "main",
    "conf_py_path": "/docs/",
    "source_suffix": "rst",
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]
