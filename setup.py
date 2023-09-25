from setuptools import setup, find_packages

setup(
    name="AoCHelpers",
    version="0.2017a4",
    packages=find_packages(),
    install_requires= [
        "requests",
        "bs4"
    ]
)