from scipy.stats import norm, expon
import math

class KS:
    def __init__(self, datos, distribucion):
        self.datos = sorted(datos)
        self.distribucion = distribucion
        self.resultados = []
        self.estadistico = 0
        self.valor_critico = 0
        self.conclusion = ""
        
        self._calcular_prueba()
        
    def _calcular_prueba(self):
        n = len(self.datos)
        max_ks = 0
        
        for i in range(1, n + 1):
            # Probabilidad acumulada observada
            po = i / n
            
            # Probabilidad acumulada esperada según la distribución
            if self.distribucion == "Uniforme [a,b]":
                a = min(self.datos)
                b = max(self.datos)
                pe = (self.datos[i-1] - a) / (b - a) if b != a else 0
                pe = max(0, min(1, pe))
            
            elif self.distribucion == "Exponencial":
                lambd = 1 / (sum(self.datos) / n)  # Estimación de lambda
                pe = 1 - math.exp(-lambd * self.datos[i-1]) if self.datos[i-1] >= 0 else 0
            
            elif self.distribucion == "Normal":
                media = sum(self.datos) / n
                varianza = sum((x - media)**2 for x in self.datos) / n
                desviacion = math.sqrt(varianza)
                pe = norm.cdf(self.datos[i-1], media, desviacion)
            
            # Calcular diferencia
            diferencia = abs(po - pe)
            max_ks = max(max_ks, diferencia)
            
            # Mostrar algunos puntos en la tabla (no todos para no saturar)
            if i % (n // 20) == 0 or i == n:
                self.resultados.append((
                    round(self.datos[i-1], 4) if i > 0 else "",
                    "",
                    1,
                    round(pe, 4),
                    round(po, 4),
                    round(pe, 4),
                    round(diferencia, 4),
                    round(max_ks, 4)
                ))
        
        # Valor crítico
        self.estadistico = max_ks
        self.valor_critico = 1.36 / math.sqrt(n)
        
        # Conclusión
        if self.estadistico <= self.valor_critico:
            self.conclusion = "Conclusión: No se rechaza la hipótesis de que los datos siguen la distribución"
        else:
            self.conclusion = "Conclusión: Se rechaza la hipótesis de que los datos siguen la distribución"