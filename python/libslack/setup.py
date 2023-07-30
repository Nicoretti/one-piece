from setuptools import setup, find_packages
from libslack.version import VERSION_TEMPLATE, MAJOR_VERSION, MINOR_VERSION, PATCH_VERSION

setup(
    name='libslack',
    version=VERSION_TEMPLATE.format(major=MAJOR_VERSION, minor=MINOR_VERSION, patch=PATCH_VERSION),
    packages=find_packages(),
    install_requires=['docopt'],
    url='https://github.com/Nicoretti/libslack',
    license='BSD',
    author='Nicola Coretti',
    author_email='nico.coretti@gmail.com',
    description='A lightweight wrapper around the slack web API.',
    entry_points={
        'console_scripts': [
            'scmd=libslack.scmd:main',
            'sls=libslack.sls:main',
        ],
    },
    keywords=['slack', 'cmd', 'api', 'shell'],
)
