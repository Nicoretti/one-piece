from setuptools import setup, find_packages

MAJOR_VERSION = 0
MINOR_VERSION = 3
PATCH_VERSION = 0

VERSION_TEMPLATE = '{major}.{minor}.{patch}'

setup(
    name='sirtalkalot',
    version=VERSION_TEMPLATE.format(major=MAJOR_VERSION, minor=MINOR_VERSION, patch=PATCH_VERSION),
    packages=find_packages(),
    install_requires=['docopt', 'libslack', 'ws4py'],
    url='https://github.com/Nicoretti/sirtalkalot',
    license='BSD',
    author='Nicola Coretti',
    author_email='nico.coretti@gmail.com',
    description='A simple service based slack bot',
    entry_points={
        'console_scripts': [
        '   sirtalkalot=sirtalkalot.bots:main',
        ],
         'sirtalkalot.plugin.services': [
            'Chuck = sirtalkalot.services:ChuckNorris',
            'Zen = sirtalkalot.services:ZenOfPython',
        ],
    },
    keywords=['slack', 'bot', 'api'],
)
