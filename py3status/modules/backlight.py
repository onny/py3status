# -*- coding: utf-8 -*-
"""
Adjust screen backlight brightness.

Configuration parameters:
    brightness_delta: Change the brightness by this step.
        (default 8)
    brightness_initial: Set brightness to this value on start.
        (default None)
    brightness_minimal: Don't go below this brightness to avoid black screen
        (default 1)
    button_down: Button to click to decrease brightness. Setting to 0 disables.
        (default 5)
    button_up: Button to click to increase brightness. Setting to 0 disables.
        (default 4)
    cache_timeout: How often we refresh this module in seconds (default 10)
    device: Device name or full path to use, eg, acpi_video0 or
        /sys/class/backlight/acpi_video0, otherwise automatic
        (default None)
    format: Display brightness, see placeholders below
        (default '☼: {level}%')
    low_tune_threshold: If current brightness value is below this threshold,
        the value is changed by a minimal value instead of the brightness_delta.
        (default 0)

Format status string parameters:
    {level} brightness

Requires:
    xbacklight: need for changing brightness, not detection

@author Tjaart van der Walt (github:tjaartvdwalt)
@license BSD

SAMPLE OUTPUT
{'full_text': u'\u263c: 100%'}
"""

from __future__ import division

import os

STRING_NOT_AVAILABLE = 'no available device'


def get_device():
    for (path, devices, files) in os.walk('/sys/class/backlight/'):
        for device in devices:
            if 'brightness' in os.listdir(path + device) and \
               'max_brightness' in os.listdir(path + device):
                return path + device


class Py3status:
    """
    """
    # available configuration parameters
    brightness_delta = 8
    brightness_initial = None
    brightness_minimal = 1
    button_down = 5
    button_up = 4
    cache_timeout = 10
    device = None
    format = u'☼: {level}%'
    low_tune_threshold = 0

    class Meta:
        deprecated = {
            'rename': [
                {
                    'param': 'device_path',
                    'new': 'device',
                    'msg': 'obsolete parameter use `device`',
                },
            ],
        }

    def post_config_hook(self):
        if not self.device:
            self.device = get_device()
        elif '/' not in self.device:
            self.device = "/sys/class/backlight/%s" % self.device
        if self.device is None:
            raise Exception(STRING_NOT_AVAILABLE)

        # check for an error code and an output
        self.xbacklight = False
        try:
            if self.py3.command_output(['xbacklight', '-get']):
                self.xbacklight = True
        except:
            pass

        if self.xbacklight and self.brightness_initial:
            self._set_backlight_level(self.brightness_initial)

    def on_click(self, event):
        if not self.xbacklight:
            return None

        level = self._get_backlight_level()
        button = event['button']
        if button == self.button_up:
            delta = self.brightness_delta if level >= self.low_tune_threshold else 1
            level += delta
            if level > 100:
                level = 100
            self._set_backlight_level(level)
        elif button == self.button_down:
            delta = self.brightness_delta if level > self.low_tune_threshold else 1
            level -= delta
            if level < self.brightness_minimal:
                level = self.brightness_minimal
            self._set_backlight_level(level)

    def _set_backlight_level(self, level):
        self.py3.command_run(['xbacklight', '-time', '0', '-set', str(level)])

    def _get_backlight_level(self):
        if self.xbacklight:
            level = self.py3.command_output(['xbacklight', '-get']).strip()
            return round(float(level))
        for brightness_line in open("%s/brightness" % self.device, 'rb'):
            brightness = int(brightness_line)
        for brightness_max_line in open("%s/max_brightness" % self.device, 'rb'):
            brightness_max = int(brightness_max_line)
        return brightness * 100 // brightness_max

    def backlight(self):
        full_text = ""
        if self.device is not None:
            level = self._get_backlight_level()
            full_text = self.py3.safe_format(self.format, {'level': level})

        response = {
            'cached_until': self.py3.time_in(self.cache_timeout),
            'full_text': full_text
        }
        return response


if __name__ == "__main__":
    """
    Run module in test mode.
    """
    from py3status.module_test import module_test
    module_test(Py3status)
