import time
import adi
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal

############################################################################################################
# Configure SDR ############################################################################################
############################################################################################################
# Configure properties
sdr = adi.adrv9002(uri="ip:jupiter.local") # Create Radio

center_freq = 2200000000 # Hz
sample_rate = sdr.rx0_sample_rate
print("sample rate: ", sample_rate)

sdr.rx_ensm_mode_chan0 = "rf_enabled"
sdr.rx_ensm_mode_chan1 = "rf_enabled"
sdr.gain_control_mode_chan0 = 'spi'
sdr.tx_hardwaregain_chan0 = -20
sdr.rx_hardwaregain_chan0 = 0
sdr.tx_ensm_mode_chan0 = "rf_enabled"
sdr.tx_cyclic_buffer = True
sdr._tx_buffer_size = 2*2048 # number of samples per call to tx()
sdr.rx_buffer_size = 32768
sdr.tx0_lo = center_freq
sdr.rx0_lo = center_freq

fs = int(sdr.rx0_sample_rate)

# Destroy Tx buffers
sdr.tx_destroy_buffer()

# Destroy Rx bufferrs
sdr.rx_destroy_buffer()
############################################################################################################
############################################################################################################

############################################################################################################
# Create array of bits #####################################################################################
############################################################################################################
predefined_key = [1, 1, 0, 0, 1, 1, 0, 0, 1, 1] # predefined key composed of firts 10 bits
num_symbols = 64 - 1 # (encoded message has one more bit) 64 * 16 = 2048 symbols will be received
sps = 16
bits = np.random.randint(0, 2, num_symbols) # Our data to be transmitted, 1's and 0'
bits[:10] = predefined_key # change the first 10 bits values with the predefined key
bits_transmitted = bits #save bits for plots
############################################################################################################
############################################################################################################

############################################################################################################
# Eecode array of bits with differential encoding algorithm#################################################
############################################################################################################
# Initialize the encoded array
bits_encoded = np.zeros(len(bits) + 1, dtype=np.uint8)
# Set the first encoded bit to be the same as the first input bit
bits_encoded[0] = 0
# Differential encoding for the rest of the bits
for i in range(1, len(bits_encoded)):
    bits_encoded[i] = (bits_encoded[i - 1] ^ bits[i - 1])  # XOR operation can also be used
############################################################################################################
############################################################################################################

############################################################################################################
# Interpolate with 16sps and Remap symbols: bit 0 -> -1; bit 1 -> 1 ########################################
############################################################################################################
pulse_train = np.array([])
for bit in bits_encoded:
    pulse = np.ones(sps)*(bit*2-1)
    pulse[0] = bit*2-1 # set the first value to either a 1 or -1
    pulse_train = np.concatenate((pulse_train, pulse)) # add the 16 samples to the signal

# Make the data complex
samples_tx = pulse_train.astype(complex)
samples_tx = samples_tx * (2**14)
samples_tx_unshifted = samples_tx
############################################################################################################
############################################################################################################

############################################################################################################
# Shift spectrum with 150KHz to the right ##################################################################
############################################################################################################
Ts = 1/fs
t_shift = np.arange(0, Ts*len(samples_tx), Ts) # create time vector
samples_tx = samples_tx * np.exp(1j*2*np.pi*150000*t_shift)
############################################################################################################
############################################################################################################

############################################################################################################
# Calculate shifted transmitted spectrum in dBFS ###########################################################
############################################################################################################
# Calculate Tx1 spectrum in dBFS
tx_samples_fft = samples_tx * np.hanning(len(samples_tx))
ampl_tx = (np.abs(np.fft.fftshift(np.fft.fft(tx_samples_fft))))
fft_tx_vals_iq_dbFS = 10*np.log10(np.real(ampl_tx)**2 + np.imag(ampl_tx)**2) + 20*np.log10(2/2**(16-1))\
                                         - 20*np.log10(len(ampl_tx))
freqs_tx = np.linspace(fs/-2, fs/2, len(fft_tx_vals_iq_dbFS))
############################################################################################################
############################################################################################################

############################################################################################################
# Call tx() function and transmit ##########################################################################
############################################################################################################
sdr.tx_destroy_buffer()
time.sleep(1)
print("Lenght of samples_tx: " + str(len(samples_tx)))
sdr.tx(samples_tx)
#time.sleep(3)
############################################################################################################
############################################################################################################

