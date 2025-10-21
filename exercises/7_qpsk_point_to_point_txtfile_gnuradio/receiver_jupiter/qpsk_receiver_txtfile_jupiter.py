#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: qpsk_receiver_txtfile_jupiter
# GNU Radio version: v3.10.11.0-1-gee27d6f3

from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio import analog
from gnuradio import blocks
from gnuradio import digital
from gnuradio import filter
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import iio
import configparser
import math
import sip
import threading



class qpsk_receiver_txtfile_jupiter(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "qpsk_receiver_txtfile_jupiter", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("qpsk_receiver_txtfile_jupiter")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except BaseException as exc:
            print(f"Qt GUI: Could not set Icon: {str(exc)}", file=sys.stderr)
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

        self.settings = Qt.QSettings("gnuradio/flowgraphs", "qpsk_receiver_txtfile_jupiter")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)
        self.flowgraph_started = threading.Event()

        ##################################################
        # Variables
        ##################################################
        self.sps = sps = 16
        self.samp_rate = samp_rate = 1920000
        self.nfilts = nfilts = 32
        self.center_freq = center_freq = 3200000000
        self.alpha = alpha = 0.50
        self.access_key = access_key = '11100001010110101110100010010011'
        self.rx_lo_freq = rx_lo_freq = int(center_freq)
        self.rcc_taps = rcc_taps = firdes.root_raised_cosine(nfilts, nfilts*samp_rate,samp_rate/sps, alpha, (11*sps*nfilts))
        self.offset_rx = offset_rx = -150000
        self._jupiter_ip_config = configparser.ConfigParser()
        self._jupiter_ip_config.read('default')
        try: jupiter_ip = self._jupiter_ip_config.get('main', 'key')
        except: jupiter_ip = 'ip:jupiter.local'
        self.jupiter_ip = jupiter_ip
        self.interval_update = interval_update = int(0)
        self.hdr_format = hdr_format = digital.header_format_default(access_key, 0)
        self.gain_control_mode_rx0 = gain_control_mode_rx0 = 'automatic'
        self.constellation = constellation = digital.constellation_calcdist([-1-1j, -1+1j, 1+1j, 1-1j], [0, 1, 2, 3],
        4, 1, digital.constellation.AMPLITUDE_NORMALIZATION).base()
        self.constellation.set_npwr(1.0)
        self.buff_size = buff_size = int(32768)

        ##################################################
        # Blocks
        ##################################################

        self.qtgui_time_sink_x_1_0 = qtgui.time_sink_c(
            1024, #size
            samp_rate, #samp_rate
            "Received Samples (After Costas Loop)", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_1_0.set_update_time(0.10)
        self.qtgui_time_sink_x_1_0.set_y_axis(-3, 3)

        self.qtgui_time_sink_x_1_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_1_0.enable_tags(True)
        self.qtgui_time_sink_x_1_0.set_trigger_mode(qtgui.TRIG_MODE_NORM, qtgui.TRIG_SLOPE_POS, 0.8, 0, 0, "")
        self.qtgui_time_sink_x_1_0.enable_autoscale(False)
        self.qtgui_time_sink_x_1_0.enable_grid(True)
        self.qtgui_time_sink_x_1_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_1_0.enable_control_panel(False)
        self.qtgui_time_sink_x_1_0.enable_stem_plot(False)


        labels = ['Re', 'Im', 'Signal 3', 'Signal 4', 'Signal 5',
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
                    self.qtgui_time_sink_x_1_0.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.qtgui_time_sink_x_1_0.set_line_label(i, "Im{{Data {0}}}".format(i/2))
            else:
                self.qtgui_time_sink_x_1_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_1_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_1_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_1_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_1_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_1_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_1_0_win = sip.wrapinstance(self.qtgui_time_sink_x_1_0.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_time_sink_x_1_0_win, 1, 1, 1, 1)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_freq_sink_x_0_0_0 = qtgui.freq_sink_c(
            8192, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            "Received spectrum", #name
            3,
            None # parent
        )
        self.qtgui_freq_sink_x_0_0_0.set_update_time(0.5)
        self.qtgui_freq_sink_x_0_0_0.set_y_axis((-140), 10)
        self.qtgui_freq_sink_x_0_0_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0_0_0.set_trigger_mode(qtgui.TRIG_MODE_NORM, -80, 2, "")
        self.qtgui_freq_sink_x_0_0_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0_0_0.enable_grid(True)
        self.qtgui_freq_sink_x_0_0_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0_0_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0_0_0.enable_control_panel(False)
        self.qtgui_freq_sink_x_0_0_0.set_fft_window_normalized(False)



        labels = ['Rx', 'Rx \n+ \nFreq Offset', 'Rx \n+ \nFreq \nOffset \n+ \nFLL', 'Rx+Freq Offset+FLL+RRC+SySync', 'Rx Spectrum+Freq Offset+FLL+RRC+SySync',
            '', '', '', '', '']
        widths = [1, 1, 1, 3, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "magenta", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(3):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0_0_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0_0_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0_0_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_0_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0_0_0.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_freq_sink_x_0_0_0_win, 2, 1, 1, 1)
        for r in range(2, 3):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_eye_sink_x_0_0 = qtgui.eye_sink_c(
            100, #size
            samp_rate, #samp_rate
            1, #number of inputs
            None
        )
        self.qtgui_eye_sink_x_0_0.set_update_time(0.10)
        self.qtgui_eye_sink_x_0_0.set_samp_per_symbol(1)
        self.qtgui_eye_sink_x_0_0.set_y_axis(-2, 2)

        self.qtgui_eye_sink_x_0_0.set_y_label('Amplitude', "")

        self.qtgui_eye_sink_x_0_0.enable_tags(True)
        self.qtgui_eye_sink_x_0_0.set_trigger_mode(qtgui.TRIG_MODE_NORM, qtgui.TRIG_SLOPE_POS, 0.3, 0, 0, "")
        self.qtgui_eye_sink_x_0_0.enable_autoscale(False)
        self.qtgui_eye_sink_x_0_0.enable_grid(True)
        self.qtgui_eye_sink_x_0_0.enable_axis_labels(True)
        self.qtgui_eye_sink_x_0_0.enable_control_panel(False)


        labels = ['Rx Re (After Costas Loop)', 'Rx Im (After Costas Loop)', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'blue', 'blue', 'blue', 'blue',
            'blue', 'blue', 'blue', 'blue', 'blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(2):
            if len(labels[i]) == 0:
                if (i % 2 == 0):
                    self.qtgui_eye_sink_x_0_0.set_line_label(i, "Eye [Re{{Data {0}}}]".format(round(i/2)))
                else:
                    self.qtgui_eye_sink_x_0_0.set_line_label(i, "Eye [Im{{Data {0}}}]".format(round((i-1)/2)))
            else:
                self.qtgui_eye_sink_x_0_0.set_line_label(i, labels[i])
            self.qtgui_eye_sink_x_0_0.set_line_width(i, widths[i])
            self.qtgui_eye_sink_x_0_0.set_line_color(i, colors[i])
            self.qtgui_eye_sink_x_0_0.set_line_style(i, styles[i])
            self.qtgui_eye_sink_x_0_0.set_line_marker(i, markers[i])
            self.qtgui_eye_sink_x_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_eye_sink_x_0_0_win = sip.wrapinstance(self.qtgui_eye_sink_x_0_0.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_eye_sink_x_0_0_win, 3, 1, 1, 1)
        for r in range(3, 4):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_const_sink_x_0_0 = qtgui.const_sink_c(
            int(1024), #size
            'Received Constellation', #name
            2, #number of inputs
            None # parent
        )
        self.qtgui_const_sink_x_0_0.set_update_time(0.10)
        self.qtgui_const_sink_x_0_0.set_y_axis((-2), 2)
        self.qtgui_const_sink_x_0_0.set_x_axis((-2), 2)
        self.qtgui_const_sink_x_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.5, 0, "")
        self.qtgui_const_sink_x_0_0.enable_autoscale(True)
        self.qtgui_const_sink_x_0_0.enable_grid(True)
        self.qtgui_const_sink_x_0_0.enable_axis_labels(True)


        labels = ['Rx Before \nCostas Loop', 'Rx After \nCostas Loop', 'Rx After Costas Loop', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        styles = [0, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        markers = [0, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(2):
            if len(labels[i]) == 0:
                self.qtgui_const_sink_x_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_const_sink_x_0_0.set_line_label(i, labels[i])
            self.qtgui_const_sink_x_0_0.set_line_width(i, widths[i])
            self.qtgui_const_sink_x_0_0.set_line_color(i, colors[i])
            self.qtgui_const_sink_x_0_0.set_line_style(i, styles[i])
            self.qtgui_const_sink_x_0_0.set_line_marker(i, markers[i])
            self.qtgui_const_sink_x_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_const_sink_x_0_0_win = sip.wrapinstance(self.qtgui_const_sink_x_0_0.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_const_sink_x_0_0_win, 3, 0, 1, 1)
        for r in range(3, 4):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.iio_device_source_0 = iio.device_source(jupiter_ip, 'axi-adrv9002-rx-lpc', ['voltage0_i','voltage0_q'], 'adrv9002-phy', [], buff_size, 1 - 1)
        self.iio_device_source_0.set_len_tag_key('packet_len')
        self.iio_attr_updater_0_1_0_1 = iio.attr_updater('gain_control_mode', gain_control_mode_rx0, interval_update)
        self.iio_attr_updater_0_1_0 = iio.attr_updater('frequency', str(rx_lo_freq), interval_update)
        self.iio_attr_updater_0_0_0 = iio.attr_updater('hardwaregain', str(-40), interval_update)
        self.iio_attr_updater_0_0 = iio.attr_updater('hardwaregain', str(0), interval_update)
        self.iio_attr_sink_0_1_0_1 = iio.attr_sink(jupiter_ip, 'adrv9002-phy', 'voltage0', 0, False)
        self.iio_attr_sink_0_1_0 = iio.attr_sink(jupiter_ip, 'adrv9002-phy', 'altvoltage0', 0, True)
        self.iio_attr_sink_0_0_0 = iio.attr_sink(jupiter_ip, 'adrv9002-phy', 'voltage1', 0, True)
        self.iio_attr_sink_0_0 = iio.attr_sink(jupiter_ip, 'adrv9002-phy', 'voltage1', 0, False)
        self.digital_symbol_sync_xx_0 = digital.symbol_sync_cc(
            digital.TED_SIGNAL_TIMES_SLOPE_ML,
            sps,
            0.045,
            1,
            1.0,
            1,
            1,
            constellation,
            digital.IR_PFB_MF,
            nfilts,
            rcc_taps)
        self.digital_fll_band_edge_cc_0 = digital.fll_band_edge_cc(sps, alpha, (sps*2+1), (2*math.pi/sps/100/sps))
        self.digital_diff_decoder_bb_0 = digital.diff_decoder_bb(constellation.arity(), digital.DIFF_DIFFERENTIAL)
        self.digital_crc32_bb_0_0 = digital.crc32_bb(True, "packet_len", True)
        self.digital_correlate_access_code_xx_ts_0_0 = digital.correlate_access_code_bb_ts(access_key,
          0, 'packet_len')
        self.digital_constellation_receiver_cb_0 = digital.constellation_receiver_cb(constellation, (2*math.pi*0.03), (-math.pi/2), (math.pi/2))
        self.blocks_unpack_k_bits_bb_0 = blocks.unpack_k_bits_bb(constellation.bits_per_symbol())
        self.blocks_skiphead_0 = blocks.skiphead(gr.sizeof_gr_complex*1, int(samp_rate))
        self.blocks_short_to_float_0_1 = blocks.short_to_float(1, 32767)
        self.blocks_short_to_float_0 = blocks.short_to_float(1, 32767)
        self.blocks_repack_bits_bb_1_0 = blocks.repack_bits_bb(1, 8, "packet_len", False, gr.GR_MSB_FIRST)
        self.blocks_null_sink_0_0_0 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_null_sink_0_0 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_null_sink_0 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_multiply_xx_0_0_0 = blocks.multiply_vcc(1)
        self.blocks_float_to_complex_0 = blocks.float_to_complex(1)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_char*1, '/home/analog/Desktop/ftc_2024/7_qpsk_point_to_point_txtfile_gnuradio/receiver_jupiter/received.txt', False)
        self.blocks_file_sink_0.set_unbuffered(True)
        self.analog_sig_source_x_0_0_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, offset_rx, 1, 0, 0)
        self.analog_agc_xx_0 = analog.agc_cc((1e-4), 1.0, 1.0, 65536)


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.iio_attr_updater_0_0, 'out'), (self.iio_attr_sink_0_0, 'attr'))
        self.msg_connect((self.iio_attr_updater_0_0_0, 'out'), (self.iio_attr_sink_0_0_0, 'attr'))
        self.msg_connect((self.iio_attr_updater_0_1_0, 'out'), (self.iio_attr_sink_0_1_0, 'attr'))
        self.msg_connect((self.iio_attr_updater_0_1_0_1, 'out'), (self.iio_attr_sink_0_1_0_1, 'attr'))
        self.connect((self.analog_agc_xx_0, 0), (self.digital_fll_band_edge_cc_0, 0))
        self.connect((self.analog_agc_xx_0, 0), (self.qtgui_freq_sink_x_0_0_0, 1))
        self.connect((self.analog_sig_source_x_0_0_0, 0), (self.blocks_multiply_xx_0_0_0, 1))
        self.connect((self.blocks_float_to_complex_0, 0), (self.blocks_multiply_xx_0_0_0, 0))
        self.connect((self.blocks_float_to_complex_0, 0), (self.qtgui_freq_sink_x_0_0_0, 0))
        self.connect((self.blocks_multiply_xx_0_0_0, 0), (self.analog_agc_xx_0, 0))
        self.connect((self.blocks_repack_bits_bb_1_0, 0), (self.digital_crc32_bb_0_0, 0))
        self.connect((self.blocks_short_to_float_0, 0), (self.blocks_float_to_complex_0, 0))
        self.connect((self.blocks_short_to_float_0_1, 0), (self.blocks_float_to_complex_0, 1))
        self.connect((self.blocks_skiphead_0, 0), (self.digital_symbol_sync_xx_0, 0))
        self.connect((self.blocks_unpack_k_bits_bb_0, 0), (self.digital_correlate_access_code_xx_ts_0_0, 0))
        self.connect((self.digital_constellation_receiver_cb_0, 3), (self.blocks_null_sink_0, 0))
        self.connect((self.digital_constellation_receiver_cb_0, 2), (self.blocks_null_sink_0_0, 0))
        self.connect((self.digital_constellation_receiver_cb_0, 1), (self.blocks_null_sink_0_0_0, 0))
        self.connect((self.digital_constellation_receiver_cb_0, 0), (self.digital_diff_decoder_bb_0, 0))
        self.connect((self.digital_constellation_receiver_cb_0, 4), (self.qtgui_const_sink_x_0_0, 1))
        self.connect((self.digital_constellation_receiver_cb_0, 4), (self.qtgui_eye_sink_x_0_0, 0))
        self.connect((self.digital_constellation_receiver_cb_0, 4), (self.qtgui_time_sink_x_1_0, 0))
        self.connect((self.digital_correlate_access_code_xx_ts_0_0, 0), (self.blocks_repack_bits_bb_1_0, 0))
        self.connect((self.digital_crc32_bb_0_0, 0), (self.blocks_file_sink_0, 0))
        self.connect((self.digital_diff_decoder_bb_0, 0), (self.blocks_unpack_k_bits_bb_0, 0))
        self.connect((self.digital_fll_band_edge_cc_0, 0), (self.blocks_skiphead_0, 0))
        self.connect((self.digital_fll_band_edge_cc_0, 0), (self.qtgui_freq_sink_x_0_0_0, 2))
        self.connect((self.digital_symbol_sync_xx_0, 0), (self.digital_constellation_receiver_cb_0, 0))
        self.connect((self.digital_symbol_sync_xx_0, 0), (self.qtgui_const_sink_x_0_0, 0))
        self.connect((self.iio_device_source_0, 0), (self.blocks_short_to_float_0, 0))
        self.connect((self.iio_device_source_0, 1), (self.blocks_short_to_float_0_1, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("gnuradio/flowgraphs", "qpsk_receiver_txtfile_jupiter")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_sps(self):
        return self.sps

    def set_sps(self, sps):
        self.sps = sps
        self.set_rcc_taps(firdes.root_raised_cosine(self.nfilts, self.nfilts*self.samp_rate, self.samp_rate/self.sps, self.alpha, (11*self.sps*self.nfilts)))
        self.digital_fll_band_edge_cc_0.set_loop_bandwidth((2*math.pi/self.sps/100/self.sps))
        self.digital_symbol_sync_xx_0.set_sps(self.sps)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_rcc_taps(firdes.root_raised_cosine(self.nfilts, self.nfilts*self.samp_rate, self.samp_rate/self.sps, self.alpha, (11*self.sps*self.nfilts)))
        self.analog_sig_source_x_0_0_0.set_sampling_freq(self.samp_rate)
        self.qtgui_eye_sink_x_0_0.set_samp_rate(self.samp_rate)
        self.qtgui_freq_sink_x_0_0_0.set_frequency_range(0, self.samp_rate)
        self.qtgui_time_sink_x_1_0.set_samp_rate(self.samp_rate)

    def get_nfilts(self):
        return self.nfilts

    def set_nfilts(self, nfilts):
        self.nfilts = nfilts
        self.set_rcc_taps(firdes.root_raised_cosine(self.nfilts, self.nfilts*self.samp_rate, self.samp_rate/self.sps, self.alpha, (11*self.sps*self.nfilts)))

    def get_center_freq(self):
        return self.center_freq

    def set_center_freq(self, center_freq):
        self.center_freq = center_freq
        self.set_rx_lo_freq(int(self.center_freq))

    def get_alpha(self):
        return self.alpha

    def set_alpha(self, alpha):
        self.alpha = alpha
        self.set_rcc_taps(firdes.root_raised_cosine(self.nfilts, self.nfilts*self.samp_rate, self.samp_rate/self.sps, self.alpha, (11*self.sps*self.nfilts)))

    def get_access_key(self):
        return self.access_key

    def set_access_key(self, access_key):
        self.access_key = access_key
        self.set_hdr_format(digital.header_format_default(self.access_key, 0))

    def get_rx_lo_freq(self):
        return self.rx_lo_freq

    def set_rx_lo_freq(self, rx_lo_freq):
        self.rx_lo_freq = rx_lo_freq
        self.iio_attr_updater_0_1_0.set_value(str(self.rx_lo_freq))

    def get_rcc_taps(self):
        return self.rcc_taps

    def set_rcc_taps(self, rcc_taps):
        self.rcc_taps = rcc_taps

    def get_offset_rx(self):
        return self.offset_rx

    def set_offset_rx(self, offset_rx):
        self.offset_rx = offset_rx
        self.analog_sig_source_x_0_0_0.set_frequency(self.offset_rx)

    def get_jupiter_ip(self):
        return self.jupiter_ip

    def set_jupiter_ip(self, jupiter_ip):
        self.jupiter_ip = jupiter_ip

    def get_interval_update(self):
        return self.interval_update

    def set_interval_update(self, interval_update):
        self.interval_update = interval_update

    def get_hdr_format(self):
        return self.hdr_format

    def set_hdr_format(self, hdr_format):
        self.hdr_format = hdr_format

    def get_gain_control_mode_rx0(self):
        return self.gain_control_mode_rx0

    def set_gain_control_mode_rx0(self, gain_control_mode_rx0):
        self.gain_control_mode_rx0 = gain_control_mode_rx0
        self.iio_attr_updater_0_1_0_1.set_value(self.gain_control_mode_rx0)

    def get_constellation(self):
        return self.constellation

    def set_constellation(self, constellation):
        self.constellation = constellation

    def get_buff_size(self):
        return self.buff_size

    def set_buff_size(self, buff_size):
        self.buff_size = buff_size




def main(top_block_cls=qpsk_receiver_txtfile_jupiter, options=None):

    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()
    tb.flowgraph_started.set()

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
