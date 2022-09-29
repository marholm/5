import time
from GPIOSimulator_v5 import GPIOSimulator, keypad_row_pins, \
    keypad_col_pins,PIN_KEYPAD_ROW_0,PIN_KEYPAD_COL_0, PIN_KEYPAD_COL_1,\
    PIN_KEYPAD_COL_2, PIN_KEYPAD_ROW_1, PIN_KEYPAD_ROW_2, PIN_KEYPAD_ROW_3

GPIO = GPIOSimulator()


class Keypad:
    """ Class for Keypad: Interface to the simulated keypad """
    def __init__(self):
        """ Constructor for Keypad """
        self.sequence_of_pressed_keys = []
        self.key_symbols = {(PIN_KEYPAD_ROW_0, PIN_KEYPAD_COL_0): "1",
                           (PIN_KEYPAD_ROW_0, PIN_KEYPAD_COL_1): "2",
                           (PIN_KEYPAD_ROW_0, PIN_KEYPAD_COL_2): "3",
                           (PIN_KEYPAD_ROW_1, PIN_KEYPAD_COL_0): "4",
                           (PIN_KEYPAD_ROW_1, PIN_KEYPAD_COL_1): "5",
                           (PIN_KEYPAD_ROW_1, PIN_KEYPAD_COL_2): "6",
                           (PIN_KEYPAD_ROW_2, PIN_KEYPAD_COL_0): "7",
                           (PIN_KEYPAD_ROW_2, PIN_KEYPAD_COL_1): "8",
                           (PIN_KEYPAD_ROW_2, PIN_KEYPAD_COL_2): "9",
                           (PIN_KEYPAD_ROW_3, PIN_KEYPAD_COL_0): "*",
                           (PIN_KEYPAD_ROW_3, PIN_KEYPAD_COL_1): "0",
                           (PIN_KEYPAD_ROW_3, PIN_KEYPAD_COL_2): "#"
                           }

    @staticmethod
    def setup():
        """ Method that sets up the row pins as outputs
        and the column pins as input """

        # Setup for row pins
        GPIO.setup(keypad_row_pins[0], GPIO.OUT)
        GPIO.setup(keypad_row_pins[1], GPIO.OUT)
        GPIO.setup(keypad_row_pins[2], GPIO.OUT)
        GPIO.setup(keypad_row_pins[3], GPIO.OUT)

        # Setup for column pins
        GPIO.setup(keypad_col_pins[0], GPIO.IN, GPIO.LOW)
        GPIO.setup(keypad_col_pins[1], GPIO.IN, GPIO.LOW)
        GPIO.setup(keypad_col_pins[2], GPIO.IN, GPIO.LOW)

    def do_polling(self):
        """ Method that determines the key currently
        being pressed on the keypad """

        # Iterating through all the pins in the keypad grid
        for row in keypad_row_pins:

            # Setting row pins to state=HIGH
            GPIO.output(row, GPIO.HIGH)

            for col in keypad_col_pins:

                # Reading the state of a column pin in a row
                if GPIO.input(col) == GPIO.HIGH:

                    # A key (row, col) is being pressed
                    print('Registered keypress: ', self.key_symbols[(row, col)])
                    return self.key_symbols[(row, col)]

            # Resetting the current pin row in order to check the next pin row
            GPIO.output(row, GPIO.LOW)

        # No key is being pressed
        return None

    def get_next_signal(self):
        """ Method that initiate repeated calls to
        do_polling until a key press is detected """
        print('Calling get_next_signal.')

        key = None
        while key is None:

            # Checking if a key is pressed and saving the pressed key as a tuple
            key = self.do_polling()

            if key is not None:
                # Adding the pressed key to the sequence of pressed keys
                self.sequence_of_pressed_keys.append(key)

            # Controlling the delay between polling
            time.sleep(0.12)