# Collect data
for r in range(1):

    ############################################################################################################
    # Call rx() function to receive data #######################################################################
    ############################################################################################################
    #sdr.rx_destroy_buffer()
    for i in range (0, 10):
        samples = sdr.rx()
    time.sleep(1)    
    samples = sdr.rx()
    
    # Stop transmitting
    sdr.tx_destroy_buffer()

    # Destroy Rx bufferrs
    sdr.rx_destroy_buffer()
    # #shift spectrum back:
    # Ts = 1/fs
    # t_shift = np.arange(0, Ts*len(samples), Ts) # create time vector
    # samples = samples * np.exp(-1j*2*np.pi*150000*t_shift)    

    # Remap received samples between -1 and 1
    max_real = np.amax(abs(np.real(samples)))
    max_imag = np.amax(abs(np.imag(samples)))
    max_value = max(max_real, max_imag)
    samples *= (1/max_value)
    # Save receive samples for plots
    samples_rx_raw = samples
    ############################################################################################################
    ############################################################################################################

    ############################################################################################################
    # Adjust frequency offset ##################################################################################
    ############################################################################################################   
    # Coarse frequancy adjustment
    samples_adjust = samples**2 # square the received signal to obtain 2* offset frequency
    psd = np.fft.fftshift(np.abs(np.fft.fft(samples_adjust)))
    f = np.linspace(-fs/2.0, fs/2.0, len(psd))
    max_freq = f[np.argmax(psd)]
    Ts = 1/fs # calc sample period
    t = np.arange(0, Ts*len(samples), Ts) # create time vector
    samples = samples * np.exp(-1j*2*np.pi*max_freq*t/2.0)

    # Save samples after coarse frequency adjustment for plots
    samples_rx_coarse_freq_adj = samples
    ############################################################################################################
    ############################################################################################################

    ############################################################################################################
    # Calculate shifted transmitted spectrum in dBFS ###########################################################
    ############################################################################################################
    # Calculate Tx1 spectrum in dBFS
    rx_samples_fft = samples * np.hanning(len(samples))
    ampl_rx = (np.abs(np.fft.fftshift(np.fft.fft(rx_samples_fft))))
    fft_rx_vals_iq_dbFS = 10*np.log10(np.real(ampl_rx)**2 + np.imag(ampl_rx)**2) + 20*np.log10(2/2**(16-1))\
                                            - 20*np.log10(len(ampl_rx))
    freqs_rx = np.linspace(fs/-2, fs/2, len(fft_rx_vals_iq_dbFS))
    ############################################################################################################
    ############################################################################################################

    ############################################################################################################
    # Select only the right samples and decimate ###############################################################
    ############################################################################################################  
    samples_interpolated = signal.resample_poly(samples, 16, 1) # interpolation
    mu = 0 # initial estimate of phase of sample
    out = np.zeros(len(samples) + 10, dtype=complex)
    out_rail = np.zeros(len(samples) + 10, dtype=complex) # stores values, each iteration we need the previous 
                                                          # 2 values plus current value
    i_in = 0 # input samples index
    i_out = 2 # output index (let first two outputs be 0)
    while i_out < len(samples) and i_in+16 < len(samples):
        #out[i_out] = samples[i_in + int(mu)] # grab what we think is the "best" sample
        out[i_out] = samples_interpolated[i_in*16 + int(mu*16)]
        out_rail[i_out] = int(np.real(out[i_out]) > 0) + 1j*int(np.imag(out[i_out]) > 0)
        x = (out_rail[i_out] - out_rail[i_out-2]) * np.conj(out[i_out-1])
        y = (out[i_out] - out[i_out-2]) * np.conj(out_rail[i_out-1])
        mm_val = np.real(y - x)
        mu += sps + 0.3*mm_val
        i_in += int(np.floor(mu)) # round down to nearest int since we are using it as an index
        mu = mu - np.floor(mu) # remove the integer part of mu
        i_out += 1 # increment output index
    out = out[2:i_out] # remove the first two, and anything after i_out (that was never filled out)
    samples = out # only include this line if you want to connect this code snippet with the Costas Loop later on
    # Save samples after time adjustment with interpolation for plots
    samples_rx_time_adj = samples
    ############################################################################################################
    ############################################################################################################
    
    ############################################################################################################
    # Fine frequency and phase adjustment (Costas Loop) ########################################################
    ############################################################################################################ 
    N = len(samples)
    phase = 0
    freq = 0
    # These next two params is what to adjust, to make the feedback loop faster or slower (which impacts stability)
    alpha = 0.332
    beta = 0.01932

    out = np.zeros(N, dtype=complex)
    freq_log = []

    for repeat in range(1):
        for i in range(N):
            out[i] = samples[i] * np.exp(-1j*phase) # adjust the input sample by the inverse of the estimated phase offset
            error = np.real(out[i]) * np.imag(out[i]) # This is the error formula for 2nd order Costas Loop (e.g. for BPSK)

            # # Debugging output
            # print(f"Iteration {i}: Phase={phase}, Freq={freq}, Error={error}")

            # Advance the loop (recalc phase and freq offset)
            freq += (beta * error)
            freq_log.append(freq * fs / (2*np.pi)) # convert from angular velocity to Hz for logging
            phase += freq + (alpha * error)

            # Optional: Adjust phase so its always between 0 and 2pi, recall that phase wraps around every 2pi
            while phase >= 2*np.pi:
                phase -= 2*np.pi
            while phase < 0:
                phase += 2*np.pi
    samples = out

    # Save the samples after costas loop (fine frequency and phase adjustment) for plots
    samples_rx_costas_loop = samples
    ##############################################################################################################
    ##############################################################################################################

    ############################################################################################################
    # Decide if the received symbol is a 1 or a 0 ##############################################################
    ############################################################################################################
    received_bits_undecoded = np.where(samples_rx_costas_loop.real > 0, 1, 0)
    ############################################################################################################

    ############################################################################################################
    # Decode bits with differential decoding ###################################################################
    ############################################################################################################
    # Differential decoded bits
    bits_decoded = np.zeros(len(received_bits_undecoded) - 1, dtype=np.uint8)
    for i in range(0, len(bits_decoded)):
        bits_decoded[i] = (received_bits_undecoded[i] ^ received_bits_undecoded[i + 1])
    #print("Differential decoded bits:" + "\n" + str(bits_decoded))
    #samples_rx_costas_loop = bits_decoded
    ############################################################################################################
    ############################################################################################################

    ############################################################################################################
    # Extrct only one packet ###################################################################################
    ############################################################################################################
    packet_length = num_symbols
    rx_packet = np.zeros(len(bits_decoded), dtype=np.uint8)
    for i in range(len(bits_decoded) - len(predefined_key) + 1):
        if np.array_equal(bits_decoded[i:i+len(predefined_key)], predefined_key):
            # Extract the packet starting from this index
            rx_packet = bits_decoded[i:i + packet_length]
            break
    bits_demodulated = rx_packet
    ############################################################################################################
    ############################################################################################################   

