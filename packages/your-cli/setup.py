"""
Setup script for the CLI package.
"""

from setuptools import setup, find_packages

setup(
    name="your-cli",
    version="0.1.0",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "your-cli=your_cli.main:main",
        ],
    },
) 