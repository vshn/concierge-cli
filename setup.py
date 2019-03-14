#!/usr/bin/env python3
"""
Packaging setup for Concierge CLI.
See: https://click.palletsprojects.com/en/7.x/setuptools/
"""
from os.path import abspath, dirname, join
from setuptools import find_packages, setup

import concierge_cli as package


def read_file(filename):
    """Get the contents of a file"""
    with open(join(abspath(dirname(__file__)), filename)) as file:
        return file.read()


setup(
    name='concierge-cli',
    version=package.__version__,
    license=package.__license__,
    author=package.__author__,
    author_email=package.__email__,
    description=package.__doc__.strip(),
    long_description=read_file('README.rst'),
    long_description_content_type='text/x-rst',
    url=package.__url__,
    packages=find_packages(exclude=['test*']),
    include_package_data=True,
    keywords=['cli', 'gitlab', 'management'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    python_requires='>=3.6',
    install_requires=read_file('requirements.in'),
    entry_points={
        'console_scripts': [
            'concierge-cli = concierge_cli.cli:main',
        ],
    },
)
