============
Introduction
============

The Chips library gives Python the ability to design, simulate and realiseV
digital devices such as FPGAs. Chips provides a simple yet powerful suite of
primitive components, *Streams*, *Processes* and *Sinks* that can be succinclty
combined to form *Chips*. The *Chips* library can automatically convert
*Streams*, *Processes* and *Sinks* into a Hardware Description Language, which
can be synthesised into real hardware. 

Python programs cannot themselves be converted into real hardware, but it is
possible to programaticaly generate which construct *Chips*, which can in-turn
be converted into hardware. When combined with the extensive libraries allready
supported by Python, such as NumPy and SciPy, Python and Chips make the ideal
design and verification environment.

A new approach to device design
-------------------------------

Traditionaly, the tool of choice for digital devices is a Hardware Description
Language (HDL), the most common being Verilog and VHDL. These languages provide
a reasonably rich environment for modeling and simulating hardware, but only a
limitied subset of the langauge can be realised in a digital device
(synthesised). 

A software designer would typically implement a function in an imperative style
using loops, branches and subprocedures, but hardware models written in an
imperative style cannot be synthesised.

Synthesisable designs require a different approach. Digital device designers
must work at the Register Transfer Level (RTL). The primitive elements of an
RTL design are clocked memory elements (registers) and combinational logic
elements. A typlical synthesis tool would be able to infer boolean logic,
addition, subtraction, multiplexing and bit manipulation from HDL code written
in a very specific style.

An RTL designer has to work at a low level of abstraction. In practical terms
this means that a designer has to do more of the work themselves.

	1. A designer is reponsible for designing their own interfaces to the
	outside world.

	2. The designer is responsible for clock to clock timing, manualy
	balancing propogation delays between clocked elements to achieve high
	performance.

	3. A designer has to provide their own mechanism to synchronise and
	pass data bwetween concurrent computational elements (by implementing a
	bus with control and handshaking signals).

	4. A designer has to provide their own mechanism to control the flow of
	execution within a computational element (usually by manually coding a
	finite state machine). 

	5. The primitive elements are primitive.


This is where *Python Chips* comes in. In *Python Chips*, there is no
synthesiseable subset, but a standalone synthesisable language built on top of
Python. *Python Chips* allows designers to work at a higher level of
abstraction. It does a lot more of the work for you.


	1. *Python Chips* provides a suite of device interfaces including portio,
	uart, usb and ethernet.

	2. Synthesisable RTL code is generated automatically by the tool. Clocks,
	resets, and clock to clock timing are all taken care of behind the scenes.

	3. *Python Chips* provides a simple method to synchronise concurrent
	elements, and to pass data between them - streams. The tool automatically
	generates interconnect busses and handshaking signals behind the scenes.

	4. *Python Chips* provides processes with imperative style sequeneces
	branches and loop. The tool automatically generates state machines, or highly
	optimized soft-core processors behind the scenes.

	6. The primitive elements are not so primitive. Common constructs such as
	counters, lookup tables, ROMS and RAMS are invoked with a single keyword and a
	few parameters. *Python Chips*. also provides a richer set of arithmetic
	operators including fully synthesiseable division and multiplication.

A language within a language
----------------------------

*Python Chips* is a python library, just an add-on to Python which is no more
or less than a programming language. The *Python Chips* library provides an
Application Programmers Interface (API) to a suite of hardware design
functions.

The *Python Chips* library can also be considered a language in its own right,
The Python language itself provides statements which are executed on your own
computer. The *Python Chips* provides an alternative language, statements which
are executed on the target device.
