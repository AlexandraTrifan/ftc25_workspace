#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: console_message_transmitter_jupiter
# GNU Radio version: 3.10.4.0

from packaging.version import Version as StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import analog
from gnuradio import blocks
import pmt
from gnuradio import digital
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import gr, pdu
from gnuradio import iio
from gnuradio.qtgui import Range, GrRangeWidget
from PyQt5 import QtCore
import configparser
import console_message_transmitter_jupiter_epy_block_0 as epy_block_0  # embedded python block
import console_message_transmitter_jupiter_epy_block_2 as epy_block_2  # embedded python block
import math



from gnuradio import qtgui

class console_message_transmitter_jupiter(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "console_message_transmitter_jupiter", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("console_message_transmitter_jupiter")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "console_message_transmitter_jupiter")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Variables
        ##################################################
        self.center_freq = center_freq = 3200000000
        self.tx_lo_freq = tx_lo_freq = int(center_freq)
        self.sps = sps = 16
        self.samp_rate = samp_rate = 1920000
        self.offset_tx = offset_tx = int(160000)
        self.message_sent = message_sent = str("ANALOG DEVICES INC FTC2024")
        self._jupiter_ip_config = configparser.ConfigParser()
        self._jupiter_ip_config.read('default')
        try: jupiter_ip = self._jupiter_ip_config.get('main', 'key')
        except: jupiter_ip = 'ip:jupiter.local'
        self.jupiter_ip = jupiter_ip
        self.interval_update = interval_update = int(0)
        self.hardwaregain_tx0 = hardwaregain_tx0 = 0
        self.constellation = constellation = digital.constellation_calcdist([-1-1j, -1+1j, 1+1j, 1-1j], [0, 1, 2, 3],
        4, 1, digital.constellation.AMPLITUDE_NORMALIZATION).base()
        self.buff_size = buff_size = int(32768)
        self.alpha = alpha = 0.50

        ##################################################
        # Blocks
        ##################################################
        self._hardwaregain_tx0_range = Range(-41, 0, 1, 0, 200)
        self._hardwaregain_tx0_win = GrRangeWidget(self._hardwaregain_tx0_range, self.set_hardwaregain_tx0, "Tx Attenuation [dBfs]", "counter_slider", float, QtCore.Qt.Horizontal, "value")

        self.top_grid_layout.addWidget(self._hardwaregain_tx0_win, 5, 0, 1, 1)
        for r in range(5, 6):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_time_sink_x_0 = qtgui.time_sink_c(
            (96*16), #size
            samp_rate, #samp_rate
            'Transmitted Samples (After Constellation Modulator)', #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(-2, 2)

        self.qtgui_time_sink_x_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0.enable_tags(True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.5, 0, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0.enable_grid(True)
        self.qtgui_time_sink_x_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0.enable_stem_plot(False)


        labels = ['Re', 'Im', 'Tx Freq offset Re', 'Tx Freq offset Im', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(2):
            if len(labels[i]) == 0:
                if (i % 2 == 0):
                    self.qtgui_time_sink_x_0.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.qtgui_time_sink_x_0.set_line_label(i, "Im{{Data {0}}}".format(i/2))
            else:
                self.qtgui_time_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_time_sink_x_0_win, 1, 0, 1, 1)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
            8192, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            'Transmitted Spectrum', #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_0.set_update_time(1)
        self.qtgui_freq_sink_x_0.set_y_axis((-140), 10)
        self.qtgui_freq_sink_x_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_NORM, -40, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0.enable_grid(True)
        self.qtgui_freq_sink_x_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0.enable_control_panel(False)
        self.qtgui_freq_sink_x_0.set_fft_window_normalized(False)



        labels = ['Tx', 'Tx Spectrum + Freq Offset', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_freq_sink_x_0_win, 2, 0, 1, 1)
        for r in range(2, 3):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.pdu_pdu_to_tagged_stream_0 = pdu.pdu_to_tagged_stream(gr.types.byte_t, 'packet_len')
        self.iio_device_sink_0_1 = iio.device_sink(jupiter_ip, 'axi-adrv9002-tx-lpc', ['voltage0','voltage1'], 'adrv9002-phy', [], buff_size, 1 - 1, False)
        self.iio_device_sink_0_1.set_len_tag_key('')
        self.iio_attr_updater_0_1_0_0_0 = iio.attr_updater('frequency', str(tx_lo_freq), interval_update)
        self.iio_attr_updater_0_1 = iio.attr_updater('hardwaregain', str(hardwaregain_tx0), interval_update)
        self.iio_attr_sink_0_1_0_0_0 = iio.attr_sink(jupiter_ip, 'adrv9002-phy', 'altvoltage2', 0, True)
        self.iio_attr_sink_0_1 = iio.attr_sink(jupiter_ip, 'adrv9002-phy', 'voltage0', 0, True)
        self.epy_block_2 = epy_block_2.blk()
        self.epy_block_0 = epy_block_0.blk()
        self.digital_crc32_async_bb_1 = digital.crc32_async_bb(False)
        self.digital_constellation_modulator_0 = digital.generic_mod(
            constellation=constellation,
            differential=True,
            samples_per_symbol=sps,
            pre_diff_code=True,
            excess_bw=alpha,
            verbose=False,
            log=False,
            truncate=False)
        self.blocks_multiply_xx_0_0 = blocks.multiply_vcc(1)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_cc(0.6)
        self.blocks_message_strobe_0_0 = blocks.message_strobe(pmt.cons(pmt.PMT_NIL, pmt.init_u8vector(len(message_sent), list(message_sent.encode()))), 1)
        self.blocks_float_to_short_0_5_0 = blocks.float_to_short(1, 32768)
        self.blocks_float_to_short_0_0_4_0 = blocks.float_to_short(1, 32768)
        self.blocks_complex_to_real_0_4_0 = blocks.complex_to_real(1)
        self.blocks_complex_to_imag_0_4_0 = blocks.complex_to_imag(1)
        self.analog_sig_source_x_0_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, offset_tx, 1, 0, 0)


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.blocks_message_strobe_0_0, 'strobe'), (self.digital_crc32_async_bb_1, 'in'))
        self.msg_connect((self.digital_crc32_async_bb_1, 'out'), (self.epy_block_0, 'PDU_in'))
        self.msg_connect((self.epy_block_0, 'msg_count'), (self.epy_block_2, 'msg_count_in'))
        self.msg_connect((self.epy_block_0, 'PDU_out'), (self.pdu_pdu_to_tagged_stream_0, 'pdus'))
        self.msg_connect((self.epy_block_2, 'msg_count'), (self.epy_block_0, 'msg_count'))
        self.msg_connect((self.iio_attr_updater_0_1, 'out'), (self.iio_attr_sink_0_1, 'attr'))
        self.msg_connect((self.iio_attr_updater_0_1_0_0_0, 'out'), (self.iio_attr_sink_0_1_0_0_0, 'attr'))
        self.connect((self.analog_sig_source_x_0_0, 0), (self.blocks_multiply_xx_0_0, 1))
        self.connect((self.blocks_complex_to_imag_0_4_0, 0), (self.blocks_float_to_short_0_0_4_0, 0))
        self.connect((self.blocks_complex_to_real_0_4_0, 0), (self.blocks_float_to_short_0_5_0, 0))
        self.connect((self.blocks_float_to_short_0_0_4_0, 0), (self.iio_device_sink_0_1, 1))
        self.connect((self.blocks_float_to_short_0_5_0, 0), (self.iio_device_sink_0_1, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.epy_block_2, 0))
        self.connect((self.blocks_multiply_xx_0_0, 0), (self.blocks_complex_to_imag_0_4_0, 0))
        self.connect((self.blocks_multiply_xx_0_0, 0), (self.blocks_complex_to_real_0_4_0, 0))
        self.connect((self.blocks_multiply_xx_0_0, 0), (self.qtgui_freq_sink_x_0, 0))
        self.connect((self.digital_constellation_modulator_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.epy_block_2, 0), (self.blocks_multiply_xx_0_0, 0))
        self.connect((self.epy_block_2, 0), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.pdu_pdu_to_tagged_stream_0, 0), (self.digital_constellation_modulator_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "console_message_transmitter_jupiter")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_center_freq(self):
        return self.center_freq

    def set_center_freq(self, center_freq):
        self.center_freq = center_freq
        self.set_tx_lo_freq(int(self.center_freq))

    def get_tx_lo_freq(self):
        return self.tx_lo_freq

    def set_tx_lo_freq(self, tx_lo_freq):
        self.tx_lo_freq = tx_lo_freq
        self.iio_attr_updater_0_1_0_0_0.set_value(str(self.tx_lo_freq))

    def get_sps(self):
        return self.sps

    def set_sps(self, sps):
        self.sps = sps

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.analog_sig_source_x_0_0.set_sampling_freq(self.samp_rate)
        self.qtgui_freq_sink_x_0.set_frequency_range(0, self.samp_rate)
        self.qtgui_time_sink_x_0.set_samp_rate(self.samp_rate)

    def get_offset_tx(self):
        return self.offset_tx

    def set_offset_tx(self, offset_tx):
        self.offset_tx = offset_tx
        self.analog_sig_source_x_0_0.set_frequency(self.offset_tx)

    def get_message_sent(self):
        return self.message_sent

    def set_message_sent(self, message_sent):
        self.message_sent = message_sent
        self.blocks_message_strobe_0_0.set_msg(pmt.cons(pmt.PMT_NIL, pmt.init_u8vector(len(self.message_sent), list(message_sent.encode()))))

    def get_jupiter_ip(self):
        return self.jupiter_ip

    def set_jupiter_ip(self, jupiter_ip):
        self.jupiter_ip = jupiter_ip

    def get_interval_update(self):
        return self.interval_update

    def set_interval_update(self, interval_update):
        self.interval_update = interval_update

    def get_hardwaregain_tx0(self):
        return self.hardwaregain_tx0

    def set_hardwaregain_tx0(self, hardwaregain_tx0):
        self.hardwaregain_tx0 = hardwaregain_tx0
        self.iio_attr_updater_0_1.set_value(str(self.hardwaregain_tx0))

    def get_constellation(self):
        return self.constellation

    def set_constellation(self, constellation):
        self.constellation = constellation

    def get_buff_size(self):
        return self.buff_size

    def set_buff_size(self, buff_size):
        self.buff_size = buff_size

    def get_alpha(self):
        return self.alpha

    def set_alpha(self, alpha):
        self.alpha = alpha




def main(top_block_cls=console_message_transmitter_jupiter, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
