from bbdevice.bb_api import *
import matplotlib.pyplot as plt

handle = bb_open_device()["handle"] # Open device

# Configure device
bb_configure_center_span(handle, center=100e6, span=10e6)
bb_configure_ref_level(handle, -70.0)
bb_configure_gain_atten(handle, BB_AUTO_GAIN, BB_AUTO_ATTEN)
bb_configure_sweep_coupling(handle, rbw=10.0e3, vbw=10.0e3, sweep_time=0.001, rbw_shape=BB_RBW_SHAPE_FLATTOP, rejection=BB_NO_SPUR_REJECT)
bb_configure_acquisition(handle, BB_MIN_AND_MAX, BB_LOG_SCALE)
bb_configure_proc_units(handle, BB_POWER)

# Initialize
bb_initiate(handle, BB_SWEEPING, 0)
query = bb_query_trace_info(handle)
trace_len = query["trace_len"]
start = query["start"]
bin_size = query["bin_size"]

trace_max = bb_fetch_trace_32f(handle, trace_len)["trace_max"]
freqs = [start + i * bin_size for i in range(trace_len)]

# Device no longer needed, close it
bb_close_device(handle)

plt.plot(freqs, trace_max)
plt.grid()
plt.show()

