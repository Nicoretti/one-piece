# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "index-503",
#     "pip",
# ]
# ///
#
# one-pack: Create a portable, offline package index for Python projects
#
# This tool helps you create a self-contained package archive (.one-pack.zip) that includes
# all dependencies for a Python project. This is useful for offline installations or
# distributing applications in air-gapped environments.
#
# # How to package a project with one-pack
# uv run --script one-pack.py /path/to/myproject
#
# # How to install packages with one-pack
# Example install of an application packaged with one-pack:
#   unzip -d one-pack myproject.one-pack.zip
#   uv tool install --no-cache -f /path/to/one-pack <package-name-of-myproject>


import logging
import shutil
import subprocess
import sys
import tempfile
from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser
from pathlib import Path


def _create_parser() -> ArgumentParser:
    parser = ArgumentParser(
        description="Create a local packaging index for a project",
        formatter_class=ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "project",
        type=Path,
        help="Project for which a local package registry package shall be created",
    )
    return parser


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s", stream=sys.stderr)
    logger = logging.getLogger(__name__)

    parser = _create_parser()
    args = parser.parse_args()

    def create_requirements_txt(project: Path, dest: Path):
        uv = shutil.which("uv")
        if not uv:
            logger.error("uv executable not found in PATH")
            raise FileNotFoundError("uv not found")
        logger.debug(f"Using uv from: {uv}")

        command = [
            uv,
            "export",
            "--directory",
            project,
            "--format",
            "requirements.txt",
            "--no-annotate",
            "--no-header",
            "--no-hashes",
            "--no-dev",
            "--output-file",
            dest,
        ]
        logger.debug("Executing command: %", " ".join(str(c) for c in command))
        subprocess.run(command, check=True)
        logger.info("Requirements file created at: %", dest)

    def create_wheels(project: Path, requirements_txt: Path, dest: Path):
        uv = shutil.which("uv")
        logger.debug(f"Using uv from: {uv}")
        logger.debug(f"Reading requirements from: {requirements_txt}")
        logger.debug(f"Output directory: {dest}")

        command = [uv, "run", "--directory", project, "pip", "wheel", "-r", requirements_txt, "-w", dest]
        logger.debug(f"Executing command: {' '.join(str(c) for c in command)}")
        subprocess.run(command, check=True)
        logger.info("Wheels created")

    def create_package_index(project: Path, wheels_dir: Path, dest: Path):
        uv = shutil.which("uv")
        logger.debug(f"Using uv from: {uv}")
        logger.debug(f"Wheels directory: {wheels_dir}")

        command = [uv, "run", "index-503", wheels_dir]
        logger.debug(f"Executing command: {' '.join(str(c) for c in command)}")
        subprocess.run(command, check=True)
        index = wheels_dir.parent / "wheels-index"
        index = index.resolve()
        name = f"{project.name}.one-pack"
        one_pack = shutil.make_archive(name, "zip", root_dir=index)
        logger.info(f"Package index created: {one_pack}")

    logger.info(f"Creating one-pack for project: {args.project}")
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)
        requirements_txt = tmpdir / "requirements.txt"
        wheels_dir = tmpdir / "wheels"
        project = args.project
        logger.info(f"Step 1/3: Exporting project dependencies from {project}")
        create_requirements_txt(project, requirements_txt)
        logger.info("Step 2/3: Building wheels for dependencies")
        create_wheels(project, requirements_txt, wheels_dir)
        logger.info("Step 3/3: Creating package index from wheels")
        create_package_index(project, wheels_dir, Path.cwd())


if __name__ == "__main__":
    main()
