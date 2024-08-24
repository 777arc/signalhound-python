# -*- coding: utf-8 -*-

# Copyright (c) 2022 Signal Hound
# For licensing information, please see the API license in the software_licenses folder

from ctypes import *
import numpy

# Added by Marc-
#bblib = CDLL("C:\\Users\\marclichtman\\Downloads\\signal_hound_sdk_08_05_24\\signal_hound_sdk\\device_apis\\bb_series\\lib\\win\\vs2019\\x64\\bb_api.dll")
bblib = CDLL("bbdevice/bb_api.dll")
#bblib = CDLL("bbdevice/bb_api.so") # for ubuntu

# ---------------------------------- Constants -----------------------------------

BB_TRUE = 1
BB_FALSE = 0

# bbGetDeviceType: type
BB_DEVICE_NONE = 0
BB_DEVICE_BB60A = 1
BB_DEVICE_BB60C = 2
BB_DEVICE_BB60D = 3

BB_MAX_DEVICES = 8

# Frequencies specified in Hz
BB_MIN_FREQ = c_double(9.0e3)
BB_MAX_FREQ = c_double(6.4e9)

BB_MIN_SPAN = c_double(20.0)
BB_MAX_SPAN = c_double(BB_MAX_FREQ.value - BB_MIN_FREQ.value)

BB_MIN_RBW = c_double(0.602006912)
BB_MAX_RBW = c_double(10100000.0)

BB_MIN_SWEEP_TIME = c_double(0.00001) # 10us
BB_MAX_SWEEP_TIME = c_double(1.0) # 1s

# Real-Time
BB_MIN_RT_RBW = c_double(2465.820313)
BB_MAX_RT_RBW = c_double(631250.0)
BB_MIN_RT_SPAN = c_double(200.0e3)
BB60A_MAX_RT_SPAN = c_double(20.0e6)
# BB60C/D
BB60C_MAX_RT_SPAN = c_double(27.0e6)

BB_MIN_USB_VOLTAGE = c_double(4.4)

BB_MAX_REFERENCE = c_double(20.0) # dBM

# Gain/Atten can be integers between -1 and MAX
BB_AUTO_ATTEN = -1
BB_MAX_ATTEN = 3
BB_AUTO_GAIN = -1
BB_MAX_GAIN = 3

BB_MIN_DECIMATION = 1 # No decimation
BB_MAX_DECIMATION = 8192

# bbInitiate: mode
BB_IDLE = -1
BB_SWEEPING = 0
BB_REAL_TIME = 1
BB_STREAMING = 4
BB_AUDIO_DEMOD = 7
BB_TG_SWEEPING = 8

# bbConfigureSweepCoupling: rejection
BB_NO_SPUR_REJECT = 0
BB_SPUR_REJECT = 1

# bbConfigureAcquisition: scale
BB_LOG_SCALE = 0
BB_LIN_SCALE = 1
BB_LOG_FULL_SCALE = 2
BB_LIN_FULL_SCALE = 3

# bbConfigureSweepCoupling: rbwShape
BB_RBW_SHAPE_NUTTALL = 0
BB_RBW_SHAPE_FLATTOP = 1
BB_RBW_SHAPE_CISPR = 2

# bbConfigureAcquisition: detector
BB_MIN_AND_MAX = 0
BB_AVERAGE = 1

# bbConfigureProcUnits: units
BB_LOG = 0
BB_VOLTAGE = 1
BB_POWER = 2
BB_SAMPLE = 3

# bbConfigureDemod: modulationType
BB_DEMOD_AM = 0
BB_DEMOD_FM = 1
BB_DEMOD_USB = 2
BB_DEMOD_LSB = 3
BB_DEMOD_CW = 4

# Streaming flags
BB_STREAM_IQ = 0x0
BB_DIRECT_RF = 0x2 # BB60C/D only
BB_TIME_STAMP = 0x10

