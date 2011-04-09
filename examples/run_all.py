#!/usr/bin/env python
"""Run all simulations from chips examples"""

import subprocess


subprocess.check_call(["./example_1_hello_world.py", "simulate"]) 
subprocess.check_call(["./example_1_hello_world.py", "simulate_vhdl"]) 
subprocess.check_call(["./example_1_hello_world.py", "simulate_cpp"]) 
subprocess.check_call(["./example_1_hello_world.py", "visualize"]) 
subprocess.check_call(["./example_2_taylor_series.py", "simulate"]) 
subprocess.check_call(["./example_2_taylor_series.py", "simulate_vhdl"]) 
subprocess.check_call(["./example_2_taylor_series.py", "simulate_cpp"]) 
subprocess.check_call(["./example_2_taylor_series.py", "visualize"]) 
subprocess.check_call(["./example_4_fft.py", "simulate"]) 
subprocess.check_call(["./example_4_fft.py", "simulate_vhdl"]) 
subprocess.check_call(["./example_4_fft.py", "simulate_cpp"]) 
subprocess.check_call(["./example_4_fft.py", "visualize"]) 
subprocess.check_call(["./example_5_edge_detect.py", "python"]) 
subprocess.check_call(["./example_5_edge_detect.py", "simulate"]) 
subprocess.check_call(["./example_5_edge_detect.py", "simulate_vhdl"]) 
subprocess.check_call(["./example_5_edge_detect.py", "simulate_cpp"]) 
subprocess.check_call(["./example_5_edge_detect.py", "visualize"]) 
