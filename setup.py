"""
Packaging setup for Concierge CLI.
See: https://click.palletsprojects.com/en/7.x/setuptools/
"""
from setuptools import setup

setup(
    name='concierge-cli',
    version='0.99.0.dev0',
    py_modules=['cli'],
    install_requires=[
        'Click',
    ],
    entry_points={
        'console_scripts': [
            'concierge-cli = cli:main',
        ],
    },
)