# BB60C/A bbConfigureIO, port1
BB60C_PORT1_AC_COUPLED = 0x00
BB60C_PORT1_DC_COUPLED = 0x04
BB60C_PORT1_10MHZ_USE_INT = 0x00
BB60C_PORT1_10MHZ_REF_OUT = 0x100
BB60C_PORT1_10MHZ_REF_IN = 0x8
BB60C_PORT1_OUT_LOGIC_LOW = 0x14
BB60C_PORT1_OUT_LOGIC_HIGH = 0x1C
# BB60C/A bbConfigureIO, port2
BB60C_PORT2_OUT_LOGIC_LOW = 0x00
BB60C_PORT2_OUT_LOGIC_HIGH = 0x20
BB60C_PORT2_IN_TRIG_RISING_EDGE = 0x40
BB60C_PORT2_IN_TRIG_FALLING_EDGE = 0x60

# BB60D bbConfigureIO, port1
BB60D_PORT1_DISABLED = 0
BB60D_PORT1_10MHZ_REF_IN = 1
# BB60D bbConfigureIO, port2
BB60D_PORT2_DISABLED = 0
BB60D_PORT2_10MHZ_REF_OUT = 1
BB60D_PORT2_IN_TRIG_RISING_EDGE = 2
BB60D_PORT2_IN_TRIG_FALLING_EDGE = 3
BB60D_PORT2_OUT_LOGIC_LOW = 4
BB60D_PORT2_OUT_LOGIC_HIGH = 5
BB60D_PORT2_OUT_UART = 6

# BB60D only
# bbSetUARTRate, rate
BB60D_UART_BAUD_4_8K = 0
BB60D_UART_BAUD_9_6K = 1
BB60D_UART_BAUD_19_2K = 2
BB60D_UART_BAUD_38_4K = 3
BB60D_UART_BAUD_14_4K = 4
BB60D_UART_BAUD_28_8K = 5
BB60D_UART_BAUD_57_6K = 6
BB60D_UART_BAUD_115_2K = 7
BB60D_UART_BAUD_125K = 8
BB60D_UART_BAUD_250K = 9
BB60D_UART_BAUD_500K = 10
BB60D_UART_BAUD_1000K = 11

# For sweep antenna switching and pseudo-doppler
BB60D_MIN_UART_STATES = 2
BB60D_MAX_UART_STATES = 8

# bbStoreTgThru: flag
TG_THRU_0DB = 0x1
TG_THRU_20DB = 0x2

# bbSetTgReference: reference
TG_REF_UNUSED = 0
TG_REF_INTERNAL_OUT = 1
TG_REF_EXTERNAL_IN = 2 # TG124 only


# --------------------------------- Mappings ----------------------------------

bbGetSerialNumberList = bblib.bbGetSerialNumberList
bbGetSerialNumberList.argtypes = [
    numpy.ctypeslib.ndpointer(c_int, ndim=1, flags='C'),
    POINTER(c_int)
]
bbGetSerialNumberList2 = bblib.bbGetSerialNumberList2
bbGetSerialNumberList2.argtypes = [
    numpy.ctypeslib.ndpointer(c_int, ndim=1, flags='C'),
    numpy.ctypeslib.ndpointer(c_int, ndim=1, flags='C'),
    POINTER(c_int)
]

bbOpenDevice = bblib.bbOpenDevice
bbOpenDeviceBySerialNumber = bblib.bbOpenDeviceBySerialNumber
bbCloseDevice = bblib.bbCloseDevice

# Power state functions BB60D only
bbSetPowerState = bblib.bbSetPowerState
bbGetPowerState = bblib.bbGetPowerState

bbPreset = bblib.bbPreset
bbPresetFull = bblib.bbPresetFull

# Self cal function BB60A only
bbSelfCal = bblib.bbSelfCal

bbGetSerialNumber = bblib.bbGetSerialNumber
bbGetDeviceType = bblib.bbGetDeviceType
bbGetFirmwareVersion = bblib.bbGetFirmwareVersion
bbGetDeviceDiagnostics = bblib.bbGetDeviceDiagnostics

bbConfigureIO = bblib.bbConfigureIO

bbSyncCPUtoGPS = bblib.bbSyncCPUtoGPS

