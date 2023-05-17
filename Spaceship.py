import Configuration

class Spaceship():
    '''
    '''
    def __init__(self, config : Configuration):
        # TODO: get some of these parameters as input (the starting point) and set them via config
        self.vs = config.vs
        self.hs = config.hs
        self.dist = config.dist
        self.ang =config.ang  # zero is vertical (as in landing)
        self.alt = config.alt  # 2:25:40 (as in the simulation) # https://www.youtube.com/watch?v=JJ0VfRL9AMs
        self.acc = config.acc  # Acceleration rate (m/s^2)
        self.fuel = config.fuel
        self.weight = config.WEIGHT_EMP + self.fuel
        self.NN = config.NN  # engine power rate (in the range [0,1]), higher = more braking power

