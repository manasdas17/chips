CHIPS
=====

The Chips library allows hardware devices to be designed in python.

FEATURES
--------

- High level device modeling language makes device design simpler and more
  powerful.

- Provides fast native simulations that integrate with Python.

- Python extension modules such as Scipy, Numpy, Matplotlib and PIL provide a
  rich verification environment.

- Automatic generation of synthesizable VHDL.

- Plugin mechanism also allows C++ and graphviz outputs to be generated.

- Existing VHDL IP can be imported.

- Seamless co-simulation of C++ and VHDL outputs.

DOCUMENTATION
-------------
HTML documentation can be found in docs/_build/html

INSTALLATION
------------
>python setup install

TEST
----
>test_chips.py
>test_chips_VHDL.py
>test_chips_cpp.py
>test_chips_visual.py


EXAMPLES
--------
>cd examples

native simulation
>./example_xxxx.py simulate

ghdl simulation
>./example_xxxx.py simulate_ghdl

xilinx build
>./example_xxxx.py build

test
>./example_xxxx.py test

test
>./example_xxxx.py visualize

TO PREPARE A SOURCE DISTRIBUTION
--------------------------------
>python setup sdist
Distribution is contained in ./dist

TO CREATE A WINDOWS DISTRIBUTION
--------------------------------
>python setup bdist_wininst

GENERATE HTML DOCUMENTATION
---------------------------
>cd docs
>make html