# UART functions BB60D only
bbSetUARTRate = bblib.bbSetUARTRate
bbEnableUARTSweeping = bblib.bbEnableUARTSweeping
bbEnableUARTSweeping.argtypes = [
    c_int,
    numpy.ctypeslib.ndpointer(c_double, ndim=1, flags='C'),
    numpy.ctypeslib.ndpointer(c_uint8, ndim=1, flags='C'),
    c_int
]
bbDisableUARTSweeping = bblib.bbDisableUARTSweeping
bbEnableUARTStreaming = bblib.bbEnableUARTStreaming
bbEnableUARTStreaming.argtypes = [
    c_int,
    numpy.ctypeslib.ndpointer(c_uint8, ndim=1, flags='C'),
    numpy.ctypeslib.ndpointer(c_uint32, ndim=1, flags='C'),
    c_int
]
bbDisableUARTStreaming = bblib.bbDisableUARTStreaming
bbWriteUARTImm = bblib.bbWriteUARTImm

bbConfigureRefLevel = bblib.bbConfigureRefLevel
bbConfigureGainAtten = bblib.bbConfigureGainAtten

bbConfigureCenterSpan = bblib.bbConfigureCenterSpan
bbConfigureSweepCoupling = bblib.bbConfigureSweepCoupling
bbConfigureAcquisition = bblib.bbConfigureAcquisition
bbConfigureProcUnits = bblib.bbConfigureProcUnits

bbConfigureRealTime = bblib.bbConfigureRealTime
bbConfigureRealTimeOverlap = bblib.bbConfigureRealTimeOverlap

bbConfigureIQCenter = bblib.bbConfigureIQCenter
bbConfigureIQ = bblib.bbConfigureIQ
bbConfigureIQDataType = bblib.bbConfigureIQDataType
bbConfigureIQTriggerSentinel = bblib.bbConfigureIQTriggerSentinel

# Audio demod
bbConfigureDemod = bblib.bbConfigureDemod

bbInitiate = bblib.bbInitiate
bbAbort = bblib.bbAbort

bbQueryTraceInfo = bblib.bbQueryTraceInfo
bbQueryRealTimeInfo = bblib.bbQueryRealTimeInfo
bbQueryRealTimePoi = bblib.bbQueryRealTimePoi
bbQueryIQParameters = bblib.bbQueryIQParameters
bbGetIQCorrection = bblib.bbGetIQCorrection

bbFetchTrace_32f = bblib.bbFetchTrace_32f
bbFetchTrace_32f.argtypes = [
    c_int,
    c_int,
    numpy.ctypeslib.ndpointer(numpy.float32, ndim=1, flags='C'),
    numpy.ctypeslib.ndpointer(numpy.float32, ndim=1, flags='C')
]
bbFetchTrace = bblib.bbFetchTrace
bbFetchTrace.argtypes = [
    c_int,
    c_int,
    numpy.ctypeslib.ndpointer(numpy.float64, ndim=1, flags='C'),
    numpy.ctypeslib.ndpointer(numpy.float64, ndim=1, flags='C')
]
bbFetchRealTimeFrame = bblib.bbFetchRealTimeFrame
bbFetchRealTimeFrame.argtypes = [
    c_int,
    numpy.ctypeslib.ndpointer(numpy.float32, ndim=1, flags='C'),
    numpy.ctypeslib.ndpointer(numpy.float32, ndim=1, flags='C'),
    numpy.ctypeslib.ndpointer(numpy.float32, ndim=1, flags='C'),
    numpy.ctypeslib.ndpointer(numpy.float32, ndim=1, flags='C')
]
bbGetIQUnpacked = bblib.bbGetIQUnpacked
bbGetIQUnpacked.argtypes = [
    c_int,
    numpy.ctypeslib.ndpointer(numpy.complex64, ndim=1, flags='C'),
    c_int,
    POINTER(c_int),
    c_int,
    c_int,
    POINTER(c_int),
    POINTER(c_int),
    POINTER(c_int),
    POINTER(c_int)
]
bbFetchAudio = bblib.bbFetchAudio
bbFetchAudio.argtypes = [
    c_int,
    numpy.ctypeslib.ndpointer(numpy.float32, ndim=1, flags='C')
]

bbAttachTg = bblib.bbAttachTg
bbIsTgAttached = bblib.bbIsTgAttached
bbConfigTgSweep = bblib.bbConfigTgSweep
bbStoreTgThru = bblib.bbStoreTgThru
bbSetTg = bblib.bbSetTg
bbGetTgFreqAmpl = bblib.bbGetTgFreqAmpl
bbSetTgReference = bblib.bbSetTgReference

