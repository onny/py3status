# -*- coding: utf-8 -*-
"""
A simple stopwatch.

This is a very basic stopwatch. You can start, pause and reset the
stopwatch.

Button 1 starts/pauses the stopwatch.
Button 2 resets stopwatch.

Configuration parameters:
    format: display format for this module (default 'Stopwatch {stopwatch}')

Format placeholders:
    {stopwatch} display hours:minutes:seconds

@author Jonas Heinrich

SAMPLE OUTPUT
{'full_text': 'Stopwatch 0:01:00'}

running
[
    {'full_text': 'Stopwatch '},
    {'color': '#00FF00', 'full_text': '0'},
    {'full_text': ':'},
    {'color': '#00FF00', 'full_text': '00'},
    {'full_text': ':'},
    {'color': '#00FF00', 'full_text': '54'},
]

paused
[
    {'full_text': 'Stopwatch '},
    {'color': '#FFFF00', 'full_text': '0'},
    {'full_text': ':'},
    {'color': '#FFFF00', 'full_text': '00'},
    {'full_text': ':'},
    {'color': '#FFFF00', 'full_text': '54'},
]
"""

from time import time
from threading import Timer


class Py3status:
    """
    """
    # available configuration parameters
    format = 'Stopwatch {stopwatch}'

    def post_config_hook(self):
        self.running = False
        self.time_start = None
        self.time_state = None
        self.color = None
        self.paused = False

    def stopwatch(self):

        def make_2_didget(value):
            value = str(value)
            if len(value) == 1:
                value = '0' + value
            return value

        if self.running:
            t = int(time() - self.time_start)
        else:
            if self.time_state:
                t = self.time_state
            else:
                t = 0

        # Hours
        hours, t = divmod(t, 3600)
        # Minutes
        mins, t = divmod(t, 60)
        # Seconds
        seconds = t

        if self.running:
            cached_until = self.py3.time_in(0, offset=1)
        else:
            cached_until = self.py3.CACHE_FOREVER

        composites = [
            {
                'full_text': str(hours),
                'color': self.color,
                'index': 'hours',
            },
            {
                'color': '#CCCCCC',
                'full_text': ':',
            },
            {
                'full_text': make_2_didget(mins),
                'color': self.color,
                'index': 'mins',
            },
            {
                'color': '#CCCCCC',
                'full_text': ':',
            },
            {
                'full_text': make_2_didget(seconds),
                'color': self.color,
                'index': 'seconds',
            },
        ]

        stopwatch = self.py3.composite_create(composites)

        return {
            'cached_until': cached_until,
            'full_text': self.py3.safe_format(self.format, {'stopwatch': stopwatch})
        }

    def on_click(self, event):
        deltas = {
            'hours': 3600,
            'mins': 60,
            'seconds': 1
        }
        index = event['index']
        button = event['button']

        if button == 1:
            if self.running:
                # pause stopwatch
                self.running = False
                self.paused = True
                self.time_state = int(time() - self.time_start)
                self.color = '#FFFF00'
            else:
                # start/restart stopwatch
                if self.paused:
                    self.time_start = int(time() - self.time_state)
                    self.running = True
                else:
                    self.time_start = time()
                    self.running = True
                self.color = '#00FF00'

        if button == 2:
            # reset and pause stopwatch
            self.running = False
            self.paused = False
            self.time_state = None
            self.color = None

        if not self.running:
            # change timer section HH:MM:SS
            t = self.time_state


if __name__ == "__main__":
    """
    Run module in test mode.
    """
    from py3status.module_test import module_test
    module_test(Py3status)
