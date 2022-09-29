import time
from GPIOSimulator_v5 import GPIOSimulator


class LEDBoard:
    """ Class for the LED Board"""

    def __init__(self):
        """ Constructor """
        self.GPIO = GPIOSimulator()
        self.pin_settings_pr_led = {
            0: [1, 0, None],
            1: [0, 1, None],
            2: [None, 1, 0],
            3: [None, 0, 1],
            4: [1, None, 0],
            5: [0, None, 1],
        }

    def light_led(self, LED):
        """ Method that turns a LED on """
        pin_settings = self.pin_settings_pr_led[LED]

        # Iterating through the pin settings for specified LED
        for index, state in enumerate(pin_settings):

            # Pin setting is output and HIGH
            if state == 1:
                self.GPIO.setup(index, self.GPIO.OUT)
                self.GPIO.output(index, self.GPIO.HIGH)

            # Pin setting is output and LOW
            elif state == 0:
                self.GPIO.setup(index, self.GPIO.OUT)
                self.GPIO.output(index, self.GPIO.LOW)

            # Pin setting is input
            elif state is None:
                self.GPIO.setup(index, self.GPIO.IN)

        # Printing the current state of all LEDs
        self.GPIO.show_leds_states()

    def turn_on_user_specified_led(self, LED, k):
        """ Method that turns one user-specified LED on
        for a user-specified number of seconds, where information
        about the particular LED and duration are entered
        via the simulated keypad """

        self.light_led(LED)

        time.sleep(k)

        self.GPIO.cleanup()

        self.GPIO.show_leds_states()

    def flash_all_leds(self, k):
        """ Method that makes one LEDs flash at a time for k seconds """

        reference_time = time.time()
        duration_time = reference_time + k
        is_time_over = False

        # Making it possible to light the same LED again
        while not is_time_over:

            for pin in range(6):

                self.light_led(pin)

                # Checking if k seconds is passed
                time_now = time.time()
                if time_now > duration_time:
                    is_time_over = True
                    break

                # Making the iteration go a bit slower
                time.sleep(0.5)

    def twinkle_all_leds(self, k):
        """ Method that turns all LEDS on and off in sequence for k seconds """

        reference_time = time.time()
        duration_time = reference_time + k
        is_time_over = False

        # Making it possible to light the sequence of LEDs again
        while not is_time_over:

            for pin in range(6):

                self.light_led(pin)

                # Making the iteration go a bit slower
                time.sleep(0.5)

            time_now = time.time()
            if time_now > duration_time:
                is_time_over = True

    def powering_up(self):
        """ Method that displays light that indicates that
        the system is powering up """
        print("---------Powering up LED sequence!---------------")

        # Turning on LED 0 for 6 sec
        self.turn_on_user_specified_led(0, 2)

    def powering_down(self):
        """ Method that displays light that indicates that
        the system is powering down """

        print("----------Powering down LED sequence..------------")

        # Making LED 4 and 5 twinkle a couple of times
        for i in range(4):
            self.turn_on_user_specified_led(4, 2)
            time.sleep(1.0)
            self.turn_on_user_specified_led(5, 2)
            time.sleep(1.0)

    def wrong_password(self):
        """ Method that flashes lights “in synchrony” when
        the user enters the wrong password during login """

        print("-----------Wrong password LED sequence--------------")
        self.flash_all_leds(5.5)

    def correct_password(self):
        """ Method that twinkles the lights when the user successfully logs in """
        print("-----------Correct password LED sequence-------------")
        self.twinkle_all_leds(2)
