"""KPC Agent"""
from GPIOSimulator_v5 import *
gpio_obj = GPIOSimulator()


class KPC:
    def __init__(self, keypad_instance, led_board_instance):
        self.keypad_instance = keypad_instance
        self.led_board_instance = led_board_instance
        self.pathname = 'top_secret_password_file.txt'  # complete pathname to file holding KPC's password
        
        self.override_signal = ''    # Y override signal from agent signalling password acceptance
        self.password_buffer = ''    # Buffer for entering password char by char

        self.verified_password = ''  # Entered password verified as file password
        self.new_password = ''       # Resetting password to new password

        self.prev_state = ''
        self.current_state = ''

        self.led_id = ''            # Light user-specified LED
        self.led_duration = ''      # Light user-specified led for user-specifies # secs

    def wake_up_sequence(self):
        """ Method call at the beginning triggering a keypress and light display """
        input('--------------WAKE UP SYSTEM BY PRESSING ANY KEY----------')
        # Powering up light show for 3 secs
        self.flash_leds(1)

    def reset_password_entry(self):
        """Clear password buffer and initiate a 'power up' lighting sequence
        on the LED board"""
        self.password_buffer = ''
        self.led_board_instance.powering_up()

    def clear_buffer(self):
        """Clear password buffer without lighting leds"""
        self.password_buffer = ''

    def get_next_signal(self):
        """Return 'override_signal' if it's non-blank, else query keypad for the next
        pressed key"""

        if self.override_signal != '':
            return self.override_signal

        else:
            return self.keypad_instance.get_next_signal()

    def read_password_file(self):
        # Open and read file containing password
        f = open(self.pathname, 'r')
        official_password = f.read()
        print('Current Official Password: ', official_password)
        f.close()
        return official_password

    def verify_password(self):
        """Check entered password matches that of the password file"""
        print('Given password for checking: ', self.password_buffer)

        if self.password_buffer == self.read_password_file():
            self.verified_password = self.password_buffer
            print('Verified password: ', self.verified_password)
            print('Password verified. Login granted.')
            self.override_signal = 'Y'
            self.led_board_instance.correct_password()
            self.current_state = 'S-Verify'

        else:
            print('Password NOT verified. Try again.')
            self.override_signal = 'N'
            self.led_board_instance.wrong_password()
            # Empty password buffer and keypad_pressed_sequence
            self.keypad_instance.sequence_of_pressed_keys = []
            self.password_buffer = ''
            self.append_next_password_digit()

    def validate_passcode_change(self):
        """Check new password is legal"""
        # Legal: >= 4 in length and only consisting of numbers
        if (len(self.new_password) >= 4) and (self.new_password.isdecimal()):
            self.led_board_instance.correct_password()
            # New password has been validated and gets cached to file
            self.cache_new_password()
        else:
            print('New password does not meet formal requirements.\n')

    def append_next_password_digit(self):
        """ Append password entry to password buffer """
        print('-----------------LOGIN------------------------')

        self.keypad_instance.get_next_signal()

        if self.keypad_instance.sequence_of_pressed_keys[-1] == '*' or \
                self.keypad_instance.sequence_of_pressed_keys[-1] == '#':

            print('Keypress: * or # ')

            self.verify_password()

        else:
            self.password_buffer += (self.keypad_instance.sequence_of_pressed_keys[-1])

            print('Password_buffer: ', self.password_buffer)
            print('Sequence of pressed keys 2: ', self.keypad_instance.sequence_of_pressed_keys)

            self.append_next_password_digit()

    def cache_new_password(self):
        """Save the new password in a file - New password replaces old password"""

        # Erase current file content (old password)
        f = open(self.pathname, 'r+')   # r+ opens file for read and write
        f.truncate()                    # truncate deletes file content - evt: truncate(0)

        # Write/save new password in file
        f.write(self.new_password)
        f.close()

    def change_password(self):
        print('-------------CHANGE PASSWORD---------------------')
        self.keypad_instance.get_next_signal()

        if self.keypad_instance.sequence_of_pressed_keys[-1] == '*' or \
                self.keypad_instance.sequence_of_pressed_keys[-1] == '#':

            # Done making new password -  cache it to file
            self.validate_passcode_change()

        else:
            # Change existing password
            self.new_password += (self.keypad_instance.sequence_of_pressed_keys[-1])

            print('New password: ', self.new_password)

            self.change_password()

    def logout_logic(self):
        # Logout sequence with extra check
        print('------------------LOGOUT-----------------------------')
        self.keypad_instance.get_next_signal()

        if self.keypad_instance.sequence_of_pressed_keys[-1] == '#':
            input_value = input('Logout initiated. Confirm logout [y/n]')

            if input_value == 'y':
                self.exit_action()

            else:
                self.clear_buffer()

    def reset_agent(self):
        """ Putting the agent in a restricted mode where it
        can only receive password login attempts """
        self.current_state = 'S-init'

    def fully_activate_agent(self):
        """ Setting the agent to S-active state """
        self.current_state = 'S-Active'
        self.led_board_instance.twinkle_all_leds(1)
        self.clear_buffer()

        print('Agent fully active!')

    def refresh_agent(self, state):
        """ Putting the agent to a less-restricted active state from
        which many other actions (not shown in Figure 4) such as turning
        on lights, may be initiated."""
        self.prev_state = self.current_state
        self.current_state = state

    def set_led_id(self):
        print('GIVE LED_ID: ')

        self.keypad_instance.get_next_signal()
        self.led_id = int(self.keypad_instance.sequence_of_pressed_keys[-1])

        print('Given L_id: ', self.led_id)

    def set_led_duration(self):
        print('GIVE LDUR: ')

        self.keypad_instance.get_next_signal()
        self.led_duration = int(self.keypad_instance.sequence_of_pressed_keys[-1])

        print('Given Ldur: ', self.led_duration)

    # LED methods
    def light_one_led(self):
        """Call the LED board and request LED #Lid be turned on for Ldur secs"""
        print('------------LIGHT USER DEFINED LED FOR USER DEFINED TIME------------------')
        self.led_board_instance.turn_on_user_specified_led(self.led_id, self.led_duration)

    def flash_leds(self, k_sec):
        """Call LED board and request flashing of all LEDs"""
        self.led_board_instance.flash_all_leds(k_sec)

    def twinkle_leds(self, k_sec):
        """Call LED board and request twinkling of all LEDs"""
        self.led_board_instance.twinkle_all_leds(k_sec)

    def exit_action(self):
        """Call LED board to initiate 'power down' lighting sequence"""
        self.led_board_instance.powering_down()