# ############################################################################################################
# # Plot data ################################################################################################
# ############################################################################################################

# Create figure with time domain plots
fig1,axs1 = plt.subplots(3,3, figsize=(12,9))

# Plot transmitted bits
axs1[0,0].plot(bits_transmitted,'.-')
axs1[0,0].set_xlabel("No. Bit")
axs1[0,0].set_ylabel("Bit Value")
axs1[0,0].grid()
# axs1[0,0].legend()
axs1[0,0].set_title('Bits Tx')

# Plot transmitted bits encoded with differential encoding
axs1[0,1].plot(bits_encoded,'.-')
axs1[0,1].set_xlabel("No. Bit")
axs1[0,1].set_ylabel("Bit Value")
axs1[0,1].grid()
# axs1[0,1].legend()
axs1[0,1].set_title('Bits Tx Encoded')

# Plot samples tx before freq shift
axs1[0,2].plot(np.real(samples_tx_unshifted),'.-', label = "I (Real)")
axs1[0,2].plot(np.imag(samples_tx_unshifted),'.-', label = "Q (Imag)")
axs1[0,2].legend()
axs1[0,2].set_xlabel("No. Sample")
axs1[0,2].set_ylabel("Sample value")
axs1[0,2].grid(True)
axs1[0,2].set_title('Samples Tx w/o Freq. Shift.')

# Plot samples tx after freq shift
axs1[1,0].plot(np.real(samples_tx[num_symbols*3:num_symbols*5]),'.-', label = "I (Real)")
axs1[1,0].plot(np.imag(samples_tx[num_symbols*3:num_symbols*5]),'.-', label = "Q (Imag)")
axs1[1,0].legend()
axs1[1,0].set_xlabel("No. Sample")
axs1[1,0].set_ylabel("Sample value")
axs1[1,0].grid(True)
axs1[1,0].set_title('Samples Tx with Freq. Shift.')

# Plot samples rx Raw
axs1[1,1].plot(np.real(samples_rx_raw[num_symbols*3:num_symbols*5]),'.-', label = "I (Real)")
axs1[1,1].plot(np.imag(samples_rx_raw[num_symbols*3:num_symbols*5]),'.-', label = "Q (Imag)")
axs1[1,1].legend()
axs1[1,1].set_xlabel("No. Sample")
axs1[1,1].set_ylabel("Sample value")
axs1[1,1].grid(True)
axs1[1,1].set_title('Samples Rx Raw')

# Plot samples Rx after Coarse Freq adjustment and Symbol Sync
axs1[1,2].plot(np.real(samples_rx_time_adj[num_symbols*3:num_symbols*5]),'.-', label = "I (Real)")
axs1[1,2].plot(np.imag(samples_rx_time_adj[num_symbols*3:num_symbols*5]),'.-', label = "Q (Imag)")
axs1[1,2].legend()
axs1[1,2].set_xlabel("No. Sample")
axs1[1,2].set_ylabel("Sample value")
axs1[1,2].grid(True)
axs1[1,2].set_title('Samples Rx after Freq Adj. & Symbol Sync')

