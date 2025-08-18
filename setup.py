"""
This setup.py is responsible for creating my machine learning application as a package that can be used
installed deployed in PyPi

"""
from setuptools import setup,find_packages


with open("requirements.txt") as f:
    requirements = [
        line.strip()
        for line in f
        if line.strip()
        and not line.startswith("#")
        and line.strip() != "-e ."
    ]

setup(
    name="python_project",                 
    version="0.1.0",                  
    author="Satwik Biswas",                 
    author_email="satwikcoder03@gmail.com",   
    packages=find_packages(),          
    install_requires= requirements,
    python_requires='>=3.8',  
)