bbGetAPIVersion = bblib.bbGetAPIVersion
bbGetAPIVersion.restype = c_char_p
bbGetProductID = bblib.bbGetProductID
bbGetProductID.restype = c_char_p
bbGetErrorString = bblib.bbGetErrorString
bbGetErrorString.restype = c_char_p


# ---------------------------------- Utility ----------------------------------

def error_check(func):
    def print_status_if_error(*args, **kwargs):
        return_vars = func(*args, **kwargs)
        if "status" not in return_vars.keys():
            return return_vars
        status = return_vars["status"]
        if status != 0:
            print (f"{'Error' if status < 0 else 'Warning'} {status}: {bb_get_error_string(status)} in {func.__name__}()")
        if status < 0:
            exit()
        return return_vars
    return print_status_if_error


# --------------------------------- Functions ---------------------------------

@error_check
def bb_get_serial_number_list():
    serials = numpy.zeros(BB_MAX_DEVICES).astype(c_int)
    device_count = c_int(-1)
    status = bbGetSerialNumberList(serials, byref(device_count))
    return {
        "status": status,
        "serials": serials,
        "device_count": device_count
    }

@error_check
def bb_get_serial_number_list_2():
    serials = numpy.zeros(BB_MAX_DEVICES).astype(c_int)
    device_types = numpy.zeros(BB_MAX_DEVICES).astype(c_int)
    device_count = c_int(-1)
    status = bbGetSerialNumberList2(serials, device_types, byref(device_count))
    return {
        "status": status,
        "serials": serials,
        "device_types": device_types,
        "device_count": device_count
    }

@error_check
def bb_open_device():
    device = c_int(-1)
    status = bbOpenDevice(byref(device))
    return {
        "status": status,
        "handle": device.value
    }

@error_check
def bb_open_device_by_serial_number(serial_number):
    device = c_int(-1)
    status = bbOpenDeviceBySerialNumber(byref(device), serial_number)
    return {
        "status": status,
        "handle": device.value
    }

@error_check
def bb_close_device(device):
    return {
        "status": bbCloseDevice(device)
    }

@error_check
def bb_set_power_state(device, power_state):
    return {
        "status": bbSetPowerState(device, power_state)
    }

@error_check
def bb_get_power_state(device):
    power_state = c_int(-1)
    status = bbGetPowerState(device, byref(power_state))
    return {
        "status": status,
        "power_state": power_state.value
    }

@error_check
def bb_preset(device):
    return {
        "status": bbPreset()
    }

@error_check
def bb_preset_full(device):
    handle = c_int(device)
    status = bbPresetFull(byref(handle))
    return {
        "status": status,
        "handle": handle.value
    }

@error_check
def bb_self_cal(device):
    return {
        "status": bbSelfCal()
    }

@error_check
def bb_get_serial_number(device):
    serial = c_uint32(-1)
    status = bbGetSerialNumber(device, byref(serial))
    return {
        "status": status,
        "serial": serial.value
    }

@error_check
def bb_get_device_type(device):
    device_type = c_int(-1)
    status = bbGetDeviceType(device, byref(device_type))
    return {
        "status": status,
        "device_type": device_type.value
    }

@error_check
def bb_get_firmware_version(device):
    version = c_int(-1)
    status = bbGetFirmwareVersion(device, byref(version))
    return {
        "status": status,
        "version": version.value
    }

@error_check
def bb_get_device_diagnostics(device):
    temperature = c_float(-1)
    usb_voltage = c_float(-1)
    usb_current = c_float(-1)
    status = bbGetDeviceDiagnostics(device, byref(temperature), byref(usb_voltage), byref(usb_current))
    return {
        "status": status,
        "temperature": temperature.value,
        "usb_voltage": usb_voltage.value,
        "usb_current": usb_current.value
    }

@error_check
def bb_configure_IO(device, port1, port2):
    return {
        "status": bbConfigureIO(device, port1, port2)
    }

