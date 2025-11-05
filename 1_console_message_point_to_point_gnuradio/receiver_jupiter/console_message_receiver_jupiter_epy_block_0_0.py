"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr

dataBuf = []

class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    def __init__(self):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='ASCII Conversion Python Block',   # will show up in GRC
            in_sig=None,
            out_sig=None
        )
        self.message_port_register_in(gr.pmt.intern('msg_in'))
        self.message_port_register_out(gr.pmt.intern('clear_input'))
        self.set_msg_handler(gr.pmt.intern('msg_in'), self.handle_msg)
    
    def handle_msg(self, msg):
        global dataBuf
        dataBuf = gr.pmt.to_python(gr.pmt.cdr(msg)) # this one returns a python list
        proc=[str(chr(x)) for x in dataBuf]
        final_msg = "".join(proc)
        self.message_port_pub(gr.pmt.intern('clear_input'), gr.pmt.cons(gr.pmt.PMT_NIL, gr.pmt.to_pmt(final_msg)))

