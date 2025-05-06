from scipy.stats import norm, expon
import math
import numpy as np

class KS:
    def __init__(self, datos, distribucion, intervalos=None):
        self.datos = sorted(datos)
        self.distribucion = distribucion
        self.intervalos = intervalos if intervalos else int(math.sqrt(len(datos)))  # Por defecto √n intervalos
        '''
        No estoy seguro si deberia calcular 
        
        '''
        self.resultados = []
        self.estadistico = 0
        self.valor_critico = 0
        self.conclusion = ""
        
        self._calcular_prueba()
        
    def _calcular_prueba(self):
        n = len(self.datos)
        min_val = min(self.datos)
        max_val = max(self.datos)
        ancho_intervalo = (max_val - min_val) / self.intervalos
        
        # Calcular frecuencias observadas en cada intervalo
        frec_obs = [0] * self.intervalos
        for x in self.datos:
            idx = int((x - min_val) / ancho_intervalo)
            idx = min(idx, self.intervalos - 1)  # Asegurar que no exceda el último intervalo
            frec_obs[idx] += 1
        
        # Calcular probabilidades observadas (Po) y acumuladas (PoAc)
        Po = [fo / n for fo in frec_obs]
        PoAc = [sum(Po[:i+1]) for i in range(self.intervalos)]
        
        # Calcular probabilidades esperadas acumuladas (PeAc)
        PeAc = []
        for i in range(self.intervalos):
            lim_sup = min_val + (i + 1) * ancho_intervalo
            
            if self.distribucion == "Uniforme [a,b]":
                pe = (lim_sup - min_val) / (max_val - min_val) if max_val != min_val else 0
            
            elif self.distribucion == "Exponencial":
                lambd = 1 / (sum(self.datos) / n)  # Estimación de lambda
                pe = 1 - math.exp(-lambd * lim_sup) if lim_sup >= 0 else 0
            
            elif self.distribucion == "Normal":
                media = sum(self.datos) / n
                varianza = sum((x - media)**2 for x in self.datos) / n
                desviacion = math.sqrt(varianza)
                pe = norm.cdf(lim_sup, media, desviacion)
            
            PeAc.append(pe)
        
        # Calcular diferencias absolutas y encontrar el máximo (estadístico KS)
        diferencias = [abs(PoAc[i] - PeAc[i]) for i in range(self.intervalos)]
        self.estadistico = max(diferencias)
        
        # Construir tabla de resultados
        for i in range(self.intervalos):
            lim_inf = min_val + i * ancho_intervalo
            lim_sup = min_val + (i + 1) * ancho_intervalo
            if i == self.intervalos - 1:  # Ajustar último intervalo
                lim_sup = max_val
            
            self.resultados.append((
                round(lim_inf, 4),
                round(lim_sup, 4),
                frec_obs[i],
                round(Po[i], 4),
                round(PeAc[i] - (PeAc[i-1] if i > 0 else 0), 4),  # Pe individual
                round(PoAc[i], 4),
                round(PeAc[i], 4),
                round(diferencias[i], 4),
                round(self.estadistico, 4)
            ))
        
        # Valor crítico (según tabla del apunte)
        if n <= 35:
            # Valores aproximados para n ≤ 35 (deberías usar una tabla exacta)
            self.valor_critico = 1.36 / math.sqrt(n)
        else:
            # Para n > 35 según apunte
            self.valor_critico = 1.36 / math.sqrt(n)  # Para α=0.05
        
        # Conclusión
        if self.estadistico <= self.valor_critico:
            self.conclusion = "Conclusión: No se rechaza la hipótesis de que los datos siguen la distribución"
        else:
            self.conclusion = "Conclusión: Se rechaza la hipótesis de que los datos siguen la distribución"