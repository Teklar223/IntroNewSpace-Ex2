import math
import Moon, Spaceship, Configuration

class Engine():
    '''
    This class represents the engine, which calculates the changes to the spaceship
    (similar to 'Model' in MVC)
    '''

    def __init__(self, config : Configuration):
        self.dt = config.dt
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
    
    def main_calc(self, ship : Spaceship):
        # main computations
        ang_rad = math.radians(ship.ang)
        h_acc = math.sin(ang_rad) * acc
        v_acc = math.cos(ang_rad) * acc
        vacc = Moon.getAcc(hs)
        time += self.dt
        dw =self. dt * self.all_burn * ship.NN
        if fuel > 0:
            fuel -= dw
            weight = self.weight_emp + fuel
            acc = ship.NN * self.accMax(weight)
        else:  # ran out of fuel
            acc = 0
        v_acc -= vacc
        if hs > 0:
            hs -= h_acc * self.dt
        dist -= hs * self.dt
        vs -= v_acc * self.dt
        alt -= self.dt * vs
        

            
