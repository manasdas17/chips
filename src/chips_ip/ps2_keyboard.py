#!/usr/bin/env python
"""Provide a wrapper for a PS/2 keyboard interface implemented in VHDL"""

import os
import sys

from chips import *

dirname = os.path.dirname(__file__)
keyboardipinterface = ExternalIPDefinition(
        name="PS2_KEYBOARD", 
        dependencies={
            "VHDL":[
                os.path.join(dirname, "ps2_kb.vhd"),
            ],
        },
        input_streams={
        },
        output_streams={
            'DATA':8
        },
        input_ports={
            'KC':1,
            'KD':1
        },
        output_ports={
        }
)

def PS2Keyboard(keyboard_clock="KC", keyboard_data="KD"):
    external_ip_interface = ExternalIPInstance(
            definition=keyboardipinterface,
            input_streams=(),
            inport_mapping={
                'KC':keyboard_clock,
                'KD':keyboard_data,
            },
            outport_mapping={},
    )
    return external_ip_interface.get_output_streams()[0]

if __name__ == "__main__":        

    if "build" in sys.argv:
        from streams_VHDL import Plugin
        system = System(Console(PS2Keyboard()))
        plugin = Plugin()
        system.write_code(plugin)
        plugin.ghdl_test("test keyboard", stop_cycles=100)

    if "visualise" in sys.argv:
        from streams_visual import Plugin
        system = System(Console(PS2Keyboard()))
        plugin = Plugin()
        system.write_code(plugin)
        plugin.draw("keyboard.svg")