# Plot samples Rx after Costas Loop
axs1[2,0].plot(np.real(samples_rx_costas_loop[num_symbols*3:num_symbols*5]),'.-', label = "I (Real)")
axs1[2,0].plot(np.imag(samples_rx_costas_loop[num_symbols*3:num_symbols*5]),'.-', label = "Q (Imag)")
axs1[2,0].legend()
axs1[2,0].set_xlabel("No. Sample")
axs1[2,0].set_ylabel("Sample value")
axs1[2,0].grid(True)
axs1[2,0].set_title('Samples Rx after Costas Loop')

# Plot bits received undecoded
axs1[2,1].plot(received_bits_undecoded[num_symbols*3:num_symbols*4],'.-')
axs1[2,1].set_xlabel("No. Bit")
axs1[2,1].set_ylabel("Bit Value")
axs1[2,1].grid()
# axs1[2,1].legend()
axs1[2,1].set_title('Bits Rx Undecoded')

# Plot bits received decoded
axs1[2,2].plot(bits_demodulated,'.-')
axs1[2,2].set_xlabel("No. Bit")
axs1[2,2].set_ylabel("Bit Value")
axs1[2,2].grid()
# axs1[2,2].legend()
axs1[2,2].set_title('Bits Rx Decoded')

plt.subplots_adjust(wspace=0.6, hspace=0.6)

# Create figure with constellation plots
fig2,axs2 = plt.subplots(2,3, figsize=(12,6))

# Plot the constellation with the samples transmitted beofre freq shift
axs2[0,0].plot(np.real(samples_tx_unshifted), np.imag(samples_tx_unshifted), 'o')
axs2[0,0].set_xlabel("I (Real) Sample Value")
axs2[0,0].set_ylabel("Q (Imag) Sample Value")
axs2[0,0].grid(True)
# axs2[0,0].legend()
axs2[0,0].set_title('Constellation Plot Tx')

# Plot the constellation with the samples transmitted after freq. shift
axs2[0,1].plot(np.real(samples_tx), np.imag(samples_tx), 'o')
axs2[0,1].set_xlabel("I (Real) Sample Value")
axs2[0,1].set_ylabel("Q (Imag) Sample Value")
axs2[0,1].grid(True)
# axs2[0,1].legend()
axs2[0,1].set_title('Constellation Tx (After Freq. Shift)') 

# Plot the Rx constellation with samples received raw
axs2[0,2].plot(np.real(samples_rx_raw), np.imag(samples_rx_raw), '.')
axs2[0,2].set_xlabel("I (Real) Sample Value")
axs2[0,2].set_ylabel("Q (Imag) Sample Value")
axs2[0,2].grid(True)
# axs2[0,2].legend()
axs2[0,2].set_title('Constellation Rx Raw')

# Plot the Rx constellation after Coarse Freq Adjustment
axs2[1,0].plot(np.real(samples_rx_coarse_freq_adj), np.imag(samples_rx_coarse_freq_adj), '.')
axs2[1,0].set_xlabel("I (Real) Sample Value")
axs2[1,0].set_ylabel("Q (Imag) Sample Value")
axs2[1,0].grid(True)
# axs2[1,0].legend()
axs2[1,0].set_title('Constellation Rx after Freq Adjustment')

# Plot the Rx constellation after Symbol Sync
axs2[1,1].plot(np.real(samples_rx_time_adj), np.imag(samples_rx_time_adj), '.')
axs2[1,1].set_xlabel("I (Real) Sample Value")
axs2[1,1].set_ylabel("Q (Imag) Sample Value")
axs2[1,1].grid(True)
# axs2[1,1].legend()
axs2[1,1].set_title('Constellation Rx after Symbol Sync')

# Plot the Rx constellation after Costas Loop
axs2[1,2].plot(np.real(samples_rx_costas_loop), np.imag(samples_rx_costas_loop), '.', label = "all samples")
axs2[1,2].set_xlabel("I (Real) Sample Value")
axs2[1,2].set_ylabel("Q (Imag) Sample Value")
axs2[1,2].set_xlim([-2, 2])
axs2[1,2].set_ylim([-2, 2])
axs2[1,2].grid(True)
axs2[1,2].set_title('Constellation Rx after Costas Loop')
# eliminate fist 200 samples to pass the costas loop adjustment 
samples_rx_costas_loop = samples_rx_costas_loop[200:]
axs2[1,2].plot(np.real(samples_rx_costas_loop), np.imag(samples_rx_costas_loop), '.', label = "without first 200 samples")
axs2[1,2].legend()

plt.subplots_adjust(wspace=0.6, hspace=0.6)
plt.show()
############################################################################################################
############################################################################################################
