import random
import math

class Uniforme:
    def __init__(self, a, b):
        self.a = a
        self.b = b
        
    def generar_muestra(self, n):
        return [round(self.a + random.random() * (self.b - self.a), 4) for _ in range(n)]