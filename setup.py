#!/usr/bin/env python

from distutils.core import setup

setup(name="PythonStreams",
      version="0.1",
      description="A library for designing hardware based on streams",
      author="Jon Dawson",
      author_email="jon@jondawson.org.uk",
      packages=["streams", "streams_VHDL"],
)

