import numpy as np
import adi
import matplotlib.pyplot as plt
import time

############################################################################################################
# Configure SDR ############################################################################################
############################################################################################################
frequency_tx1 = 20000  # 10 KHz sinewave to be transmitted
frequency_tx2 = frequency_tx1 * 3
num_periods_tx1 = 160
num_periods_tx2 = num_periods_tx1 * 3 # if frequency_tx2 = frequency_tx1 * x then num_periods_tx2 = num_periods_tx1 * x because the buffers for both channels needs to have the same length
amplitude = 2**14 # maximum is (2**15) - 1
center_freq_tx = 915000000 # 915 MHz
sample_rate = 2e6 # Hz
num_samps_tx1 = int((num_periods_tx1*sample_rate)/frequency_tx1) # number of samples per call to rx(), multiple of 200 to have full period of the sinewave
num_samps_tx2 = int((num_periods_tx2*sample_rate)/frequency_tx2)
print("num_samps_tx1: " + str(num_samps_tx1))
print("num_samps_tx2: " + str(num_samps_tx2))
num_samps_rx1 = num_samps_tx1
num_samps_rx2 = num_samps_tx2

sdr = adi.ad9361("ip:192.168.2.1")
sdr.sample_rate = int(sample_rate)

# Enable both channels
sdr.rx_enabled_channels = [0, 1]
sdr.tx_enabled_channels = [0, 1]

# Config Tx 1
sdr.tx_rf_bandwidth = int(sample_rate) # filter cutoff, just set it to the same as sample rate
sdr.tx_lo = center_freq_tx
sdr.tx_hardwaregain_chan0 = -10 # Increase to increase tx power, valid range is -90 to 0 dB
sdr.tx_buffer_size = num_samps_tx1# number of samples per call to tx()
sdr.tx_cyclic_buffer = True # Enable cyclic buffers

# Config Tx 2
# sdr.tx2_buffer_size = num_samps_tx2
sdr.tx_hardwaregain_chan1 = -10 # Increase to increase tx power, valid range is -90 to 0 dB

# Config Rx 1
sdr.rx_lo = center_freq_tx
sdr.rx_rf_bandwidth = int(sample_rate)
sdr.rx_buffer_size = num_samps_rx1
sdr.gain_control_mode_chan0 = 'slow_attack' # other modes: 'fast_attack', 'slow_attack', 'manual'
# sdr.rx_hardwaregain_chan0 = 0 # dB, works only for sdr.gain_control_mode_chan0 = 'manual'

# Config Rx 2
sdr.gain_control_mode_chan1 = 'slow_attack' # other modes: 'fast_attack', 'slow_attack', 'manual'
# sdr.rx_hardwaregain_chan1 = 0 # dB, works only for sdr.gain_control_mode_chan1 = 'manual'

# Destroy Tx buffer
sdr.tx_destroy_buffer()

# Destroy Rx buffer
sdr.rx_destroy_buffer()
############################################################################################################
############################################################################################################

############################################################################################################
# Create and plot a complex sinusoid #######################################################################
############################################################################################################
# Calculate time values for Tx1
t1 = np.arange(num_samps_tx1) / sample_rate
# Generate sinusoidal waveform
phase_shift = -np.pi/2  # Shift by -90 degrees
tx1_samples = amplitude * (np.cos(2 * np.pi * frequency_tx1 * t1 + phase_shift) + 1j*np.sin(2 * np.pi * frequency_tx1 * t1 + phase_shift))

# Calculate time values for Tx2
t2 = np.arange(num_samps_tx2) / sample_rate
# Generate sinusoidal waveform
tx2_samples = amplitude * (np.cos(2 * np.pi * frequency_tx2 * t2 + phase_shift) + 1j*np.sin(2 * np.pi * frequency_tx2 * t2 + phase_shift))

fig,axs = plt.subplots(2,3, figsize=(12,6))

#plotted_num_samples_time_tx = int(num_samps_tx1/num_periods_tx*2)
if(frequency_tx1 < frequency_tx2):
    plotted_num_samples_time_tx = int(num_samps_tx1/num_periods_tx1)
else:
    plotted_num_samples_time_tx = int(num_samps_tx2/num_periods_tx2) 

