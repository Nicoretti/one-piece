{{ cookiecutter.project_name }}
=================================

{% if cookiecutter.linux_ci | lower == "true" -%}
.. image:: https://github.com/Nicoretti/{{ cookiecutter.project_slug }}/actions/workflows/linux-ci.yaml/badge.svg
    :target: https://github.com/Nicoretti/{{ cookiecutter.project_slug }}/actions/workflows/verifier.yaml
{%- endif %}

{% if cookiecutter.macos_ci | lower == "true" -%}
.. image:: https://github.com/Nicoretti/{{ cookiecutter.project_slug }}/actions/workflows/macos-ci.yaml/badge.svg
    :target: https://github.com/Nicoretti/{{ cookiecutter.project_slug }}/actions/workflows/macos-ci.yaml
{%- endif %}

{% if cookiecutter.windows_ci | lower == "true" -%}
.. image:: https://github.com/Nicoretti/{{ cookiecutter.project_slug }}/actions/workflows/windows-ci.yaml/badge.svg
    :target: https://github.com/Nicoretti/{{ cookiecutter.project_slug }}/actions/workflows/windows-ci.yaml
{%- endif %}

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black

.. image:: https://img.shields.io/badge/imports-isort-ef8336.svg
    :target: https://pycqa.github.io/isort/

.. image:: https://img.shields.io/badge/docs-available-blue.svg
    :target: https://nicoretti.github.io/{{ cookiecutter.project_slug }}/

.. image:: https://img.shields.io/pypi/v/{{ cookiecutter.project_slug }}
     :target: https://pypi.org/project/{{ cookiecutter.project_slug }}/
     :alt: PyPI Version


Getting Started
+++++++++++++++

#. Setup virtual environment for development

    .. code-block:: shell

        poetry shell

#. Install a dependencies

    .. code-block:: shell

        poetry install

#. List all tasks/targets

    .. code-block:: shell

        nox -l