@error_check
def bb_sync_CPU_to_GPS(device, com_port, baud_rate):
    return {
        "status": bbSyncCPUtoGPS(com_port, baud_rate)
    }

@error_check
def bb_set_UART_rate(device, rate):
    return {
        "status": bbSetUARTRate(device, rate)
    }

@error_check
def bb_enable_UART_sweeping(device, freqs, data, states):
    return {
        "status": bbEnableUARTSweeping(device, freqs, data, states)
    }

@error_check
def bb_disable_UART_sweeping(device):
    return {
        "status": bbDisableUARTSweeping(device)
    }

@error_check
def bb_enable_UART_streaming(device, data, counts, states):
    return {
        "status": bbEnableUARTStreaming(device, data, counts, states)
    }

@error_check
def bb_disable_UART_streaming(device):
    return {
        "status": bbDisableUARTStreaming(device)
    }

@error_check
def bbWriteUARTImm(device, data):
    return {
        "status": bbWriteUARTImm(device, data)
    }

@error_check
def bb_configure_ref_level(device, ref_level):
    return {
        "status": bbConfigureRefLevel(device, c_double(ref_level))
    }

@error_check
def bb_configure_gain_atten(device, gain, atten):
    return {
        "status": bbConfigureGainAtten(device, gain, atten)
    }

@error_check
def bb_configure_center_span(device, center, span):
    return {
        "status": bbConfigureCenterSpan(device, c_double(center), c_double(span))
    }

@error_check
def bb_configure_sweep_coupling(device, rbw, vbw, sweep_time, rbw_shape, rejection):
    return {
        "status": bbConfigureSweepCoupling(device, c_double(rbw), c_double(vbw), c_double(sweep_time), rbw_shape, rejection)
    }

@error_check
def bb_configure_acquisition(device, detector, scale):
    return {
        "status": bbConfigureAcquisition(device, detector, scale)
    }

@error_check
def bb_configure_proc_units(device, units):
    return {
        "status": bbConfigureProcUnits(device, units)
    }

@error_check
def bb_configure_real_time(device, frame_scale, frame_rate):
    return {
        "status": bbConfigureRealTime(device, c_double(frame_scale), frame_rate)
    }

@error_check
def bb_configure_real_time_overlap(device, advance_rate):
    return {
        "status": bbConfigureRealTimeOverlap(device, c_double(advance_rate))
    }

@error_check
def bb_configure_IQ_center(device, center_freq):
    return {
        "status": bbConfigureIQCenter(device, c_double(center_freq))
    }

@error_check
def bb_configure_IQ(device, downsample_factor, bandwidth):
    return {
        "status": bbConfigureIQ(device, downsample_factor, c_double(bandwidth))
    }

@error_check
def bb_configure_IQ_data_type(device, data_type):
    return {
        "status": bbConfigureIQDataType(device, data_type)
    }

@error_check
def bb_configure_IQ_trigger_sentinel(device, sentinel):
    return {
        "status": bbConfigureIQTriggerSentinel(device, sentinel)
    }

@error_check
def bb_configure_demod(device, modulation_type, freq, IFBW, audio_low_pass_freq, audio_high_pass_freq, FM_deemphasis):
    return {
        "status": bbConfigureDemod(device, modulation_type, c_double(freq), c_float(IFBW), c_float(audio_low_pass_freq), c_float(audio_high_pass_freq), c_float(FM_deemphasis))
    }

@error_check
def bb_initiate(device, mode, flag):
    return {
        "status": bbInitiate(device, mode, flag)
    }

@error_check
def bb_abort(device):
    return {
        "status": bbAbort(device)
    }

@error_check
def bb_query_trace_info(device):
    trace_len = c_int(-1)
    bin_size = c_double(-1)
    start = c_double(-1)
    status = bbQueryTraceInfo(device, byref(trace_len), byref(bin_size), byref(start))
    return {
        "status": status,
        "trace_len": trace_len.value,
        "bin_size": bin_size.value,
        "start": start.value
    }

@error_check
def bb_query_real_time_info(device):
    frame_width = c_int(-1)
    frame_height = c_int(-1)
    status = bbQueryRealTimeInfo(device, byref(frame_width), byref(frame_height))
    return {
        "status": status,
        "frame_width": frame_width.value,
        "frame_height": frame_height.value
    }

