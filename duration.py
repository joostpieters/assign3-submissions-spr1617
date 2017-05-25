''' File: duration.py
-----------------------------------------------------------
Converts ISO durations into a more human readable format (e.g. PT45M --> 45 minutes)
'''

# Turns a thing like PT45M into a duration like 45 minutes

CONVERSION = 60

def process_duration(duration_string, letter):
    ''' Read the duration string and return how much time to add
    handles different conversions for hours, minutes, and seconds
    '''
    end = duration_string.index(letter)
    time = float(duration_string[:end])
    if letter == 'S':
        time /= CONVERSION
    elif letter == 'H':
        time *= CONVERSION
    duration_string = duration_string[end+1:]

    return time, duration_string

class Duration(object):
    def __init__(self, duration_string):
        '''
        This isn't perfect, but we'll claim it's good enough.
        More info at https://en.wikipedia.org/wiki/ISO_8601#Durations
        Assume all durations here are less than a day, so everything is of the form
        PT[#H][#M][#S]
        '''

        if not duration_string or duration_string == 'PT':
            self.duration = 0
            self.private_final = 'M'
            return

        duration_string = duration_string[2:] # Strip the leading PT
        minutes = 0
        if 'H' in duration_string:
            time, duration_string = process_duration(duration_string, 'H')
            minutes += time
        if 'M' in duration_string:
            time, duration_string = process_duration(duration_string, 'M')
            minutes += time
        if 'S' in duration_string:
            time, duration_string = process_duration(duration_string, 'S')
            minutes += time

        self.duration = minutes

    def how_long(self):
        return self.duration

    def __str__(self):
        return "Duration: {} minutes".format(self.duration)
