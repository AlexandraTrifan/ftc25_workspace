import adi

sdr = adi.Pluto(uri="ip:pluto.local")

# Set the RX gain control to manual
sdr.gain_control_mode_chan0 = 'manual'
print("RX gain control mode: " + sdr.gain_control_mode_chan0)

# Set the RX hardware gain for Pluto
sdr.rx_hardwaregain_chan0 = 10
print("RX gain : " + str(sdr.rx_hardwaregain_chan0))
