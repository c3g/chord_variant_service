#!/usr/bin/env python

import configparser
import os
import setuptools

with open("README.md", "r") as rf:
    long_description = rf.read()

config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(os.path.realpath(__file__)), "chord_variant_service", "package.cfg"))

setuptools.setup(
    name="chord_variant_service",
    version="0.1.0",

    python_requires=">=3.6",
    install_requires=[
        "chord_lib[flask]==0.7.0",
        "Flask>=1.1,<2.0",
        "jsonschema>=3.2,<4.0",
        "pysam>=0.15.4,<0.16",
        "requests>=2.23,<3.0",
        "requests_unixsocket>=0.2.0,<0.3.0",
    ],

    author="David Lougheed",
    author_email="david.lougheed@mail.mcgill.ca",

    description="An implementation of a variant store for the CHORD project.",
    long_description=long_description,
    long_description_content_type="text/markdown",

    packages=setuptools.find_packages(),
    include_package_data=True,

    url="https://github.com/c3g/chord_variant_service",
    license="LGPLv3",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent"
    ]
)
