"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr
from collections import deque

class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self, window_size=100):
        gr.sync_block.__init__(
            self,
            name="EVM RMS",
            in_sig=[np.float32],
            out_sig=[np.float32]
        )
        self.window_size = window_size
        self.buffer = deque(maxlen=window_size)
        self.sum_squares = 0.0

    def work(self, input_items, output_items):
        in0 = input_items[0]
        out = output_items[0]

        for i, val in enumerate(in0):
            squared = val ** 2
            if len(self.buffer) == self.window_size:
                removed = self.buffer.popleft()
                self.sum_squares -= removed
            self.buffer.append(squared)
            self.sum_squares += squared

            rms = np.sqrt(self.sum_squares / len(self.buffer))
            out[i] = rms

        return len(out)

