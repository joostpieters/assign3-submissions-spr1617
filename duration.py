#!/usr/bin/env python3 -tt
"""
File: durations.py
-----------------------
Assignment 3: Stylize
Course: CS 41
Name: Grant Spellman
SUNet: gshamus

Defines the duration object as a more covenient representation of time compared to
ISO 8601 durations. See below for more information

https://en.wikipedia.org/wiki/ISO_8601#Durations
"""
class Duration(object):
    def __init__(self, duration_string):
        # Assume all durations here are less than a day, so everything is of the form
        # PT[#H][#M][#S]
        if not duration_string:
            self.duration = 0
            self.private_final = 'M'
            return
        if duration_string == 'PT':
            self.duration = 0
            self.private_final = 'M'
            return

        duration_string = duration_string[2:] # Strip the leading PT
        minutes = 0
        if 'H' in duration_string:
            end = duration_string.index('H')
            hours = float(duration_string[:end])
            minutes += hours * 60
            duration_string = duration_string[end+1:]
        if 'M' in duration_string:
            end = duration_string.index('M')
            minutes += float(duration_string[:end])
            duration_string = duration_string[end+1:]
        if 'S' in duration_string:
            end = duration_string.index('S')
            seconds = float(duration_string[:end])
            minutes += seconds / 60
            duration_string = duration_string[end+1:]

        self.duration = minutes

    def how_long(self):
        return self.duration

    def __str__(self):
        return "Duration(minutes={})".format(self.duration)
