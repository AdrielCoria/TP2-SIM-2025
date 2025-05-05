import random
import math

class Normal:
    def __init__(self, media, desviacion):
        self.media = media
        self.desviacion = desviacion
        
    def generar_muestra(self, n):
        datos = []
        for _ in range((n + 1) // 2):  # Generamos de a pares
            u1 = random.random()
            u2 = random.random()
            z0 = math.sqrt(-2 * math.log(u1)) * math.cos(2 * math.pi * u2)
            z1 = math.sqrt(-2 * math.log(u1)) * math.sin(2 * math.pi * u2)
            datos.append(round(self.media + z0 * self.desviacion, 4))
            if len(datos) < n:
                datos.append(round(self.media + z1 * self.desviacion, 4))
        return datos