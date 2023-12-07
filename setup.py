from setuptools import setup, find_packages

setup(
    name="AoCHelpers",
    version="0.2023a",
    packages=find_packages(),
    install_requires= [
        "requests",
        "bs4"
    ]
)