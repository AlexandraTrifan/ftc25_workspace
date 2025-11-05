"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr
import pmt

class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Message Counter Decrease',   # will show up in GRC
            in_sig=[np.complex64],
            out_sig=[np.complex64]
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.message_port_register_in(pmt.intern('msg_count_in'))
        self.message_port_register_out(pmt.intern('msg_count'))
        self.set_msg_handler(pmt.intern('msg_count_in'), self.handle_msg)
        self.message_counter=0
        

    def handle_msg(self, msg):
        self.message_counter = pmt.to_python(msg)[1]


    def work(self, input_items, output_items):
        tags = self.get_tags_in_window(0, 0, len(input_items[0]),pmt.intern('packet_len'))
        #print(len(tags))
        if(len(tags)):            
            if(self.message_counter > len(tags)):
                self.message_counter-=len(tags)
            else:
                self.message_counter=0
            self.message_port_pub(pmt.intern('msg_count'), pmt.cons(pmt.PMT_NIL,pmt.from_long(self.message_counter)))
            #print(self.message_counter)
        output_items[0][:] = input_items[0]
        return len(output_items[0])
