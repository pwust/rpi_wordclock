
class time_as_words_german():
    """
    This class returns a given time as words (string)::
    """

    def __init__(self):
        self.prefix = "ES IST "
        self.minutes = ["",
            "FÜNF NACH ", \
            "ZEHN NACH ", \
            "VIERTEL NACH ", \
            "ZWANZIG NACH ", \
            "FÜNF VOR HALB ", \
            "HALB ", \
            "FÜNF NACH HALB ", \
            "ZWANZIG VOR ", \
            "VIERTEL VOR ", \
            "ZEHN VOR ", \
            "FÜNF VOR "]
        self.hours = ["ZWÖLF", \
            "EIN", \
            "ZWEI", \
            "DREI", \
            "VIER", \
            "FÜNF", \
            "SECHS", \
            "SIEBEN", \
            "ACHT", \
            "NEUN", \
            "ZEHN", \
            "ELF", \
            "ZWÖLF"]
        self.full_hour_suffix = " UHR"

    def get_time(self, time, withPrefix=True):
        hour = time.hour % 12 + (1 if int(time.minute / 5) > 4 else 0)
        minute = int(time.minute / 5)
        # Assemble string
        return str(
            (self.prefix if withPrefix else "") +
            self.minutes[minute] +
            self.hours[hour] +
            # Append "S" to "EIN" (in case of "EIN UHR")
            ("S" if (hour == 1 and minute != 0) else "") + \
            (self.full_hour_suffix if (minute == 0) else "")) + " " + \
            ('*' * int(time.minute % 5))

