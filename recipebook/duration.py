MIN_IN_HOUR = 60
SEC_IN_MINIUTE = 60


# Turns a thing like PT45M into a duration like 45 minutes
class Duration(object):

    def __init__(self, duration_string):
        # This isn't perfect, but we'll claim it's good enough.
        # More info at https://en.wikipedia.org/wiki/ISO_8601#Durations
        # Assume all durations here are less than a day,
        # so everything is of the form
        # PT[#H][#M][#S]
        if not duration_string or duration_string == 'PT':
            self.duration, self.private_final = 0, 'M'
            return
        # Strip the leading PT
        duration_string, minutes = duration_string[2:], 0
        if 'H' in duration_string:
            minutes, duration_string = self.shift_end(
                'H', duration_string, minutes)
        if 'M' in duration_string:
            minutes, duration_string = self.shift_end(
                'M', duration_string, minutes)
        if 'S' in duration_string:
            minutes, duration_string = self.shift_end(
                'S', duration_string, minutes)
        self.duration = minutes

    def how_long(self):
        return self.duration

    def __str__(self):
        return "Duration(minutes={})".format(self.duration)

    # Broke shift code into its own function because it was
    # being called so much
    def shift_end(self, ch, duration_string, minutes):
        end = duration_string.index(ch)
        if(ch == 'H'):
            hours = float(duration_string[:end])
            minutes += hours * MIN_IN_HOUR
        elif(ch == 'M'):
            minutes += float(duration_string[:end])
        else:
            seconds = float(duration_string[:end])
            minutes += seconds / SEC_IN_MINIUTE
        duration_string = duration_string[end + 1:]
        return minutes, duration_string
