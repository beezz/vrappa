# -*- coding: utf-8 -*-
# vim:fenc=utf-8


from setuptools import setup


# with open("README.rst") as f:
#     description = f.read()

setup(
    version="1.0.6",
    name="vrappa",
    description=(
        "Simple wrapper (decorator factory) with hooks for preparing arguments"
        " catching exceptions and acting on them."
    ),
    # long_description=description,
    long_description="Will be",
    author="Michal Kuffa",
    author_email="michal.kuffa@gmail.com",
    py_modules=["vrappa"],
    license="BSD",
    url="https://github.com/beezz/vrappa",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Topic :: Software Development",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
    ]
)
