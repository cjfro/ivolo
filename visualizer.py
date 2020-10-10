# from https://raw.githubusercontent.com/IzzyBrand/ledvis/0b51564b47a70eb9d21d5f149e517cbfbcdb0e4f/visualizer.py

import numpy as np
import masker
import time
from config import *
from sound_processing import *


class VisualizerBase:
    '''
    Base class for the visualizer. This structure takes in incoming audio data and generates
    output colors for the LED strips
    '''
    def __init__(self):
        self.name = self.__class__.__name__

    def visualize(self, sample_array):
        return np.zeros([LED_1_COUNT, 3], dtype=int)

class ExampleVisualizer(VisualizerBase):
    def __init__(self):
        VisualizerBase.__init__(self)
        self.bounder = Bounder()

    def visualize(self, sample_array):
        self.bounder.update(sample_array) # update the max and min observed sample
        m = sample_array[-1] # pull out the most recent sample
        m = self.bounder.normalize(most_recent_sample) # normalize it to be from 0 to 1

        # make an array with LED_1_COUNT elements, where one entry is 255 and the rest are zeros.
        color_channel = 255 * (np.arrange(LED_1_COUNT) == int(m * LED_1_COUNT))

        # there are three color channels. repeating the same array three times yields white
        return np.vstack([color_channel, color_channel, color_channel]).T


class StripsOff(VisualizerBase):
    def visualize(self, sample_array):
        color_array = np.zeros([LED_1_COUNT,3], dtype=int)
        return color_array


class VooMeter(VisualizerBase):
    def __init__(self, color=np.array([120, 200, 100]), mask_maker=masker.middle_out):
        VisualizerBase.__init__(self)
        self.color = np.random.randint(low=0, high=255, size=3)
        self.mask_maker = mask_maker
        self.smoother = SplitExponentialMovingAverage(0.2, 0.7)
        self.bounder = Bounder()
        self.bounder.L_contraction_rate = 0.999
        self.bounder.L_contraction_rate = 0.9

    def visualize(self, sample_array):
        m = np.max(sample_array[-300:]) # get the maximum amplitude
        m = self.bounder.update_and_normalize(m) # normalize the amplitude to [0,1]
        m = self.smoother.smooth(m) # and smooth it

        color_mask = self.mask_maker(m) # create a mask of which LEDS to turn on

        # create a color array to be sent to the LED_writer
        return color_mask * self.color
