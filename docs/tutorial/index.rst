Tutorial
========

Learn Python
------------
In order to make any real use of the *Chips* library you will need to be
familiar with the basics of Python. The `python tutorial`_ is a good place to
start.

.. _`Python tutorial` : http://docs.python.org/tut

Install Chips
-------------

Windows
~~~~~~~

1. First `install python`_. You need Python 2.6 or later, but not Python 3.
2. Then install the chips library from the `windows installer`_.

Linux
~~~~~

1. First `install python`_. You need Python 2.6 or later, but not Python 3.
2. Then install the chips library from the `source distribution`_::

        desktop:~$ tar -zxf Chips-0.1.tar.gz
        desktop:~$ cd Chips-0.1
        desktop:~$ python setup.py install #run as root

.. _`install python` : http://python.org/download
.. _`source distribution` : http://github.com/dawsonjon/chips
.. _`windows installer` : http://github.com/dawsonjon/chips

First Simulations
-----------------

Once you have python and chips all set up, you can start with some simple
examples. This one counts to 10 repeatedly::

        from streams import *

        #create a chip model
        my_chip = Chip(
          Console(
            Printer(
                Counter(0, 10, 1),
            ),
          ),
        )

        #run a simulation
        my_chip.reset()
        my_chip.execute(100)

The example can be broken down as follows:

- ``from stream import *`` adds the basic features of the streams
  library to the local namespace.  

- A *Chip* models a target device. You need to tell it what the outputs
  (*sinks*) are, but it will work out what the inputs are by itself. In
  this case the only *sink* is the *Console*.

- A *Console* is a sink that outputs a stream of data to the console.
  The only argument it needs is the data stream, *Printer*.

- A *Printer* is a *stream* object that represents a stream of data in
  decimal format as a string of ASCII characters. A *Printer* is not a
  source of data in itself, it transforms a stream of data that you
  supply, the *Counter*.

- The *Counter* is a fundamental data stream. It accepts three
  arguments: start, stop and step. The *Counter* will yield a stream of
  data counting from *start* to *stop* in *step* increments.

Hello World
-----------

No language would be complete without a "hello world" example::

        from chips import *

        #convert string into a sequence of characters
        hello_world = tuple((ord(i) for i in "hello world\n"))

        my_chip = Chip(
            Console(
                Sequence(*hello_world),
            )
        )

        #run a simulation
        my_chip.reset()
        my_chip.execute(100)

In this example we have made only a few changes:

- ``hello_world = tuple((ord(i) for i in "hello world\n"))`` creates a tuple
  containing the numeric values of the ascii characters in a string.

- This example introduces a new stream, the *Sequence*. The *Sequence* stream
  outputs each of its arguments in turn, when the arguments are exhausted, the
  process repeats.
 
- A *Printer* is  *stream* is not needed in this example since the stream is
  allready a sequence of ascii values.

Generating VHDL
---------------

Now lets consider how the "hello world" example could be implemented in an
actual device. A first step to implementing a device would be to generate a
VHDL model::

        from chips import *
        from chips.VHDL_plugin import Plugin

        #convert string into a sequence of characters
        hello_world = tuple((ord(i) for i in "hello world\n"))

        my_chip = Chip(
            Console(
                Sequence(*hello_world),
            )
        )

        #generate a VHDL model
        code_generator = Plugin(project_name="hello world")
        my_chip.write_code(code_generator)

The *Chips* library uses plugins to generate output code from models. This
means that new code generators can be added to Chips without having to change
the way that hardware is designed and simulated. At present, chips supports C++
and VHDL code generation, but it is VHDL code that allows *Chips" to be
synthesised. 

The VHDL code generation plugin is found in ``chips.VHDL_plugin`` If you run
this example yo0u should find hello_world.vhd has been generated. You can run
this code in an external vhdl simulator, but you won't be able to synthesise it
into a device because real hardware devices don't have a concept of a
*Console*.

To make this example synthesise, we need to write the characters to some
realisable hardware interface. The *Chips* library provides a *SerialOut* sink,
this provides a simple way to direct the stream of characters to a serial port::

        from chips import *
        from chips.VHDL_plugin import Plugin

        #convert string into a sequence of characters
        hello_world = tuple((ord(i) for i in "hello world\n"))

        my_chip = Chip(
            SerialOut(
                Sequence(*hello_world),
            )
        )

        #generate a VHDL model
        code_generator = Plugin(project_name="hello world")
        my_chip.write_code(code_generator)

Now you should have a hello_world.vhd file that you can synthesise in a real
device. By default, SerialOut will assume that you are using a 50 MHz clock and
a baud rate of 115200. If you need something else you can use the clock_rate
and baud_rate arguments to specify what you need.

More Streams
------------
So far we have seen three types of streams, *Counter*, *Sequence* and
*Printer*. Chips provides a few more basic streams which you can read about in
the `Language Reference Manual`_. It is also possible to combine streams using
arithmetic operators : ``+, -, *, //, %, <<, >>, &, |, ^, ==, !=, <, <=, >,
>=`` on the whole they have the same (or very similar) meaning as they do in
Python except that they operate on streams of data.

        .. _`Language Reference Manual` : ../language_reference/index


Introducing Processes
---------------------

        

        





