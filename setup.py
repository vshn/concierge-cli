#!/usr/bin/env python3
"""
Packaging setup for Concierge CLI.
See: https://click.palletsprojects.com/en/8.0.x/setuptools/
"""
from pathlib import Path
from setuptools import find_packages, setup

import concierge_cli as package


def read_file(filename):
    """Read a text file and return its contents."""
    project_home = Path(__file__).parent.resolve()
    file_path = project_home / filename
    return file_path.read_text(encoding="utf-8")


setup(
    name=package.__name__.replace('_', '-'),
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
    keywords=['cli', 'gitlab', 'maintenance'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    python_requires='>=3.6',
    install_requires=[
        'click',
        'python-gitlab',
    ],
    entry_points={
        'console_scripts': [
            'concierge-cli = concierge_cli.cli:main',
        ],
    },
)
