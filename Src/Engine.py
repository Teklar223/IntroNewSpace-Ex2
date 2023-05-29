import numpy as np
import math
import Src.Moon as Moon, Src.Configuration as Configuration
from Src.Constants import *


class Engine():
    '''
    This class represents the physics engine, which calculates the changes to the spaceships position
    '''

    def __init__(self, config: Configuration):
        self.all_burn = config.ALL_BURN
        self.weight_emp = config.WEIGHT_EMP
        self.MAIN_ENG_F = config.MAIN_ENG_F
        self.SECOND_ENG_F = config.SECOND_ENG_F


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
        # TODO: normalize dt to seconds!
        ang_rad = math.radians(config.angle)
        h_acc = math.cos(ang_rad) * config.acc
        v_acc = math.sin(ang_rad) * config.acc - Moon.getAcc(config.hs)

        vs = config.vs + v_acc * dt
        hs = config.hs + h_acc * dt

        dw = dt * self.all_burn * config.thrust
        fuel = config.fuel
        acc = 0 # if fuel <= 0
        weight = self.weight_emp

        if fuel > 0:
            fuel = fuel - dw
            weight += fuel
            acc = config.thrust * self.accMax(weight)
        else:
            fuel = 0

        lat = config.lat + hs * dt
        alt = config.alt + dt * vs

        return lat,vs,hs,acc,alt,fuel, weight
        

            
