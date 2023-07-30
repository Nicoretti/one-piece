#!/usr/bin/env python3
import sys
from {{ cookiecutter.project_slug }} import cli

if __name__ == "__main__":
    sys.exit(cli.main())
