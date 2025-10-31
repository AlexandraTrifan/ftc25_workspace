#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
# GNU Radio version: v3.10.11.0-1-gee27d6f3

from PyQt5 import Qt
from gnuradio import qtgui
from PyQt5 import QtCore
from gnuradio import analog
from gnuradio import blocks
from gnuradio import digital
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
import sip
import threading



class QPSK_raw_loopback_jupiter(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Not titled yet", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Not titled yet")
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

        self.settings = Qt.QSettings("gnuradio/flowgraphs", "QPSK_raw_loopback_jupiter")

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
        self.lo_tx_offset = lo_tx_offset = int(0)
        self.tx_lo_freq = tx_lo_freq = int(2200000000 + lo_tx_offset)
        self.sps = sps = 100
        self.samp_rate = samp_rate = 1920000
        self.rx_lo_freq = rx_lo_freq = int(2200000000)
        self.offset_tx = offset_tx = 250000
        self.offset_rx = offset_rx = -250000
        self._jupiter_ip_config = configparser.ConfigParser()
        self._jupiter_ip_config.read('default')
        try: jupiter_ip = self._jupiter_ip_config.get('main', 'key')
        except: jupiter_ip = 'ip:jupiter.local'
        self.jupiter_ip = jupiter_ip
        self.interval_update = interval_update = int(0)
        self.hardwaregain_tx0 = hardwaregain_tx0 = 0
        self.hardwaregain_rx0 = hardwaregain_rx0 = 20
        self.gain_control_mode_rx0 = gain_control_mode_rx0 = 'spi'
        self.buff_size = buff_size = int(32768)

        ##################################################
        # Blocks
        ##################################################

        self._offset_rx_range = qtgui.Range(-1000000, 1000000, 1, -250000, 200)
        self._offset_rx_win = qtgui.RangeWidget(self._offset_rx_range, self.set_offset_rx, "'offset_rx'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._offset_rx_win, 2, 0, 1, 2)
        for r in range(2, 3):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._hardwaregain_tx0_range = qtgui.Range(-41, 0, 1, 0, 200)
        self._hardwaregain_tx0_win = qtgui.RangeWidget(self._hardwaregain_tx0_range, self.set_hardwaregain_tx0, "Tx Attenuation [dBfs]", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._hardwaregain_tx0_win)
        self._hardwaregain_rx0_range = qtgui.Range(0, 34, 1, 20, 200)
        self._hardwaregain_rx0_win = qtgui.RangeWidget(self._hardwaregain_rx0_range, self.set_hardwaregain_rx0, "Rx Gain [dBfs]", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._hardwaregain_rx0_win)
        self.qtgui_time_sink_x_1 = qtgui.time_sink_c(
            (1024*3), #size
            samp_rate, #samp_rate
            "Received Samples Raw", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_1.set_update_time(0.10)
        self.qtgui_time_sink_x_1.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_1.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_1.enable_tags(True)
        self.qtgui_time_sink_x_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_1.enable_autoscale(False)
        self.qtgui_time_sink_x_1.enable_grid(True)
        self.qtgui_time_sink_x_1.enable_axis_labels(True)
        self.qtgui_time_sink_x_1.enable_control_panel(False)
        self.qtgui_time_sink_x_1.enable_stem_plot(False)


        labels = ['Rx Samples Raw Re', 'Rx Samples Raw Im', 'Signal 3', 'Signal 4', 'Signal 5',
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
                    self.qtgui_time_sink_x_1.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.qtgui_time_sink_x_1.set_line_label(i, "Im{{Data {0}}}".format(i/2))
            else:
                self.qtgui_time_sink_x_1.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_1.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_1.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_1.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_1.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_1.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_1_win = sip.wrapinstance(self.qtgui_time_sink_x_1.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_time_sink_x_1_win, 1, 0, 1, 1)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_time_sink_x_0 = qtgui.time_sink_c(
            (1024*3), #size
            samp_rate, #samp_rate
            "Transmitted samples", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0.enable_tags(True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0.enable_grid(True)
        self.qtgui_time_sink_x_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0.enable_stem_plot(False)


        labels = ['Tx Samples Re', 'Tx Samples Im', 'Signal 3', 'Signal 4', 'Signal 5',
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
        self.top_grid_layout.addWidget(self._qtgui_time_sink_x_0_win, 0, 0, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_freq_sink_x_0_0 = qtgui.freq_sink_c(
            8192, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            "Transmitted Spectrum", #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_0_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0_0.set_y_axis((-140), 10)
        self.qtgui_freq_sink_x_0_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0_0.enable_grid(True)
        self.qtgui_freq_sink_x_0_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0_0.enable_control_panel(False)
        self.qtgui_freq_sink_x_0_0.set_fft_window_normalized(False)



        labels = ['Tx Spectrum', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0_0.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_freq_sink_x_0_0_win, 0, 1, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
            8192, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            "Received spectrum", #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0.set_y_axis((-140), 10)
        self.qtgui_freq_sink_x_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0.enable_grid(True)
        self.qtgui_freq_sink_x_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0.enable_control_panel(False)
        self.qtgui_freq_sink_x_0.set_fft_window_normalized(False)



        labels = ['Rx Spectrum Raw', '', '', '', '',
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
        self.top_grid_layout.addWidget(self._qtgui_freq_sink_x_0_win, 1, 1, 1, 1)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_const_sink_x_0 = qtgui.const_sink_c(
            1024, #size
            "Received constellation", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_const_sink_x_0.set_update_time(0.50)
        self.qtgui_const_sink_x_0.set_y_axis((-2), 2)
        self.qtgui_const_sink_x_0.set_x_axis((-2), 2)
        self.qtgui_const_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, "")
        self.qtgui_const_sink_x_0.enable_autoscale(False)
        self.qtgui_const_sink_x_0.enable_grid(True)
        self.qtgui_const_sink_x_0.enable_axis_labels(True)


        labels = ['Rx Constellation', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "red", "red", "red",
            "red", "red", "red", "red", "red"]
        styles = [0, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        markers = [0, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_const_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_const_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_const_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_const_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_const_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_const_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_const_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_const_sink_x_0_win = sip.wrapinstance(self.qtgui_const_sink_x_0.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_const_sink_x_0_win, 3, 0, 1, 1)
        for r in range(3, 4):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.iio_device_source_0 = iio.device_source(jupiter_ip, 'axi-adrv9002-rx-lpc', ['voltage0_i','voltage0_q'], 'adrv9002-phy', [], buff_size, 1 - 1)
        self.iio_device_source_0.set_len_tag_key('packet_len')
        self.iio_device_sink_0_1 = iio.device_sink(jupiter_ip, 'axi-adrv9002-tx-lpc', ['voltage0','voltage1'], 'adrv9002-phy', [], buff_size, 1 - 1, False)
        self.iio_device_sink_0_1.set_len_tag_key('')
        self.iio_attr_updater_0_1_0_1 = iio.attr_updater('gain_control_mode', gain_control_mode_rx0, interval_update)
        self.iio_attr_updater_0_1_0_0 = iio.attr_updater('frequency', str(tx_lo_freq), interval_update)
        self.iio_attr_updater_0_1_0 = iio.attr_updater('frequency', str(rx_lo_freq), interval_update)
        self.iio_attr_updater_0_1 = iio.attr_updater('hardwaregain', str(hardwaregain_tx0), interval_update)
        self.iio_attr_updater_0_0_0 = iio.attr_updater('hardwaregain', str(-40), interval_update)
        self.iio_attr_updater_0_0 = iio.attr_updater('hardwaregain', str(0), interval_update)
        self.iio_attr_updater_0 = iio.attr_updater('hardwaregain', str(hardwaregain_rx0), interval_update)
        self.iio_attr_sink_0_1_0_1 = iio.attr_sink(jupiter_ip, 'adrv9002-phy', 'voltage0', 0, False)
        self.iio_attr_sink_0_1_0_0 = iio.attr_sink(jupiter_ip, 'adrv9002-phy', 'altvoltage2', 0, True)
        self.iio_attr_sink_0_1_0 = iio.attr_sink(jupiter_ip, 'adrv9002-phy', 'altvoltage0', 0, True)
        self.iio_attr_sink_0_1 = iio.attr_sink(jupiter_ip, 'adrv9002-phy', 'voltage0', 0, True)
        self.iio_attr_sink_0_0_0 = iio.attr_sink(jupiter_ip, 'adrv9002-phy', 'voltage1', 0, True)
        self.iio_attr_sink_0_0 = iio.attr_sink(jupiter_ip, 'adrv9002-phy', 'voltage1', 0, False)
        self.iio_attr_sink_0 = iio.attr_sink(jupiter_ip, 'adrv9002-phy', 'voltage0', 0, False)
        self.digital_chunks_to_symbols_xx_0 = digital.chunks_to_symbols_bc((-1 -1j,-1+1j, +1+1j,+1-1j), 1)
        self.blocks_vector_source_x_0 = blocks.vector_source_b((2,2,3,1,3,1,0,2,0), True, 1, [])
        self.blocks_short_to_float_0_1 = blocks.short_to_float(1, 32767)
        self.blocks_short_to_float_0 = blocks.short_to_float(1, 32767)
        self.blocks_repeat_0 = blocks.repeat(gr.sizeof_gr_complex*1, sps)
        self.blocks_multiply_xx_0_0 = blocks.multiply_vcc(1)
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
        self.blocks_float_to_short_0_5_0 = blocks.float_to_short(1, 32767)
        self.blocks_float_to_short_0_0_4_0 = blocks.float_to_short(1, 32767)
        self.blocks_float_to_complex_0 = blocks.float_to_complex(1)
        self.blocks_complex_to_real_0_4_0 = blocks.complex_to_real(1)
        self.blocks_complex_to_imag_0_4_0 = blocks.complex_to_imag(1)
        self.analog_sig_source_x_0_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, offset_rx, 1, 0, 0)
        self.analog_sig_source_x_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, offset_tx, 1, 0, 0)


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.iio_attr_updater_0, 'out'), (self.iio_attr_sink_0, 'attr'))
        self.msg_connect((self.iio_attr_updater_0_0, 'out'), (self.iio_attr_sink_0_0, 'attr'))
        self.msg_connect((self.iio_attr_updater_0_0_0, 'out'), (self.iio_attr_sink_0_0_0, 'attr'))
        self.msg_connect((self.iio_attr_updater_0_1, 'out'), (self.iio_attr_sink_0_1, 'attr'))
        self.msg_connect((self.iio_attr_updater_0_1_0, 'out'), (self.iio_attr_sink_0_1_0, 'attr'))
        self.msg_connect((self.iio_attr_updater_0_1_0_0, 'out'), (self.iio_attr_sink_0_1_0_0, 'attr'))
        self.msg_connect((self.iio_attr_updater_0_1_0_1, 'out'), (self.iio_attr_sink_0_1_0_1, 'attr'))
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.analog_sig_source_x_0_0, 0), (self.blocks_multiply_xx_0_0, 1))
        self.connect((self.blocks_complex_to_imag_0_4_0, 0), (self.blocks_float_to_short_0_0_4_0, 0))
        self.connect((self.blocks_complex_to_real_0_4_0, 0), (self.blocks_float_to_short_0_5_0, 0))
        self.connect((self.blocks_float_to_complex_0, 0), (self.blocks_multiply_xx_0_0, 0))
        self.connect((self.blocks_float_to_short_0_0_4_0, 0), (self.iio_device_sink_0_1, 1))
        self.connect((self.blocks_float_to_short_0_5_0, 0), (self.iio_device_sink_0_1, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.blocks_complex_to_imag_0_4_0, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.blocks_complex_to_real_0_4_0, 0))
        self.connect((self.blocks_multiply_xx_0_0, 0), (self.qtgui_const_sink_x_0, 0))
        self.connect((self.blocks_multiply_xx_0_0, 0), (self.qtgui_freq_sink_x_0, 0))
        self.connect((self.blocks_multiply_xx_0_0, 0), (self.qtgui_time_sink_x_1, 0))
        self.connect((self.blocks_repeat_0, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.blocks_repeat_0, 0), (self.qtgui_freq_sink_x_0_0, 0))
        self.connect((self.blocks_repeat_0, 0), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.blocks_short_to_float_0, 0), (self.blocks_float_to_complex_0, 0))
        self.connect((self.blocks_short_to_float_0_1, 0), (self.blocks_float_to_complex_0, 1))
        self.connect((self.blocks_vector_source_x_0, 0), (self.digital_chunks_to_symbols_xx_0, 0))
        self.connect((self.digital_chunks_to_symbols_xx_0, 0), (self.blocks_repeat_0, 0))
        self.connect((self.iio_device_source_0, 0), (self.blocks_short_to_float_0, 0))
        self.connect((self.iio_device_source_0, 1), (self.blocks_short_to_float_0_1, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("gnuradio/flowgraphs", "QPSK_raw_loopback_jupiter")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_lo_tx_offset(self):
        return self.lo_tx_offset

    def set_lo_tx_offset(self, lo_tx_offset):
        self.lo_tx_offset = lo_tx_offset
        self.set_tx_lo_freq(int(2200000000 + self.lo_tx_offset))

    def get_tx_lo_freq(self):
        return self.tx_lo_freq

    def set_tx_lo_freq(self, tx_lo_freq):
        self.tx_lo_freq = tx_lo_freq
        self.iio_attr_updater_0_1_0_0.set_value(str(self.tx_lo_freq))

    def get_sps(self):
        return self.sps

    def set_sps(self, sps):
        self.sps = sps
        self.blocks_repeat_0.set_interpolation(self.sps)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)
        self.analog_sig_source_x_0_0.set_sampling_freq(self.samp_rate)
        self.qtgui_freq_sink_x_0.set_frequency_range(0, self.samp_rate)
        self.qtgui_freq_sink_x_0_0.set_frequency_range(0, self.samp_rate)
        self.qtgui_time_sink_x_0.set_samp_rate(self.samp_rate)
        self.qtgui_time_sink_x_1.set_samp_rate(self.samp_rate)

    def get_rx_lo_freq(self):
        return self.rx_lo_freq

    def set_rx_lo_freq(self, rx_lo_freq):
        self.rx_lo_freq = rx_lo_freq
        self.iio_attr_updater_0_1_0.set_value(str(self.rx_lo_freq))

    def get_offset_tx(self):
        return self.offset_tx

    def set_offset_tx(self, offset_tx):
        self.offset_tx = offset_tx
        self.analog_sig_source_x_0.set_frequency(self.offset_tx)

    def get_offset_rx(self):
        return self.offset_rx

    def set_offset_rx(self, offset_rx):
        self.offset_rx = offset_rx
        self.analog_sig_source_x_0_0.set_frequency(self.offset_rx)

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

    def get_hardwaregain_rx0(self):
        return self.hardwaregain_rx0

    def set_hardwaregain_rx0(self, hardwaregain_rx0):
        self.hardwaregain_rx0 = hardwaregain_rx0
        self.iio_attr_updater_0.set_value(str(self.hardwaregain_rx0))

    def get_gain_control_mode_rx0(self):
        return self.gain_control_mode_rx0

    def set_gain_control_mode_rx0(self, gain_control_mode_rx0):
        self.gain_control_mode_rx0 = gain_control_mode_rx0
        self.iio_attr_updater_0_1_0_1.set_value(self.gain_control_mode_rx0)

    def get_buff_size(self):
        return self.buff_size

    def set_buff_size(self, buff_size):
        self.buff_size = buff_size




def main(top_block_cls=QPSK_raw_loopback_jupiter, options=None):

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
