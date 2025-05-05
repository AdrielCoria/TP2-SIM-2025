import random
import math

class Exponencial:
    def __init__(self, lambd):
        self.lambd = lambd
        
    def generar_muestra(self, n):
        return [round(-(1/self.lambd) * math.log(1 - random.random()), 4) for _ in range(n)]