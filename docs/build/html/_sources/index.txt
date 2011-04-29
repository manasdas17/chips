=================================
Chips - Hardware Design in Python
=================================

What is Chips?
==============
Chips is a Python library that provides a language for designing hardware
devices.

Features
======== 
Some of the key features include:

- High level modeling language makes device design simpler and more
  powerful.

- An open source hardware design environment.

- Provides fast native simulations that integrate with Python.

- Exploit Python extension modules such as Scipy, Numpy, Matplotlib and PIL
  provide a rich verification environment.

- Automatic generation of synthesizable VHDL.

- Plugin mechanism also allows C++ and graphviz outputs to be generated.

- Existing VHDL IP can be imported.

- Seamless co-simulation of C++ and VHDL outputs.

A Quick Taster
==============

::

        >>> #4 bit linear feedback shift register

        >>> from chips import *

        >>> new_bit = Variable(0)
        >>> shift_register = Variable(1) #initialise to anything but 0
        >>> output_stream = Output()

        >>> Process(5,
        ...     Loop(
        ... 
        ...         #tap off bit 2 and 3 
        ...         new_bit.set((shift_register >> 0) ^ (shift_register >> 1) ^ new_bit),
        ... 
        ...         #implement shift register
        ...         shift_register.set(((new_bit & 1) << 3) | (shift_register >> 1)),
        ... 
        ...         #4 bit mask
        ...         shift_register.set(shift_register & 0xf),
        ... 
        ...         #write to stream
        ...         output_stream.write(shift_register)
        ...     )
        ... )
        Process(...

        >>> device = Chip(Console(Printer(output_stream)))
        >>> device.reset()
        >>> device.execute(1000)
        8
        12
        14
        7
        3
        1
        ...

Download
========
You can download the `source distribution`_ or the `windows  installer`_ from
the `GitHub`_ homepage.

.. _`GitHub`: http://github.com/dawsonjon/chips/

.. _`source distribution` : https://github.com/downloads/dawsonjon/chips/Chips-0.1.tar.gz

.. _`windows installer` : https://github.com/downloads/dawsonjon/chips/Chips-0.1.win32.exe

Documentation
=============
.. toctree::
   :maxdepth: 2

   introduction/index
   tutorial/index
   language_reference/index
   automatic_code_generation/index
   ip_library/index
   extending_chips/index

News
====

- 2011-04-09 Chips Library Published on GitHub.
- 2011-04-29 Chips Library Published on Python Package Index.

Links
=====

- `SciPy`_ Scientific Tools for Python.

- `matplotlib`_ 2D plotting library for Python.

- `Python Imaging Library (PIL)`_ Python Imaging Library adds image processing
  capabilities to Python.

- `MyHDL`_ A Hardware description language based on Python.

.. _`SciPy`: http://scipy.org
.. _`matplotlib`: http://matplotlib.sourceforge.net
.. _`MyHDL`: http://www.myhdl.org
.. _`Python Imaging Library (PIL)`: http://www.pythonware.com/products/pil/


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

