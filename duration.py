'''
File: duration.py
Edited by Samantha Robertson
SUNet ID: srobert4

This file contains the implementation of the Duration
class, which takes a duration of the form  PT[#H][#M][#S]
and converts it to a number of minutes.
'''
import re


class Duration(object):
    def __init__(self, duration_string):
        '''
        This constructor takes a string of the format
        PT[#H][#M][#S] and converts the time to minutes.
        The duration in minutes is stored in self.duration.
        '''
        self.duration = 0

        if not duration_string:
            return

        # Get hours
        hours = re.search('\d+H', duration_string)
        if hours:
            self.duration += float(hours.group(0)[:-1]) * 60

        # Get minutes
        minutes = re.search('\d+M', duration_string)
        if minutes:
            self.duration += float(minutes.group(0)[:-1])

        # Get seconds
        seconds = re.search('\d+S', duration_string)
        if seconds:
            self.duration += float(seconds.group(0)[:-1]) / 60

    def __str__(self):
        return "Duration(minutes={})".format(self.duration)
