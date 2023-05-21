import math
import Moon, Spaceship, Configuration
from Constants import *
class Engine():
    '''
    This class represents the physics engine, which calculates the changes to the spaceships position
    '''

    def __init__(self, config : Configuration):
        self.all_burn = config.ALL_BURN
        self.weight_emp = config.WEIGHT_EMP
        self.MAIN_ENG_F = 430  # N
        self.SECOND_ENG_F = 25  # N


    def accMax(self, weight: float) -> float:
        return self.acc_fun(weight, True, 8)


    def acc_fun(self, weight: float, main: bool, seconds: int) -> float:
        t = 0
        if main:
            t += self.MAIN_ENG_F
        t += seconds * self.SECOND_ENG_F
        ans = t / weight
        return ans
    
    def main_calc(self, dt, config : Configuration) :
        # temps
        ang_rad = math.radians(config.angle)
        h_acc = math.sin(ang_rad) * config.acc
        v_acc = math.cos(ang_rad) * config.acc
        vacc = Moon.getAcc(config.hs)
        dw = dt * self.all_burn * config.NN
        fuel = None
        acc = None
        weight = None
        if config.fuel > 0:
            fuel = config.fuel - dw
            weight = self.weight_emp + fuel
            acc = config.NN * self.accMax(weight)
        else:  # ran out of fuel
            acc = 0
        v_acc -= vacc
        hs = None
        if config.hs > 0:
            hs = config.hs - h_acc * dt
        dist = config.dist - hs * dt
        vs = config.vs - v_acc * dt
        alt = config.alt - dt * vs

        return dist,vs,hs,acc,alt,fuel, weight
        

            
