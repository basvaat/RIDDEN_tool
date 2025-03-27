import os, sys

from setuptools import setup, find_packages
from pathlib import Path

project_dir = Path(__file__).parent
long_description = (project_dir / "README.md").read_text()


setup(
    name='ridden',
    version='1.0',
    author='Szilvia Barsi',
    description="RIDDEN: Data-driven inference of receptor activity for cell-cell communication studies",
    long_description_content_type='text/markdown',
    long_description = long_description,

    url="https://github.com/basvaat/RIDDEN_tool",
    include_package_data=True,
    packages=find_packages(),
    package_data={
        'ridden_model': ['ridden_model_matrix.csv'],  
    },
    entry_points={
        'console_scripts': [
            'ridden-tool=ridden_tool.main:cli',
        ],
    },
    python_requires = '>=3.6',
    
    install_requires=[
        'pandas',
        'numpy'
    ]
)

