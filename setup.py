#!/usr/bin/env python

from distutils.core import setup

setup(name="PythonStreams",
      version="0.1",
      description="Design hardware with Python",
      long_description="""\
    
Chips
-----

The Chips library allows hardware devces to be designed in python

Features

- High level device modeling language makes device design simpler and more powerful.

- Provides fast native simulations that integrate with Python.

- Python extension modules such asch as Scipy, Numpy, Matplotlib and PIL provide a rich
  verification environment.

- Automatic generation of synthesisable VHDL.

- Plugin mechanism also allows C++ and graphviz outputs to be generated.

- Existing VHDL IP can be imported.

- Seamless co-simulation of C++ and VHDL outputs.

""",
        
      author="Jon Dawson",
      author_email="chips@jondawson.org.uk",
      url="http://github.com/dawsonjon/chips",
      keywords=["VHDL", "FPGA", "hardware design", "simulation"],
      classifiers = [
          "Programming Language :: Python",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
          "Intended Audience :: Science/Research",
          "Intended Audience :: Developers",
          "Development Status :: 3 - Alpha",
          "Topic :: Scientific/Engineering :: Electronic Design Automation (EDA)",
          "Topic :: Software Development :: Embedded Systems",
          "Topic :: Software Development :: Code Generators",
      ],
      packages=[
          "chips", 
          "chips.ip", 
          "chips.cpp_plugin", 
          "chips.VHDL_plugin", 
          "chips.visual_plugin", 
      ],
)

