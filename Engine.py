import math
import Moon, Spaceship, Configuration
from Constants import *
class Engine():
    '''
    This class represents the engine, which calculates the changes to the spaceship
    (similar to 'Model' in MVC)
    '''

    def __init__(self, config : Configuration):
        self.all_burn = config.ALL_BURN
        self.weight_emp = config.WEIGHT_EMP


    def accMax(self, weight: float) -> float:
        return self.acc_fun(weight, True, 8)


    def acc_fun(self, weight: float, main: bool, seconds: int) -> float:
        t = 0
        if main:
            t += self.MAIN_ENG_F
        t += seconds * self.SECOND_ENG_F
        ans = t / weight
        return ans
    
    def main_calc(self, dt, ship : Spaceship):
        # temps
        ang_rad = math.radians(ship.config.ang)
        h_acc = math.sin(ang_rad) * acc
        v_acc = math.cos(ang_rad) * acc
        vacc = Moon.getAcc(hs)
        time += dt
        dw = dt * self.all_burn * ship.config.NN
        fuel = None
        acc = None
        if ship.config.fuel > 0:
            fuel = ship.config.fuel - dw
            weight = self.weight_emp + fuel
            acc = ship.config.NN * self.accMax(weight)
        else:  # ran out of fuel
            acc = 0
        v_acc -= vacc
        if hs > 0:
            hs -= h_acc * self.dt
        dist -= hs * self.dt
        vs -= v_acc * self.dt
        alt -= self.dt * vs

        ship.config.update(dist = dist, vs = vs, hs = hs, acc = acc, alt = alt, fuel = fuel)
        

            
