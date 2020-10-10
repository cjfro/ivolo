import numpy as np

# PYAUDIO CONFIGURATION
CHUNK_SIZE 		= 2**10 	 # How many audio samples to read in per step
FORMAT 			= 8
NUM_CHANNELS 	= 1      # Number of audio channels
SAMPLING_FREQ	= 44100  # Sampling frequency of incoming audio
DEVICE_INDEX 	= 0      # Which audio device to read from (listed in pyaudio_test.py)

# LED STRIPS CONFIGURATION
LED_1_COUNT      = 60     # Number of LED pixels.
LED_1_PIN        = 18      # GPIO pin connected to the pixels (must support PWM! GPIO 13 and 18 on RPi 3).
LED_1_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_1_DMA        = 10      # DMA channel to use for generating signal (Between 1 and 14)
LED_1_BRIGHTNESS = 255      # Set to 0 for darkest and 255 for brightest
LED_1_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_1_CHANNEL    = 0       # 0 or 1

LED_WRITE_DELAY  = 0.005   # wait (in seconds) after writing to each LED strip
