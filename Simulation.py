'''
    This is the 'Controller' of our simulation
'''

import Engine, Spaceship, Configuration

class Simulation():
    
    def __init__(self, config : Configuration):
        self.time = 0
        self.ship = Spaceship(config)
        self.engine = Engine(config)
