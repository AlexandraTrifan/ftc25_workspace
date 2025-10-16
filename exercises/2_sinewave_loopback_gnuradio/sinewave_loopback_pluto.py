#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: sinewave_loopback_pluto
# GNU Radio version: 3.10.11.0

from PyQt5 import Qt
from gnuradio import qtgui
from PyQt5 import QtCore
from gnuradio import analog
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



class sinewave_loopback_pluto(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "sinewave_loopback_pluto", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("sinewave_loopback_pluto")
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

        self.settings = Qt.QSettings("gnuradio/flowgraphs", "sinewave_loopback_pluto")

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
        self.tx_attenuation = tx_attenuation = 15
        self.sine_frequency = sine_frequency = 10000
        self.samp_rate = samp_rate = 1000000
        self.rx_gain = rx_gain = 10
        self._pluto_ip_config = configparser.ConfigParser()
        self._pluto_ip_config.read('default')
        try: pluto_ip = self._pluto_ip_config.get('main', 'key')
        except: pluto_ip = 'ip:192.168.2.1'
        self.pluto_ip = pluto_ip
        self.lo_freq_tx = lo_freq_tx = 3200000000
        self.lo_freq_rx = lo_freq_rx = 3200000000
        self.interval_update = interval_update = int(0)
        self.buff_size = buff_size = int(32768)

        ##################################################
        # Blocks
        ##################################################

        self._tx_attenuation_range = qtgui.Range(0, 89, 1, 15, 200)
        self._tx_attenuation_win = qtgui.RangeWidget(self._tx_attenuation_range, self.set_tx_attenuation, "Tx Attenuation", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._tx_attenuation_win)
        self._sine_frequency_range = qtgui.Range(-300000, 300000, 1, 10000, 200)
        self._sine_frequency_win = qtgui.RangeWidget(self._sine_frequency_range, self.set_sine_frequency, "Transmitted Sine Frequency [Hz]", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._sine_frequency_win, 0, 0, 1, 2)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._rx_gain_range = qtgui.Range(0, 60, 1, 10, 200)
        self._rx_gain_win = qtgui.RangeWidget(self._rx_gain_range, self.set_rx_gain, "Rx Gain", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._rx_gain_win)
        self.qtgui_time_sink_x_1 = qtgui.time_sink_c(
            (1024*8), #size
            samp_rate, #samp_rate
            "Received Samples", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_1.set_update_time(0.10)
        self.qtgui_time_sink_x_1.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_1.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_1.enable_tags(True)
        self.qtgui_time_sink_x_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.4, 0, 0, "")
        self.qtgui_time_sink_x_1.enable_autoscale(False)
        self.qtgui_time_sink_x_1.enable_grid(False)
        self.qtgui_time_sink_x_1.enable_axis_labels(True)
        self.qtgui_time_sink_x_1.enable_control_panel(False)
        self.qtgui_time_sink_x_1.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
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
        self.top_grid_layout.addWidget(self._qtgui_time_sink_x_1_win, 1, 1, 1, 1)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_time_sink_x_0 = qtgui.time_sink_c(
            (1024*8), #size
            samp_rate, #samp_rate
            "Transmitted samples", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0.enable_tags(True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_NORM, qtgui.TRIG_SLOPE_POS, 0.5, 0, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0.enable_grid(False)
        self.qtgui_time_sink_x_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
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
        self.qtgui_freq_sink_x_1 = qtgui.freq_sink_c(
            8192, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            'Transmitted Spectrum', #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_1.set_update_time(0.10)
        self.qtgui_freq_sink_x_1.set_y_axis((-240), 10)
        self.qtgui_freq_sink_x_1.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_1.set_trigger_mode(qtgui.TRIG_MODE_NORM, -15, 0, "")
        self.qtgui_freq_sink_x_1.enable_autoscale(False)
        self.qtgui_freq_sink_x_1.enable_grid(False)
        self.qtgui_freq_sink_x_1.set_fft_average(1.0)
        self.qtgui_freq_sink_x_1.enable_axis_labels(True)
        self.qtgui_freq_sink_x_1.enable_control_panel(False)
        self.qtgui_freq_sink_x_1.set_fft_window_normalized(True)



        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_1.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_1.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_1.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_1.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_1_win = sip.wrapinstance(self.qtgui_freq_sink_x_1.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_freq_sink_x_1_win, 2, 0, 1, 1)
        for r in range(2, 3):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
            32768, #size
            window.WIN_FLATTOP, #wintype
            0, #fc
            samp_rate, #bw
            "Received spectrum", #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0.set_y_axis((-140), 10)
        self.qtgui_freq_sink_x_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, -60, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0.enable_grid(False)
        self.qtgui_freq_sink_x_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0.enable_control_panel(False)
        self.qtgui_freq_sink_x_0.set_fft_window_normalized(True)



        labels = ['', '', '', '', '',
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
        self.top_grid_layout.addWidget(self._qtgui_freq_sink_x_0_win, 2, 1, 1, 1)
        for r in range(2, 3):
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
        self.qtgui_const_sink_x_0.enable_grid(False)
        self.qtgui_const_sink_x_0.enable_axis_labels(True)


        labels = ['', '', '', '', '',
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
        self.top_grid_layout.addWidget(self._qtgui_const_sink_x_0_win, 3, 0, 1, 2)
        for r in range(3, 4):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.iio_pluto_source_0 = iio.fmcomms2_source_fc32(pluto_ip if pluto_ip else iio.get_pluto_uri(), [True, True], buff_size)
        self.iio_pluto_source_0.set_len_tag_key('packet_len')
        self.iio_pluto_source_0.set_frequency(lo_freq_rx)
        self.iio_pluto_source_0.set_samplerate(samp_rate)
        self.iio_pluto_source_0.set_gain_mode(0, 'manual')
        self.iio_pluto_source_0.set_gain(0, rx_gain)
        self.iio_pluto_source_0.set_quadrature(True)
        self.iio_pluto_source_0.set_rfdc(True)
        self.iio_pluto_source_0.set_bbdc(True)
        self.iio_pluto_source_0.set_filter_params('Auto', '', 0, 0)
        self.iio_pluto_sink_0 = iio.fmcomms2_sink_fc32(pluto_ip if pluto_ip else iio.get_pluto_uri(), [True, True], buff_size, False)
        self.iio_pluto_sink_0.set_len_tag_key('')
        self.iio_pluto_sink_0.set_bandwidth((samp_rate*5))
        self.iio_pluto_sink_0.set_frequency(lo_freq_tx)
        self.iio_pluto_sink_0.set_samplerate(samp_rate)
        self.iio_pluto_sink_0.set_attenuation(0, tx_attenuation)
        self.iio_pluto_sink_0.set_filter_params('Auto', '', 0, 0)
        self.analog_sig_source_x_0 = analog.sig_source_c(samp_rate, analog.GR_SIN_WAVE, sine_frequency, 1, 0, 0)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_sig_source_x_0, 0), (self.iio_pluto_sink_0, 0))
        self.connect((self.analog_sig_source_x_0, 0), (self.qtgui_freq_sink_x_1, 0))
        self.connect((self.analog_sig_source_x_0, 0), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.iio_pluto_source_0, 0), (self.qtgui_const_sink_x_0, 0))
        self.connect((self.iio_pluto_source_0, 0), (self.qtgui_freq_sink_x_0, 0))
        self.connect((self.iio_pluto_source_0, 0), (self.qtgui_time_sink_x_1, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("gnuradio/flowgraphs", "sinewave_loopback_pluto")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_tx_attenuation(self):
        return self.tx_attenuation

    def set_tx_attenuation(self, tx_attenuation):
        self.tx_attenuation = tx_attenuation
        self.iio_pluto_sink_0.set_attenuation(0,self.tx_attenuation)

    def get_sine_frequency(self):
        return self.sine_frequency

    def set_sine_frequency(self, sine_frequency):
        self.sine_frequency = sine_frequency
        self.analog_sig_source_x_0.set_frequency(self.sine_frequency)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)
        self.iio_pluto_sink_0.set_bandwidth((self.samp_rate*5))
        self.iio_pluto_sink_0.set_samplerate(self.samp_rate)
        self.iio_pluto_source_0.set_samplerate(self.samp_rate)
        self.qtgui_freq_sink_x_0.set_frequency_range(0, self.samp_rate)
        self.qtgui_freq_sink_x_1.set_frequency_range(0, self.samp_rate)
        self.qtgui_time_sink_x_0.set_samp_rate(self.samp_rate)
        self.qtgui_time_sink_x_1.set_samp_rate(self.samp_rate)

    def get_rx_gain(self):
        return self.rx_gain

    def set_rx_gain(self, rx_gain):
        self.rx_gain = rx_gain
        self.iio_pluto_source_0.set_gain(0, self.rx_gain)

    def get_pluto_ip(self):
        return self.pluto_ip

    def set_pluto_ip(self, pluto_ip):
        self.pluto_ip = pluto_ip

    def get_lo_freq_tx(self):
        return self.lo_freq_tx

    def set_lo_freq_tx(self, lo_freq_tx):
        self.lo_freq_tx = lo_freq_tx
        self.iio_pluto_sink_0.set_frequency(self.lo_freq_tx)

    def get_lo_freq_rx(self):
        return self.lo_freq_rx

    def set_lo_freq_rx(self, lo_freq_rx):
        self.lo_freq_rx = lo_freq_rx
        self.iio_pluto_source_0.set_frequency(self.lo_freq_rx)

    def get_interval_update(self):
        return self.interval_update

    def set_interval_update(self, interval_update):
        self.interval_update = interval_update

    def get_buff_size(self):
        return self.buff_size

    def set_buff_size(self, buff_size):
        self.buff_size = buff_size




def main(top_block_cls=sinewave_loopback_pluto, options=None):

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
