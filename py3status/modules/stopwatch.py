# -*- coding: utf-8 -*-
"""
A simple stopwatch.

This module is able to start tracking the amount of time elapsed
when activated through a mouse click. The stopwatch can also be
paused, resumed and with a different mouse button, reset to zero.

Configuration parameters:
    button_reset: mouse button to reset the stopwatch (default 2)
    button_toggle: mouse button to start/stop the stopwatch (default 1)
    format: display format for this module (default 'Stopwatch {stopwatch}')

Format placeholders:
    {stopwatch} display hours:minutes:seconds

@author Jonas Heinrich

SAMPLE OUTPUT
{'full_text': 'Stopwatch 0:00:00'}

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
    {'color': '#FFFF00', 'full_text': '58'},
]
"""

from time import time


class Py3status:
    """
    """
    # available configuration parameters
    button_reset = 2
    button_toggle = 1
    format = 'Stopwatch {stopwatch}'

    def post_config_hook(self):
        self.time_start = None
        self._reset_time()

    def _reset_time(self):
        self.running = False
        self.paused = False
        self.time_state = None
        self.color = None

    def stopwatch(self):
        if self.running:
            cached_until = self.py3.time_in(0, offset=1)
            t = int(time() - self.time_start)
        else:
            cached_until = self.py3.CACHE_FOREVER
            if self.time_state:
                t = self.time_state
            else:
                t = 0

        hours, t = divmod(t, 3600)
        minutes, t = divmod(t, 60)
        seconds = t

        stopwatch = self.py3.safe_format('\?color=%s %d:%02d:%02d' % (
            self.color, hours, minutes, seconds))

        return {
            'cached_until': cached_until,
            'full_text': self.py3.safe_format(
                self.format, {'stopwatch': stopwatch}
            )
        }

    def on_click(self, event):
        button = event['button']

        if button == self.button_toggle:
            if self.running:
                # pause stopwatch
                self.running = False
                self.paused = True
                self.time_state = int(time() - self.time_start)
                self.color = self.py3.COLOR_DEGRADED
            else:
                self.color = self.py3.COLOR_GOOD
                self.running = True
                # start/restart stopwatch
                if self.paused:
                    self.time_start = int(time() - self.time_state)
                else:
                    self.time_start = time()
        elif button == self.button_reset:
            # reset and pause stopwatch
            self._reset_time()
        else:
            self.py3.prevent_refresh()


if __name__ == "__main__":
    """
    Run module in test mode.
    """
    from py3status.module_test import module_test
    module_test(Py3status)