@error_check
def bb_query_real_time_poi(device):
    poi = c_double(-1)
    status = bbQueryRealTimePoi(device, byref(poi))
    return {
        "status": status,
        "poi": poi.value
    }

@error_check
def bb_query_IQ_parameters(device):
    sample_rate = c_double(-1)
    bandwidth = c_double(-1)
    status = bbQueryIQParameters(device, byref(sample_rate), byref(bandwidth))
    return {
        "status": status,
        "sample_rate": sample_rate.value,
        "bandwidth": bandwidth.value
    }

@error_check
def bb_get_IQ_correction(device):
    correction = c_float(-1)
    status = bbGetIQCorrection(device, byref(correction))
    return {
        "status": status,
        "correction": correction.value
    }

@error_check
def bb_fetch_trace_32f(device, array_size):
    trace_min = numpy.zeros(array_size).astype(numpy.float32)
    trace_max = numpy.zeros(array_size).astype(numpy.float32)
    status = bbFetchTrace_32f(device, array_size, trace_min, trace_max)
    return {
        "status": status,
        "trace_min": trace_min,
        "trace_max": trace_max
    }

@error_check
def bb_fetch_trace(device, array_size):
    trace_min = numpy.zeros(array_size).astype(numpy.float64)
    trace_max = numpy.zeros(array_size).astype(numpy.float64)
    status = bbFetchTrace(device, array_size, trace_min, trace_max)
    return {
        "status": status,
        "trace_min": trace_min,
        "trace_max": trace_max
    }

@error_check
def bb_fetch_real_time_frame(device):
    ret = bb_query_trace_info(device)
    if ret["status"] != 0:
        return {
            "status": ret["status"]
        }
    trace_len = ret["trace_len"]

    ret = bb_query_real_time_info(device)
    if ret["status"] != 0:
        return {
            "status": ret["status"]
        }
    frame_width = ret["frame_width"]
    frame_height = ret["frame_height"]

    trace_min = numpy.zeros(trace_len).astype(numpy.float32)
    trace_max = numpy.zeros(trace_len).astype(numpy.float32)
    frame = numpy.zeros(frame_width * frame_height).astype(numpy.float32)
    alpha_frame = numpy.zeros(frame_width * frame_height).astype(numpy.float32)

    status = bbFetchRealTimeFrame(device,
                                  trace_min, trace_max,
                                  frame, alpha_frame)
    return {
        "status": status,
        "trace_min": trace_min,
        "trace_max": trace_max,
        "frame": frame,
        "alpha_frame": alpha_frame
    }

@error_check
def bb_get_IQ_unpacked(device, iq_count, purge, triggers = c_int(0), trigger_count = 0):
    iq_data = numpy.zeros(iq_count).astype(numpy.complex64)
    data_remaining = c_int(-1)
    sample_loss = c_int(-1)
    sec = c_int(-1)
    nano = c_int(-1)
    status = bbGetIQUnpacked(device, iq_data, iq_count, triggers, trigger_count, purge, byref(data_remaining), byref(sample_loss), byref(sec), byref(nano))
    return {
        "status": status,
        "iq": iq_data,
        "data_remaining": data_remaining.value,
        "sample_loss": sample_loss.value,
        "sec": sec.value,
        "nano": nano.value
    }

@error_check
def bb_fetch_audio(device):
    audio = numpy.zeros(4096).astype(numpy.float32)
    status = bbFetchAudio(device, audio)
    return {
        "status": status,
        "audio": audio
    }

@error_check
def bb_attach_TG(device):
    return {
        "status": bbAttachTg(device)
    }

@error_check
def bb_is_TG_attached(device):
    is_attached = c_bool(False)
    status = bbIsTgAttached(device, byref(is_attached))
    return {
        "status": status,
        "is_attached": is_attached.value
    }

@error_check
def bb_config_TG_sweep(device, sweep_size, high_dynamic_range, passive_device):
    return {
        "status": bbConfigTgSweep(device, sweep_size, high_dynamic_range, passive_device)
    }

@error_check
def bb_store_TG_thru(device, flag):
    return {
        "status": bbStoreTgThru(device, flag)
    }

