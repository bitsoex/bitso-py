import os
from setuptools import setup

if os.path.exists('README.md'):
    long_description = open('README.md').read()
else:
    long_description = 'A python wrapper for the Bitso API.'

setup(
    name='bitso-py',
    version='3.0.0',
    author='Mario Romero',
    author_email='mario@bitso.com',
    packages=['bitso', 'tests'],
    url='https://github.com/bitsoex/bitso-py',
    license='LICENSE.txt',
    description='A python wrapper for the Bitso API.',
    long_description=long_description,
    install_requires=[
        "requests >= 2.2.1",
        "websocket-client == 0.40.0",
        "python-dateutil >= 1.5",
        "mock >= 2.0.0",
        "future >= 0.16.0"
    ],
)
