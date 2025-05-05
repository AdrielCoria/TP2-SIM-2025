from scipy.stats import chi2, norm  # Añade norm a los imports
import math

class ChiCuadrado:
    def __init__(self, datos, distribucion, intervalos):
        self.datos = datos
        self.distribucion = distribucion
        self.intervalos = intervalos
        self.resultados = []
        self.estadistico = 0
        self.valor_critico = 0
        self.conclusion = ""
        
        self._calcular_prueba()
        
    def _calcular_prueba(self):
        # Calcular frecuencias observadas
        min_val = min(self.datos)
        max_val = max(self.datos)
        ancho_intervalo = (max_val - min_val) / self.intervalos
        
        frec_obs = []
        limites_inf = []
        limites_sup = []
        
        for i in range(self.intervalos):
            lim_inf = min_val + i * ancho_intervalo
            lim_sup = min_val + (i + 1) * ancho_intervalo
            if i == self.intervalos - 1:
                lim_sup = max_val + 0.0001  # Asegurar inclusión del valor máximo
            
            count = sum(1 for x in self.datos if lim_inf <= x < lim_sup)
            frec_obs.append(count)
            limites_inf.append(lim_inf)
            limites_sup.append(lim_sup)
        
        # Calcular frecuencias esperadas según la distribución
        frec_esp = []
        n = len(self.datos)
        
        if isinstance(self.distribucion, str):
            # Manejo para cuando solo se pasa el nombre de la distribución
            if self.distribucion == "Uniforme [a,b]":
                a = min(self.datos)
                b = max(self.datos)
                for i in range(self.intervalos):
                    lim_inf = max(limites_inf[i], a)
                    lim_sup = min(limites_sup[i], b)
                    prob = (lim_sup - lim_inf) / (b - a) if b != a else 0
                    frec_esp.append(prob * n)
            
            elif self.distribucion == "Exponencial":
                lambd = 1 / (sum(self.datos) / n)  # Estimación de lambda
                for i in range(self.intervalos):
                    lim_inf = max(limites_inf[i], 0)
                    lim_sup = limites_sup[i]
                    prob = math.exp(-lambd * lim_inf) - math.exp(-lambd * lim_sup)
                    frec_esp.append(prob * n)
            
            elif self.distribucion == "Normal":
                media = sum(self.datos) / n
                varianza = sum((x - media)**2 for x in self.datos) / n
                desviacion = math.sqrt(varianza)
                
                for i in range(self.intervalos):
                    lim_inf = limites_inf[i]
                    lim_sup = limites_sup[i]
                    prob = norm.cdf(lim_sup, media, desviacion) - norm.cdf(lim_inf, media, desviacion)
                    frec_esp.append(prob * n)
        else:
            # Manejo para cuando se pasa el objeto distribución
            if hasattr(self.distribucion, 'cdf'):
                # Usar el método cdf del objeto distribución
                for i in range(self.intervalos):
                    lim_inf = limites_inf[i]
                    lim_sup = limites_sup[i]
                    prob = self.distribucion.cdf(lim_sup) - self.distribucion.cdf(lim_inf)
                    frec_esp.append(prob * n)
            else:
                raise ValueError("El objeto distribución no tiene método cdf")
        
        # Calcular estadístico Chi-cuadrado
        chi_acumulado = 0
        for i in range(self.intervalos):
            if frec_esp[i] > 0:
                chi = (frec_obs[i] - frec_esp[i])**2 / frec_esp[i]
                chi_acumulado += chi
                
                if frec_esp[i] >= 5:  # Regla de Cochran: frec esperada >= 5
                    self.resultados.append((
                        round(limites_inf[i], 4),
                        round(limites_sup[i], 4),
                        frec_obs[i],
                        round(frec_esp[i], 4),
                        round(chi, 4),
                        round(chi_acumulado, 4)
                    ))
        
        # Determinar grados de libertad
        if isinstance(self.distribucion, str):
            if self.distribucion == "Uniforme [a,b]":
                m = 0  # No se estiman parámetros
            elif self.distribucion == "Exponencial":
                m = 1  # Se estima lambda
            elif self.distribucion == "Normal":
                m = 2  # Se estiman media y desviación
        else:
            # Si es un objeto, asumimos que los parámetros están fijos
            m = 0
            
        k = len([f for f in frec_esp if f >= 5])  # Número de intervalos válidos
        gl = k - 1 - m if (k - 1 - m) > 0 else 1  # Mínimo 1 grado de libertad
        
        # Valor crítico
        self.estadistico = chi_acumulado
        self.valor_critico = chi2.ppf(0.95, gl) if gl > 0 else 0
        
        # Conclusión
        self.conclusion = ("Conclusión: No se rechaza la hipótesis de que los datos siguen la distribución"
                         if self.estadistico <= self.valor_critico
                         else "Conclusión: Se rechaza la hipótesis de que los datos siguen la distribución")