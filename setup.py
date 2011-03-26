#!/usr/bin/env python

from distutils.core import setup

setup(name="PythonStreams",
      version="0.1",
      description="A library for designing hardware based on chips",
      author="Jon Dawson",
      author_email="jon@jondawson.org.uk",
      packages=[
          "chips", 
          "chips_VHDL", 
          "chips_visual", 
          "chips_cpp",
          "chips_ip"
      ],
      scripts=[
          "test_suite/test_chips.py",
          "test_suite/test_chips_cpp.py",
          "test_suite/test_chips_VHDL.py",
          "test_suite/test_chips_visual.py",
      ],
      package_dir={
          "chips":"src/chips", 
          "chips_VHDL":"src/chips_VHDL", 
          "chips_visual":"src/chips_visual", 
          "chips_cpp":"src/chips_cpp", 
          "chips_ip":"src/chips_ip", 
      },
      package_data={
          "chips_ip":["*.vhd"], 
      },
)

