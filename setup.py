#!/usr/bin/env python

from distutils.core import setup

setup(name="PythonStreams",
      version="0.1",
      description="A library for designing hardware based on streams",
      author="Jon Dawson",
      author_email="jon@jondawson.org.uk",
      packages=["streams", "streams_VHDL", "streams_visual", "streams_cpp"],
      scripts=[
          "test_suite/test_streams.py",
          "test_suite/test_streams_VHDL.py",
          "test_suite/test_streams_visual.py",
      ],
      package_dir={
          "streams":"src/streams", 
          "streams_VHDL":"src/streams_VHDL", 
          "streams_visual":"src/streams_visual", 
          "streams_cpp":"src/streams_cpp", 
      },
)