# Plot Tx time domain
axs[0,0].plot(t1[:plotted_num_samples_time_tx], np.real(tx1_samples[:plotted_num_samples_time_tx]), label = "I (Real) Tx1")
axs[0,0].plot(t1[:plotted_num_samples_time_tx], np.imag(tx1_samples[:plotted_num_samples_time_tx]), label = "Q (Imag) Tx1")
axs[0,0].plot(t2[:plotted_num_samples_time_tx], np.real(tx2_samples[:plotted_num_samples_time_tx]), label = "I (Real) Tx2")
axs[0,0].plot(t2[:plotted_num_samples_time_tx], np.imag(tx2_samples[:plotted_num_samples_time_tx]), label = "Q (Imag) Tx2")
axs[0,0].legend()
axs[0,0].set_title('Tx1 Tx2 time domain')
axs[0,0].set_xlabel('Time (seconds)')
axs[0,0].set_ylabel('Amplitude')
axs[0,0].grid(True)

# Calculate Tx1 spectrum in dBFS
tx1_samples_fft = tx1_samples * np.hanning(num_samps_tx1)
ampl_tx = (np.abs(np.fft.fftshift(np.fft.fft(tx1_samples_fft))))
fft_tx1_vals_iq_dbFS = 10*np.log10(np.real(ampl_tx)**2 + np.imag(ampl_tx)**2) + 20*np.log10(2/2**(15-1))\
                                         - 20*np.log10(len(ampl_tx))
f1 = np.linspace(sample_rate/-2, sample_rate/2, len(fft_tx1_vals_iq_dbFS))

# Calculate Tx2 spectrum in dBFS
tx2_samples_fft = tx2_samples * np.hanning(num_samps_tx2)
ampl_tx = (np.abs(np.fft.fftshift(np.fft.fft(tx2_samples_fft))))
fft_tx2_vals_iq_dbFS = 10*np.log10(np.real(ampl_tx)**2 + np.imag(ampl_tx)**2) + 20*np.log10(2/2**(15-1))\
                                         - 20*np.log10(len(ampl_tx))
f2 = np.linspace(sample_rate/-2, sample_rate/2, len(fft_tx2_vals_iq_dbFS))

# Plot Tx1 and Tx2 freq domain
axs[0,1].plot(f1/1e6, fft_tx1_vals_iq_dbFS, label = "Tx1 Spectrum")
axs[0,1].plot(f2/1e6, fft_tx2_vals_iq_dbFS, label = "Tx2 Spectrum")
axs[0,1].legend()
axs[0,1].set_xlabel("Frequency [MHz]")
axs[0,1].set_ylabel("dBFS")
axs[0,1].grid(True)
axs[0,1].set_title('Tx1 Tx2 FFT')

# Constellation plot for the Tx1 data
axs[0,2].plot(np.real(tx1_samples), np.imag(tx1_samples), '.', label = "Tx1 Constellation")
axs[0,2].plot(np.real(tx2_samples), np.imag(tx2_samples), '.', label = "Tx2 Constellation")
axs[0,2].set_xlabel("I (Real) Sample Value")
axs[0,2].set_ylabel("Q (Imag) Sample Value")
axs[0,2].grid(True)
axs[0,2].legend()
axs[0,2].set_title('Constellation Plot Tx1 Tx2')
############################################################################################################
############################################################################################################

############################################################################################################
# Call Tx function to start transmission ###################################################################
############################################################################################################
sdr.tx([tx1_samples, tx2_samples]) # start transmitting
############################################################################################################
############################################################################################################

time.sleep(1) # wait for internal calibrations
# Clear buffer just to be safe
for i in range (0, 10):
    raw_data = sdr.rx()

############################################################################################################
# Call Rx function to receive transmission and plot the data################################################
############################################################################################################
# Receive samples on Rx1 and Rx2
data = sdr.rx()
rx1_samples = data[0]
rx2_samples = data[1]

# Stop transmitting
sdr.tx_destroy_buffer()
# sdr.tx2_destroy_buffer()

# Destroy Rx bufferrs
sdr.rx_destroy_buffer()
# sdr.rx2_destroy_buffer()

