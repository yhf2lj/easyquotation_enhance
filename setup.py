# coding:utf8
from os import path

from setuptools import setup

# read the contents of your README file
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="easyquotation_enhance",
    version="0.0.0.6",
    description="A utility for Fetch China Stock Info",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="demon finch",
    author_email="yhf2lj@outlook.com",
    license="MIT",
    url="https://github.com/yhf2lj/easyquotation_enhance",
    keywords="China stock trade download",
    install_requires=["requests", "easyquotation", "SQLAlchemy", "func_timeout"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3.5",
    ],
    packages=["easyquotation_enhance"],
)
