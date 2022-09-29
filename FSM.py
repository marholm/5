"""Finite State Machine implementation"""
from FSM_rules import Rules
from keypad import Keypad
from LED_board import LEDBoard


class FSM:
    """Class for implementing the Finite State Machine"""

    def __init__(self, agent):
        """Initializer function"""
        self.current_state = None  # Current state of the finite state machine
        self.start_state = 'S-Init'

        self.agent = agent         # Pointer back to agent
        self.rules = []            # List of rules the FSM implements

    def add_rule(self, rule):
        """Add a new rule to the end of the FSM rules list"""
        self.rules.append(rule)

    def get_next_signal(self):
        """Query the agent for the next signal"""

        next_signal = self.agent.get_next_signal()

        return next_signal

    def run(self, next_signal):
        """Start in FSMs init state and repeatedly call g_n_s() and
        run the rules one by one until reaching the final state"""

        for rule in self.rules:
            if self.match(rule, next_signal):
                self.fire(rule)
                break   # break after first match

        print('No match - find error!')

    def match(self, rule, next_signal):
        """ Check whether rule condition is fulfilled """
        # Check signal matches, Check state matches

        if next_signal in rule.signal and self.current_state == rule.state_1:

            # Match found
            self.fire(rule)

            return True

        return False

    def fire(self, rule):
        """Use consequent of a rule to
        a) set next state(state2) of the FSM and
        b) call the appropriate agent action method"""

        self.current_state = rule.state2

        rule.agent_action()

    def is_final_state(self):

        if self.current_state == 'S-Active' and self.get_next_signal() == '#':

            return True

        return False

    def create_rules(self):
        """ Method that creates rule objects from the Rule class """

        # All possible signals
        all_signals = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '*', '#']

        # A1 for first iteration
        rule1 = Rules('S-init', all_signals, 'S-Read', self.agent.wake_up_sequence())

        # A2
        rule2 = Rules('S-Read', all_signals[:10], 'S-Read', self.agent.append_next_password_digit())

        # A3
        rule3 = Rules('S-Read', all_signals[10], 'S-Verify', self.agent.verify_password())

        # A4
        rule4 = Rules('S-Verify', all_signals, 'S-init', self.agent.reset_password_entry())

        # A5
        rule5 = Rules('S-Verify', 'Y', 'S-Active', self.agent.fully_activate_agent())

        # A4
        rule6 = Rules('S-Read', all_signals, 'S-init', self.agent.clear_buffer())

        # A1
        rule7 = Rules('S-Active', all_signals[10], 'S-Read-2', self.agent.reset_password_entry())

        # Choose a LED id
        rule8 = Rules('S-Active', all_signals[:6], 'S-Led', self.agent.set_led_id())

        # Choose a LED duration
        rule9 = Rules('S-time', all_signals[:10], 'S-time', self.agent.set_led_duration())  # Evt kall append_next_password_digit()

        # Complete duration
        rule10 = Rules('S-time', all_signals[10],'S-Active', self.agent.light_one_led())

        # A6
        rule16 = Rules('S-Read-2', all_signals, 'S-Active', self.agent.reset_password_entry())

        # A2
        rule17 = Rules('S-Active', all_signals[:10], 'S-Read-2', self.agent.change_password())

        # A7
        rule18 = Rules('S-Read-2', all_signals[10], 'S-Read-3', self.agent.cache_new_password())

        # A6
        rule19 = Rules('S-Read-3', all_signals, 'S-Active', self.agent.reset_password_entry())

        # LOGOUT RULES
        # Confirm logout
        rule11 = Rules('S-Active', all_signals[11], 'S-Confirm_Logout', self.agent.clear_buffer())

        # Actual logout
        rule12 = Rules('S-Confirm_Logout', all_signals[11], 'S-Done', self.agent.logout_logic())

        rule_ = Rules('S-Done', all_signals, 'S-Active', self.agent.wake_up_sequence())

        # Logout cancelled
        rule13 = Rules('S-Confirm_Logout', all_signals, 'S-Active', self.agent.clear_buffer())

        # Add all rule-tuples to a list
        self.rules = [rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9, rule10, rule16,
                      rule17, rule18, rule19, rule11, rule12, rule_, rule13]

    def main_loop(self):
        """Main sequence to run the FSM"""

        # Create all rule objects
        self.create_rules()
        print('Rules created')

        for rule in self.rules:
            self.add_rule(rule)


        led_board_obj = LEDBoard()
        keypad_obj = Keypad()

        self.current_state = self.start_state
        print('Current state: ', self.current_state)

        while not self.is_final_state():
            print("Not Final State Loop")
            keypad_obj.get_next_signal()
            next_signal = self.agent.get_next_signal()
            self.run(next_signal)

            for rule in self.rules:
                self.add_rule(rule)
                self.match(rule, next_signal)

        # Shutdown agent, keypad, LED board etc.
        led_board_obj.powering_down()
        self.agent.exit_action()
