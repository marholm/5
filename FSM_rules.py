class Rules:
    """ Class that defines states, signals and actions
    for each rule instance of the class """
    def __init__(self, state_1, signal, state_2, agent_action):
        """ """
        self.state_1 = state_1      # Triggering state of the FSM
        self.state_2 = state_2      # New state of FSM if this rule fires
        self.signal = signal       # Triggering signal
        self.agent_action = agent_action       # Agent will be instructed to perform this action if this rule fires