@error_check
def bb_set_TG(device, frequency, amplitude):
    return {
        "status": bbSetTg(device, c_double(frequency), c_double(amplitude))
    }

@error_check
def bb_get_TG_freq_ampl(device):
    frequency = c_double(-1)
    amplitude = c_double(-1)
    status = bbGetTgFreqAmpl(byref(frequency), byref(amplitude))
    return {
        "status": status,
        "frequency": frequency,
        "amplitude": amplitude
    }

@error_check
def bb_set_TG_reference(device, reference):
    return {
        "status": bbSetTgReference(device, reference)
    }

def bb_get_API_version():
    return {
        "api_version": bbGetAPIVersion()
    }


def bb_get_product_ID():
    return {
        "product_id": bbGetProductID()
    }

def bb_get_error_string(status):
    return {
        "error_string": bbGetErrorString(status)
    }

# Deprecated functions, use suggested alternatives

# Use bbConfigureRefLevel instead
bbConfigureLevel = bblib.bbConfigureLevel
@error_check
def bb_configure_level(device, ref, atten):
    return {
        "status": bbConfigureLevel(device, c_double(ref), atten)
    }

# Use bbConfigureGainAtten instead
bbConfigureGain = bblib.bbConfigureGain
@error_check
def bb_configure_gain(device, gain):
    return {
        "status": bbConfigureGain(device, gain)
    }

# Use bbQueryIQParameters instead
bbQueryStreamInfo = bblib.bbQueryStreamInfo
@error_check
def bb_query_stream_info(device):
    return_len = c_int(-1)
    bandwidth = c_double(-1)
    samples_per_sec = c_int(-1)
    status = bbQueryStreamInfo(device, byref(return_len), byref(bandwidth), byref(samples_per_sec))
    return {
        "status": status,
        "return_len": return_len.value,
        "bandwidth": bandwidth.value,
        "samples_per_sec": samples_per_sec.value
    }

# Deprecated macros, use alternatives where available
BB60_MIN_FREQ = c_double(BB_MIN_FREQ.value)
BB60_MAX_FREQ = c_double(BB_MAX_FREQ.value)
BB60_MAX_SPAN = c_double(BB_MAX_SPAN.value)
BB_MIN_BW = c_double(BB_MIN_RBW.value)
BB_MAX_BW = c_double(BB_MAX_RBW.value)
BB_MAX_ATTENUATION = c_double(30.0) # For deprecated bbConfigureLevel function
BB60C_MAX_GAIN = BB_MAX_GAIN
BB_PORT1_INT_REF_OUT = 0x00 # use BB_PORT1_10MHZ_USE_INT
BB_PORT1_EXT_REF_IN = BB60C_PORT1_10MHZ_REF_IN
BB_RAW_PIPE = BB_STREAMING # use BB_STREAMING
BB_STREAM_IF = 0x1 # No longer supported
# Use new device specific port 1 macros
BB_PORT1_AC_COUPLED = BB60C_PORT1_AC_COUPLED
BB_PORT1_DC_COUPLED = BB60C_PORT1_DC_COUPLED
BB_PORT1_10MHZ_USE_INT = BB60C_PORT1_10MHZ_USE_INT
BB_PORT1_10MHZ_REF_OUT = BB60C_PORT1_10MHZ_REF_OUT
BB_PORT1_10MHZ_REF_IN = BB60C_PORT1_10MHZ_REF_IN
BB_PORT1_OUT_LOGIC_LOW = BB60C_PORT1_OUT_LOGIC_LOW
BB_PORT1_OUT_LOGIC_HIGH = BB60C_PORT1_OUT_LOGIC_HIGH
# Use new device specific port 2 macros
BB_PORT2_OUT_LOGIC_LOW = BB60C_PORT2_OUT_LOGIC_LOW
BB_PORT2_OUT_LOGIC_HIGH = BB60C_PORT2_OUT_LOGIC_HIGH
BB_PORT2_IN_TRIGGER_RISING_EDGE = BB60C_PORT2_IN_TRIG_RISING_EDGE
BB_PORT2_IN_TRIGGER_FALLING_EDGE = BB60C_PORT2_IN_TRIG_FALLING_EDGE