# Time values for Rx1
t1 = np.arange(num_samps_rx1) / sample_rate
# Time values for Rx1
t2 = np.arange(num_samps_rx2) / sample_rate

if(frequency_tx1 < frequency_tx2):
    plotted_num_samples_time_rx = int(num_samps_rx1/num_periods_tx1)
else:
    plotted_num_samples_time_rx = int(num_samps_rx2/num_periods_tx2) 

# Plot Rx1 and Rx2 time domain
axs[1,0].plot(t1[plotted_num_samples_time_rx:plotted_num_samples_time_rx*2], np.real(rx1_samples[plotted_num_samples_time_rx:plotted_num_samples_time_rx*2]), label = "I (Real) Rx1")
axs[1,0].plot(t1[plotted_num_samples_time_rx:plotted_num_samples_time_rx*2], np.imag(rx1_samples[plotted_num_samples_time_rx:plotted_num_samples_time_rx*2]), label = "Q (Imag) Rx1")
axs[1,0].plot(t2[plotted_num_samples_time_rx:plotted_num_samples_time_rx*2], np.real(rx2_samples[plotted_num_samples_time_rx:plotted_num_samples_time_rx*2]), label = "I (Real) Rx2")
axs[1,0].plot(t2[plotted_num_samples_time_rx:plotted_num_samples_time_rx*2], np.imag(rx2_samples[plotted_num_samples_time_rx:plotted_num_samples_time_rx*2]), label = "Q (Imag) Rx2")
axs[1,0].grid(True)
axs[1,0].legend()
axs[1,0].set_title('Rx1 Rx2 time domain')
axs[1,0].set_xlabel('Time (seconds)')
axs[1,0].set_ylabel('Amplitude')

# Calculate Rx1 spectrum in dBFS
rx1_samples_fft = rx1_samples * np.hanning(num_samps_rx1)
ampl_rx = (np.abs(np.fft.fftshift(np.fft.fft(rx1_samples_fft))))
fft_rx1_vals_iq_dbFS = 10*np.log10(np.real(ampl_rx)**2 + np.imag(ampl_rx)**2) + 20*np.log10(2/2**(15-1))\
                                         - 20*np.log10(len(ampl_rx))
f1 = np.linspace(sample_rate/-2, sample_rate/2, len(fft_rx1_vals_iq_dbFS))

# Calculate Rx2 spectrum in dBFS
rx2_samples_fft = rx2_samples * np.hanning(num_samps_rx2)
ampl_rx = (np.abs(np.fft.fftshift(np.fft.fft(rx2_samples_fft))))
fft_rx2_vals_iq_dbFS = 10*np.log10(np.real(ampl_rx)**2 + np.imag(ampl_rx)**2) + 20*np.log10(2/2**(15-1))\
                                         - 20*np.log10(len(ampl_rx))
f2 = np.linspace(sample_rate/-2, sample_rate/2, len(fft_rx2_vals_iq_dbFS))

# Plot Rx1, Rx2 freq domain
axs[1,1].plot(f1/1e6, fft_rx1_vals_iq_dbFS, label = "Rx1 Spectrum")
axs[1,1].plot(f2/1e6, fft_rx2_vals_iq_dbFS, label = "Rx2 Spectrum")
axs[1,1].set_xlabel("Frequency [MHz]")
axs[1,1].set_ylabel("dBFS")
axs[1,1].set_title('Rx1 Rx2 FFT')
axs[1,1].grid(True)
axs[1,1].legend()

# Constellation plot for Rx1, Rx2
axs[1,2].plot(np.real(rx1_samples), np.imag(rx1_samples), '.', label = "Rx1 Constellation")
axs[1,2].plot(np.real(rx2_samples), np.imag(rx2_samples), '.', label = "Rx2 Constellation")
axs[1,2].set_xlabel("I (Real) Sample Value")
axs[1,2].set_ylabel("Q (Imag) Sample Value")
axs[1,2].grid(True)
axs[1,2].set_title('Constellation Plot Rx1 Rx2')
axs[1,2].legend()

plt.subplots_adjust(hspace=0.4)
plt.show()

sdr.rx_enabled_channels = [0] # leave only channel 0 enabled
sdr.tx_enabled_channels = [0]
############################################################################################################
############################################################################################################
