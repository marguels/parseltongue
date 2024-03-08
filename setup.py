from setuptools import setup
import __init__

with open('requirements.txt') as f:
    required = f.read().splitlines()
    

setup(
    name=__init__.__name__,
    author="marguels",
    packages=["app"],
    include_package_data=True,
    description="RAG-powered chat with Obsidian vault"
)