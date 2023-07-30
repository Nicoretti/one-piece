  $ export ROOT=${TESTDIR}/../..

  $ cookiecutter --no-input ${ROOT}

  $ tree -all
  .
  `-- python_project_template
      |-- .github
      |   |-- dependabot.yml
      |   `-- workflows
      |       |-- gh-pages.yaml
      |       |-- linux-ci.yaml
      |       |-- macos-ci.yaml
      |       `-- windows-ci.yaml
      |-- .gitignore
      |-- README.rst
      |-- docs
      |   `-- .empty
      |-- examples
      |   `-- .empty
      |-- noxfile.py
      |-- pyproject.toml
      |-- scripts
      |   `-- .empty
      |-- src
      |   `-- python_project_template
      |       |-- __init__.py
      |       |-- __main__.py
      |       `-- cli.py
      `-- test
          |-- bench
          |   |-- python_project_template
          |   |   `-- cli_bench_test.py
          |   `-- scripts
          |       `-- .empty
          |-- integration
          |   |-- python_project_template
          |   |   `-- cli.t
          |   `-- scripts
          |       `-- .empty
          `-- unit
              |-- python_project_template
              |   `-- cli_test.py
              `-- scripts
                  `-- .empty
  
  18 directories, 21 files

