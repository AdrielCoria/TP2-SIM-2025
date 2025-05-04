# Imports
import random
import math

# Clase para distribución Exponencial
class Exponencial:
    def __init__(self, lam, muestras, intervalos):
        self.lam = lam
        self.muestras = muestras
        self.intervalos = intervalos
        self.list_nums = []

    # Genera números usando la fórmula: -(1/λ)*ln(1 - U)
    def generar_numeros(self):
        for _ in range(self.muestras):
            rnd = random.random()
            numero = round(-math.log(1 - rnd) / self.lam, 4)
            self.list_nums.append(numero)

    def mostrar_lista(self):
        for i in self.list_nums:
            print(i)

    # Igual que en uniforme, pero con datos exponenciales
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