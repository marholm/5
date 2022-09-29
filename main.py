""" The main function"""
from KPC import KPC
from keypad import Keypad
from LED_board import LEDBoard
from FSM import FSM


def main():
    """ Main function of the entire system """
    keypad = Keypad()
    keypad.setup()

    l_board = LEDBoard()

    kpc_agent = KPC(keypad, l_board)

    fsm = FSM(kpc_agent)
    fsm.main_loop()

RUN_MAIN = main()
