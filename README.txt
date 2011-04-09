TO PREPARE A SOURCE DISTRIBUTION
--------------------------------
>python setup sdist
Distribution is contained in ./dist

TO CREATE A WINDOWS DISTRIBUTION
--------------------------------
>python setup bdist_wininst

TO INSTALL
----------
>python setup install

TO TEST
-------
>test_streams.py
>test_streams_VHDL.py
>test_streams_visual.py

GENERATE VHDL DOCUMENTATION
---------------------------
>cd doc
>pdflatex python-streams.tex

GENERATE HTML DOCUMENTATION
---------------------------
>cd doc
>latex2html python-streams.tex

HTML DOCUMENTATION
------------------
html documentation can be found in doc/python_streams

PDF DOCUMENTATION
-----------------
pdf documentation can be found in doc

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
>./example_xxxx.py visulaize

