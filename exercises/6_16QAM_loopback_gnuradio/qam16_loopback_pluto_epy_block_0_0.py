"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr

class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self, window_size=100):
        gr.sync_block.__init__(
            self,
            name="EVM MAX",
            in_sig=[np.float32],
            out_sig=[np.float32]
        )
        self.window_size = window_size
        self.count = 0
        self.max_val = 0

    def work(self, input_items, output_items):
        in0 = input_items[0]
        out = output_items[0]

        
        for i in range(len(in0)):
            self.max_val = max(self.max_val, in0[i])
            self.count += 1
            out[i] = self.max_val
        
        if (self.count >= self.window_size):
            self.count = 0
            self.max_val = 0

        return len(output_items[0])
