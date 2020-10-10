#!/usr/bin/env python
from ctypes import *
import pyaudio
import numpy as np
import matplotlib.pyplot as plt
import time
import sys
from rpi_ws281x import PixelStrip, Color
from config import *
from visualizer import *

# Silence the Raspberry PI logger
# Define our error handler type
# ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)
# def py_error_handler(filename, line, function, err, fmt):
#   pass
# c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)
# asound = cdll.LoadLibrary('libasound.so')
# asound.snd_lib_error_set_handler(c_error_handler) # Set error handler

CHUNK = 1024*4  # CHUNKS of bytes to read each time from mic
FORMAT = pyaudio.paInt16
CHANNELS = 1
MIC_NAME = 'USB PnP Audio Device: Audio'
# MIC_NAME = 'MacBook Pro Microphone'

# Initial Plots
i=0
f,ax = plt.subplots(2)

# Prepare the Plotting Environment with random starting values
x = np.arange(10000)
y = np.random.randn(10000)

# Plot 0 is for raw audio data
li, = ax[0].plot(x, y)
ax[0].set_xlim(0,1000)
ax[0].set_ylim(-5000,5000)
ax[0].set_title("Raw Audio Signal")
# Plot 1 is for the FFT of the audio
li2, = ax[1].plot(x, y)
ax[1].set_xlim(0,5000)
ax[1].set_ylim(-100,100)
ax[1].set_title("Fast Fourier Transform")
# Show the plot, but without blocking updates
plt.tight_layout()
plt.subplots_adjust(hspace=0.3)
plt.pause(0.01)

# let's always keep going!
global keep_going
keep_going = True

# Initialize PyAudio
p = pyaudio.PyAudio()

# setup visualizer
visualizer = VooMeter()
strip = PixelStrip(LED_1_COUNT, LED_1_PIN, LED_1_FREQ_HZ, LED_1_DMA, LED_1_INVERT, LED_1_BRIGHTNESS, LED_1_CHANNEL)
strip.begin()

def get_device():
    for ii in range(p.get_device_count()):
        dev = p.get_device_info_by_index(ii)
        name = dev.get('name')
        print (dev)
        if MIC_NAME in name:
            device = {
                'name': name,
                'index': ii,
                'channels': int(dev.get('maxInputChannels')),
                'rate': int(dev.get('defaultSampleRate')),
                'input_latency': dev.get('defaultHighInputLatency')
            }
            print('Found mic at channel', device)
            return device
    return None

def process(buffer):
    plot_data(buffer)
    draw(buffer)

def draw(samples):
    colors = visualizer.visualize(samples)
    for i in range(min(strip.numPixels(), len(samples))):
        print(i, colors[i])
        strip.setPixelColorRGB(i, int(colors[i][0]), int(colors[i][1]), int(colors[i][2]), int(colors[i][2]))
    strip.show()

def plot_data(samples):
    # Fast Fourier Transform, 10*log10(abs) is to scale it to dB
    # and make sure it's not imaginary
    dfft = 10.*np.log10(abs(np.fft.rfft(samples)))

    # Force the new data into the plot, but without redrawing axes.
    li.set_xdata(np.arange(len(samples)))
    li.set_ydata(samples)
    li2.set_xdata(np.arange(len(dfft))*10.)
    li2.set_ydata(dfft)

    # Show the updated plot, but without blocking
    plt.pause(0.01)
    # print('plot updated')
    if keep_going:
        return True
    else:
        return False

# find the device
device = get_device()
if device == None:
    print('Failed to find mic!')
    import sys; sys.exit()
else:
    print('Found device', device['index'])

# open the stream
stream = p.open(format=pyaudio.paInt16,
                channels=CHANNELS,
                rate=device['rate'],
                input=True,
                frames_per_buffer=CHUNK);

# Open the connection and start streaming the data
stream.start_stream()
print("\n+---------------------------------+")
print("| Press Ctrl+C to Break Recording |")
print( "+---------------------------------+\n")

# Loop so program doesn't end while the stream is open
while keep_going:
    try:
        data = stream.read(CHUNK, exception_on_overflow = False)
        samples = np.fromstring(data, dtype="int16")
        process(samples)
    except KeyboardInterrupt:
        keep_going=False
    except OSError as err:
        print("OS error: {0}".format(err))
        break
    except:
        print("Unexpected error:", sys.exc_info())
        import traceback; traceback.print_exc()
        break

# Close up shop
stream.stop_stream()
stream.close()
