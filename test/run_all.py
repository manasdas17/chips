#!/usr/bin/env python
"""run all chips tests"""

import subprocess

__author__ = "Jon Dawson"
__copyright__ = "Copyright 2010, Jonathan P Dawson"
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Jon Dawson"
__email__ = "chips@jondawson.org.uk"
__status__ = "Prototype"

subprocess.check_call(["./test_chips.py"]) 
subprocess.check_call(["./test_chips_cpp.py"]) 
subprocess.check_call(["./test_chips_VHDL.py"]) 
subprocess.check_call(["./test_chips_visual.py"]) 
subprocess.check_call(["./test_chips_ip.py"]) 
subprocess.check_call(["./tutorial_examples.py"]) 
