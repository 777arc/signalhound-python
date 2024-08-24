from bbdevice.bb_api import *
import matplotlib.pyplot as plt
import numpy as np

handle = bb_open_device()["handle"] # Open device

# Configure device
bb_configure_ref_level(handle, -70.0) # I cant quite figure out how this works
bb_configure_gain_atten(handle, BB_AUTO_GAIN, BB_AUTO_ATTEN)
bb_configure_IQ_center(handle, center_freq=99.5e6)
downsample_factor = 16 # must be an order of two it seems
sample_rate = 40e6/downsample_factor # 40 MHz is their native sample rate apparently
bb_configure_IQ(handle, downsample_factor=downsample_factor, bandwidth=sample_rate*0.8)

# Initialize
bb_initiate(handle, BB_STREAMING, BB_STREAM_IQ)

print(bb_query_IQ_parameters(handle)) # must come after bb_initiate

N = 16384
iq = bb_get_IQ_unpacked(handle, N, BB_TRUE)["iq"] # Get IQ data
iq *= 2**10 # they are doing weird scaling, so we need to undo it to get between -1 and +1

bb_close_device(handle) # No longer need device, close

# FFT plot
plt.figure(0)
iq_data_FFT = np.fft.fftshift(np.fft.fft(iq) / N)
PSD = 10 * np.log10(iq_data_FFT.real ** 2 + iq_data_FFT.imag ** 2)
f = np.linspace(-sample_rate/2/1e6, sample_rate/2/1e6, len(iq_data_FFT))
plt.plot(f, PSD)
plt.xlabel("Frequency (MHz)")
plt.ylabel("Power Spectral Density (dB)")
plt.grid()

# Time plot
plt.figure(1)
plt.plot(iq.real)
plt.plot(iq.imag)
plt.xlabel("Time")
plt.ylabel("Amplitude")
plt.grid()

plt.show()


