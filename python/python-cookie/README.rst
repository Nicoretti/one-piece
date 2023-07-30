Nicoretti's Python Cookie
=========================

How to use this cookie
Asep

What's in the box
-----------------

TL;DR
+++++
* Github Actions
    - Dependabot (Weekly PR to catch up on Dependencies)
    - Github Pages
    - Linux CI (Python 3.x Matrix)
    - MacOs CI (Python 3.x Matrix)
    - Windows CI (Python 3.x Matrix)
* Dev Tools
    - pytest
    - prysk
    - pylint
    - black
    - isort
    - nox
    - mypy
    - coverage
    - sphinx
    - furo
* Structure
    - Project configuration pyproject.toml
        - Poetry
            - dependencies
            - publishing
    - Testing
        - unit (pytest)
        - integration (prysk)
        - performance / bench
    - Linting
        - Pylint
        - MyPy
        - Coverage
    - Task Runner/Automation (Nox)
        - check
        - fix
        - test (with coverage?)
            - ut
            - integration
            - bench
        - coverage?
        - doc
        - release
    - Documenation (Sphinx, Furo, GithubPages)


TODO's after publishing the baked cookie
+++++++++++++++++++++++++++++++++++++++++
* enable gh pages

TODO's for this Cookie
-----------------------
* Coverage target + reporting
* Detailed sphinx documenation for cookie
