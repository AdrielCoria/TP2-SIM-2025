# Imports
import random
import math

# Clase para distribución Normal usando el método de Box-Muller
class Normal:
    def __init__(self, media, desviacion, muestras, intervalos):
        self.media = media
        self.desviacion = desviacion
        self.muestras = muestras
        self.intervalos = intervalos
        self.list_nums = []

    # Genera números normales con Box-Muller transform
    def generar_numeros(self):
        i = 0
        while i < self.muestras:
            u1 = random.random()
            u2 = random.random()
            z1 = math.sqrt(-2 * math.log(u1)) * math.cos(2 * math.pi * u2)
            z2 = math.sqrt(-2 * math.log(u1)) * math.sin(2 * math.pi * u2)

            x1 = round(self.media + self.desviacion * z1, 4)
            self.list_nums.append(x1)
            i += 1

            if i < self.muestras:  # Para evitar pasarse cuando muestras es impar
                x2 = round(self.media + self.desviacion * z2, 4)
                self.list_nums.append(x2)
                i += 1

    def mostrar_lista(self):
        for i in self.list_nums:
            print(i)

    def calcular_frecuencias(self):
        frecuencias = [0] * self.intervalos
        minimo = min(self.list_nums)
        maximo = max(self.list_nums)
        rango = maximo - minimo
        ancho = rango / self.intervalos

        for numero in self.list_nums:
            indice = int((numero - minimo) / ancho)
            if indice == self.intervalos:
                indice -= 1
            frecuencias[indice] += 1
        print(frecuencias)