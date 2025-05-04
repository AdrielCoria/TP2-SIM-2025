# Import
import random

# Clase para distribución Uniforme
class Uniforme: 
    def __init__(self, inf, sup, muestras, intervalos):
        self.inf = inf
        self.sup = sup 
        self.muestras = muestras
        self.intervalos = intervalos
        self.list_nums = []
    
    # Genera números uniformemente distribuidos entre inf y sup
    def generar_numeros(self):
        for i in range(self.muestras):
            numero = round(random.random(), 4)
            numero = round(self.inf + numero*(self.sup - self.inf), 4)
            self.list_nums.append(numero)

    # Muestra la lista generada
    def mostrar_lista(self):
        for i in self.list_nums:
            print(i)
    
    # Calcula y muestra las frecuencias de los números generados en intervalos
    def calcular_frecuencias(self):
        frecuencias = [0] * self.intervalos
        rango = max(self.list_nums) - min(self.list_nums)
        ancho = rango / self.intervalos
        for numero in self.list_nums:
            indice = int((numero - min(self.list_nums)) / ancho)
            if indice == self.intervalos:
                indice -= 1
            frecuencias[indice] += 1
        print(frecuencias)
