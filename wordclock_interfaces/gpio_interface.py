import RPi.GPIO as GPIO


class gpio_interface:
    def __init__(self, config, evtHandler):
        """
        Initialization
        """

        interface_type = config.get('wordclock_interface', 'type')

        if interface_type == 'no_gpio':
            print('GPIO interface disabled. If hardware buttons are attached, '
                  'any input is ignored. Webinterface can be used instead.')
            return

        self.evtHandler = evtHandler

        # 3 buttons are required to run the wordclock.
        # Below, for each button, the corresponding GPIO-pin is specified.
        self.button_left = int(config.get('wordclock_interface', 'pin_button_left'))
        self.button_return = int(config.get('wordclock_interface', 'pin_button_return'))
        self.button_right = int(config.get('wordclock_interface', 'pin_button_right'))
        self.button_four = int(config.get('wordclock_interface', 'pin_button_four'))
        self.button_five = int(config.get('wordclock_interface', 'pin_button_five'))

        # Initializations for GPIO-input
        GPIO.setmode(GPIO.BCM)
        GPIO.setup([self.button_left, self.button_return, self.button_right,
                    self.button_four, self.button_five], GPIO.IN)

        if interface_type == 'gpio_high':
            self.polarity = GPIO.FALLING
        else:
            if interface_type != 'gpio_low':
                print('Warning: Unknown interface_type ' + interface_type +
                      '. Falling back to default.')
                interface_type = 'gpio_low'
            self.polarity = GPIO.RISING

        print('Interface type set to ' + interface_type)

        GPIO.add_event_detect(self.button_left,
                              self.polarity,
                              callback=lambda channel: self._left(),
                              bouncetime=100)
        GPIO.add_event_detect(self.button_return,
                              self.polarity,
                              callback=lambda channel: self._return(),
                              bouncetime=100)
        GPIO.add_event_detect(self.button_right,
                              self.polarity,
                              callback=lambda channel: self._right(),
                              bouncetime=100)
        GPIO.add_event_detect(self.button_four,
                              self.polarity,
                              callback=lambda channel: self._four(),
                              bouncetime=100)
        GPIO.add_event_detect(self.button_five,
                              self.polarity,
                              callback=lambda channel: self._five(),
                              bouncetime=100)

    def _left(self):
        self.evtHandler.setEvent(self.evtHandler.EVENT_BUTTON_LEFT)

    def _return(self):
        self.evtHandler.setEvent(self.evtHandler.EVENT_BUTTON_RETURN)

    def _right(self):
        self.evtHandler.setEvent(self.evtHandler.EVENT_BUTTON_RIGHT)

    def _four(self):
        self.evtHandler.setEvent(self.evtHandler.EVENT_BUTTON_FOUR)

    def _five(self):
        self.evtHandler.setEvent(self.evtHandler.EVENT_BUTTON_FIVE)

