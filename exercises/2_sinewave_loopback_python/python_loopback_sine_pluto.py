import numpy as np
import adi
import matplotlib.pyplot as plt
import time

############################################################################################################
# Configure SDR ############################################################################################
############################################################################################################
frequency_tx = 20000  # 20 KHz sinewave to be transmitted
num_periods_tx = 50
amplitude = 2**14
center_freq_tx = 915000000 # 915 MHz
sample_rate = 2e6 # Hz
num_samps_tx = int(num_periods_tx*sample_rate/frequency_tx) # number of samples per call to rx(), multiple of 200 to have full period of the sinewave
num_samps_rx = num_samps_tx

sdr = adi.Pluto("ip:192.168.2.1")
sdr.sample_rate = int(sample_rate)

# Config Tx
sdr.tx_rf_bandwidth = int(sample_rate) # filter cutoff, just set it to the same as sample rate
sdr.tx_lo = center_freq_tx
sdr.tx_hardwaregain_chan0 = -10 # Increase to increase tx power, valid range is -90 to 0 dB
sdr._tx_buffer_size = 200*10 # number of samples per call to tx()
sdr.tx_cyclic_buffer = True # Enable cyclic buffers

# Config Rx
sdr.rx_lo = center_freq_tx
sdr.rx_rf_bandwidth = int(sample_rate)
sdr.rx_buffer_size = num_samps_rx
sdr.gain_control_mode_chan0 = 'fast_attack'
sdr.rx_hardwaregain_chan0 = 0 # dB, increase to increase the receive gain, but be careful not to saturate the ADC

# Destroy Tx buffer
sdr.tx_destroy_buffer()

# Destroy Rx buffer
sdr.rx_destroy_buffer()
############################################################################################################
############################################################################################################

############################################################################################################
# Create and plot a complex sinusoid #######################################################################
############################################################################################################
# Calculate time values
t = np.arange(num_samps_tx) / sample_rate
# Generate sinusoidal waveform
phase_shift = -np.pi/2  # Shift by -90 degrees
tx_samples = amplitude * (np.cos(2 * np.pi * frequency_tx * t + phase_shift) + 1j*np.sin(2 * np.pi * frequency_tx * t + phase_shift))

fig,axs = plt.subplots(2,3, figsize=(12,6))

plotted_num_samples_time_tx = int(num_samps_tx/num_periods_tx*2)

# Plot Tx time domain
axs[0,0].plot(t[:plotted_num_samples_time_tx], np.real(tx_samples[:plotted_num_samples_time_tx]), label = "I (Real)")
axs[0,0].plot(t[:plotted_num_samples_time_tx], np.imag(tx_samples[:plotted_num_samples_time_tx]), label = "Q (Imag)")
axs[0,0].legend()
axs[0,0].set_title('Tx time domain')
axs[0,0].set_xlabel('Time (seconds)')
axs[0,0].set_ylabel('Amplitude')
axs[0,0].grid(True)

# Calculate Tx spectrum in dBFS
tx_samples_fft = tx_samples * np.hanning(num_samps_tx)
ampl_tx = (np.abs(np.fft.fftshift(np.fft.fft(tx_samples_fft))))
fft_txvals_iq_dbFS = 10*np.log10(np.real(ampl_tx)**2 + np.imag(ampl_tx)**2) + 20*np.log10(2/2**(15-1))\
                                         - 20*np.log10(len(ampl_tx))
f = np.linspace(sample_rate/-2, sample_rate/2, len(fft_txvals_iq_dbFS))

# Plot Tx freq domain
axs[0,1].plot(f/1e6, fft_txvals_iq_dbFS, label = "Tx Spectrum")
axs[0,1].legend()
axs[0,1].set_xlabel("Frequency [MHz]")
axs[0,1].set_ylabel("dBFS")
axs[0,1].set_title('Tx FFT')
axs[0,1].grid(True)

# Constellation plot for the transmit data
axs[0,2].plot(np.real(tx_samples), np.imag(tx_samples), '.', label = "Tx Constellation")
axs[0,2].legend()
axs[0,2].set_xlabel("I (Real) Sample Value")
axs[0,2].set_ylabel("Q (Imag) Sample Value")
axs[0,2].grid(True)
axs[0,2].set_title('Constellation Plot Tx')
############################################################################################################
############################################################################################################

############################################################################################################
# Call Tx function to start transmission ###################################################################
############################################################################################################
sdr.tx(tx_samples) # start transmitting
############################################################################################################
############################################################################################################

time.sleep(1) # wait for internal calibrations
# Clear buffer just to be safe
for i in range (0, 10):
    raw_data = sdr.rx()

############################################################################################################
# Call Rx function to receive transmission and plot the data################################################
############################################################################################################
# Receive samples
rx_samples = sdr.rx()

# Stop transmitting
sdr.tx_destroy_buffer()

# Destroy Rx buffer
sdr.rx_destroy_buffer()

# Time values
t = np.arange(num_samps_rx) / sample_rate

plotted_num_samples_time_rx = int(num_samps_rx/num_periods_tx*2)

# Plot Rx time domain
axs[1,0].plot(t[:plotted_num_samples_time_rx], np.real(rx_samples[:plotted_num_samples_time_rx]), label = "I (Real)")
axs[1,0].plot(t[:plotted_num_samples_time_rx], np.imag(rx_samples[:plotted_num_samples_time_rx]), label = "Q (Imag)")
axs[1,0].legend()
axs[1,0].set_title('Rx time domain')
axs[1,0].set_xlabel('Time (seconds)')
axs[1,0].set_ylabel('Amplitude')
axs[1,0].grid(True)

# Calculate Rx spectrum in dBFS
rx_samples_fft = rx_samples * np.hanning(len(rx_samples))
ampl_rx = (np.abs(np.fft.fftshift(np.fft.fft(rx_samples_fft))))
fft_rxvals_iq_dbFS = 10*np.log10(np.real(ampl_rx)**2 + np.imag(ampl_rx)**2) + 20*np.log10(2/2**(11-1))\
                                         - 20*np.log10(len(ampl_rx))
f = np.linspace(sample_rate/-2, sample_rate/2, len(fft_rxvals_iq_dbFS))

# Plot Rx freq domain
axs[1,1].plot(f/1e6, fft_rxvals_iq_dbFS, label = "Rx Spectrum")
axs[1,1].legend()
axs[1,1].set_xlabel("Frequency [MHz]")
axs[1,1].set_ylabel("dBFS")
axs[1,1].set_title('Rx FFT')
axs[1,1].grid(True)

# Constellation plot for the transmit data
axs[1,2].plot(np.real(rx_samples), np.imag(rx_samples), '.', label = "Rx Constellation")
axs[1,2].legend()
axs[1,2].set_xlabel("I (Real) Sample Value")
axs[1,2].set_ylabel("Q (Imag) Sample Value")
axs[1,2].grid(True)
axs[1,2].set_title('Constellation Plot Rx')

plt.subplots_adjust(hspace=0.4)
plt.show()
############################################################################################################
############################################################################################################
