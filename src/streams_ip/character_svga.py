#!/usr/bin/env python
"""Provide a wrapper for a character SVGA interface implemented in VHDL"""

import os
import sys

from streams import *

dirname = os.path.dirname(__file__)
svgaipinterface = ExternalIPDefinition(
        name="CHARACTER_SVGA", 
        dependencies={
            "VHDL":[
                os.path.join(dirname, "character_svga.vhd"),
            ],
        },
        input_streams={
            'DATA':8
        },
        output_streams={
        },
        input_ports={
        },
        output_ports={
            'R':1,
            'G':1,
            'B':1,
            'VSYNCH':1,
            'HSYNCH':1,
        }
)

def CharacterSVGA(stream, r="R", g='G', b='B', hsynch='HSYNCH', vsynch='VSYNCH'):
    external_ip_interface = ExternalIPInstance(
            definition=svgaipinterface,
            input_streams=[
                stream,
            ],
            inport_mapping={
            },
            outport_mapping={
                'R':r,
                'G':g,
                'B':b,
                'HSYNCH':hsynch,
                'VSYNCH':vsynch,
            },
    )
    return external_ip_interface

if __name__ == "__main__":        

    if "build" in sys.argv:
        from streams_VHDL import Plugin
        system = System(CharacterSVGA(Resizer(Sequence(0, 0, ord("#")), 8)))
        plugin = Plugin()
        system.write_code(plugin)
        plugin.ghdl_test("test svga", stop_cycles=100)

    if "visualise" in sys.argv:
        from streams_visual import Plugin
        system = System(Console(PS2Keyboard()))
        plugin = Plugin()
        system.write_code(plugin)
        plugin.draw("SVGA.svg")
