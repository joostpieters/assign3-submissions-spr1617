# Turns a thing like PT45M into a duration like 45 minutes
class Duration(object):
    def __init__(self, duration_string):
        # More info at https://en.wikipedia.org/wiki/ISO_8601#Durations
        # Assume all durations here are less than a day, so everything is of the form
        # PT[#H][#M][#S]

        self.duration = 0

        if not duration_string or duration_string == 'PT':
            self.private_final = 'M'
            return

        duration_string = duration_string[2:] # Strip the leading PT

        while True:
            multiplier = 1 # changes dependent on whether H, M, or S
            if 'H' in duration_string:
                end = duration_string.index('H')
                multiplier = 60

            elif 'M' in duration_string:
                end = duration_string.index('M')

            elif 'S' in duration_string:
                end = duration_string.index('S')
                multiplier = float(1/60)
            else:
                break

            time = float(duration_string[:end])
            self.duration += time * multiplier
            duration_string = duration_string[end + 1:]

    def how_long(self):
        return self.duration

    def __str__(self):
        return "Duration(minutes={})".format(self.duration)
