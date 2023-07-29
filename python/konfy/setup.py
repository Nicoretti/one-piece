from pathlib import Path

from setuptools import setup

PROJECT_ROOT = Path(__file__).parent
README = (PROJECT_ROOT / "README.rst").read_text()

setup(
    name="konfy",
    version="0.1.0",
    py_modules=["konf"],
    url="https://github.com/Nicoretti/monotone/konfy",
    license="MIT",
    author="Nicola Coretti",
    author_email="nico.coretti@gmail.com",
    description="Read and write configuration settings",
    long_description=README,
    python_requires=">=3.8, <4",
    install_requires=["setuptools"],
)
