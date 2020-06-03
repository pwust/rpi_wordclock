# -*- coding: UTF-8
class time_german3:
    """
    This class returns a given time as a range of LED-indices.
    Illuminating these LEDs represents the current time on a german WCA
    """

    def __init__(self):
        self.prefix = list(range(1,3)) + list(range(4,7))
        # -> es ist
        self.minutes = [[], \
            list(range(17,21)) + list(range(45,49)), \
                      # -> fünf nach
            list(range(12,16)) + list(range(45,49)), \
                      # -> zehn nach
            list(range(37,44)) + list(range(45,49)), \
                      # -> viertel nach
            list(range(25,32)) + list(range(45,49)), \
                      # -> zwanzig nach
            list(range(17,21)) + list(range(50,53)) + list(range(55,59)), \
                      # -> fünf vor halb
            list(range(55,59)), \
                      # -> halb
            list(range(17,21)) + list(range(45,49)) + list(range(55,59)), \
                      # -> fünf nach halb
            list(range(25,32)) + list(range(50,53)), \
                      # -> zwanzig vor
            list(range(37,44)) + list(range(50,53)), \
                      # -> viertel vor
            list(range(12,16)) + list(range(50,53)), \
                      # -> zehn vor
            list(range(17,21)) + list(range(50,53)) ]
                      # fünf vor
        self.hours = [list(range(81,86)), \
                      # -> zwölf
            list(range(102,105)), \
                      # -> ein/s
            list(range(100,104)), \
                      # -> zwei
            list(range(77,81)), \
                      # -> drei
            list(range(73,77)), \
                      # -> vier
            list(range(62,66)), \
                      # -> fünf
            list(range(88,93)), \
                      # -> sechs
            list(range(92,98)), \
                      # -> sieben
            list(range(113,117)), \
                      # -> acht
            list(range(66,70)), \
                      # -> neun
            list(range(106,110)), \
                      # -> zehn
            list(range(60,63)), \
                      # -> elf
            list(range(81,86))]
                      # -> zwölf
        self.full_hour = list(range(117,120))

    def get_time(self, time, purist):
        minute = int(time.minute / 5)
        hour = time.hour % 12 + (1 if minute >= 5 else 0)
        # Assemble indices
        # special "8:00": "ACHT" range(46,50) from elsewhere to prevent "ACHTUHR" w/o space!
        # special case "ein uhr" vs. e.g. "fünf nach einS": add "s" manually on 1:05..1:59!
        return  \
            (self.prefix if not purist else []) + \
            self.minutes[minute] + \
            (list(range(46,50)) if (minute == 0 and hour == 8) else self.hours[hour]) + \
            ([105] if (hour == 1 and minute != 0) else []) + \
            (self.full_hour if (minute == 0) else [])

