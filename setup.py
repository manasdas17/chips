#!/usr/bin/env python

from distutils.core import setup

setup(name="PythonStreams",
      version="0.1",
      description="Design hardware with Python",
      author="Jon Dawson",
      author_email="chips@jondawson.org.uk",
      packages=[
          "chips", 
          "chips.ip", 
          "chips.cpp_plugin", 
          "chips.VHDL_plugin", 
          "chips.visual_plugin", 
      ],
      scripts=[
          "test_suite/test_chips.py",
          "test_suite/test_chips_cpp.py",
          "test_suite/test_chips_VHDL.py",
          "test_suite/test_chips_visual.py",
      ],
      package_data={
          "chips.ip":["*.vhd"], 
      },
)

