from scipy.stats import chi2, norm
import math
import numpy as np

class ChiCuadrado:
    def __init__(self, datos, distribucion, intervalos):
        self.datos = datos
        self.distribucion = distribucion
        self.intervalos = intervalos
        self.resultados = []
        self.estadistico = 0
        self.valor_critico = 0
        self.conclusion = ""
        self.advertencias = []
        
        self._validar_datos()
        self._calcular_prueba()
        
    def _validar_datos(self):
        """Validaciones previas al cálculo de la prueba"""
        n = len(self.datos)
        
        # Validación de tamaño mínimo de muestra
        if n < 30:
            self.advertencias.append(f"Advertencia: Tamaño de muestra pequeño (n={n}). Los resultados pueden no ser confiables.")
        
        # Validación de número de intervalos
        if self.intervalos > n/5:
            self.intervalos = max(1, int(math.sqrt(n)))
            self.advertencias.append(f"Advertencia: Demasiados intervalos para el tamaño de muestra. Se ajustó a {self.intervalos} intervalos.")
    
    def _agrupar_intervalos(self, frec_obs, frec_esp, limites_inf, limites_sup):
        """Agrupa intervalos adyacentes cuando frec_esp < 5"""
        i = 0
        while i < len(frec_esp):
            if frec_esp[i] < 5 and len(frec_esp) > 1:
                # Agrupar con el siguiente intervalo (o anterior si es el último)
                j = i+1 if i < len(frec_esp)-1 else i-1
                
                frec_obs[i] += frec_obs.pop(j)
                frec_esp[i] += frec_esp.pop(j)
                limites_sup[i] = limites_sup.pop(j)
                
                self.advertencias.append(f"Se agruparon intervalos {i} y {j} por frecuencia esperada <5")
                i = max(0, i-1)  # Revisar nuevamente desde el anterior
            else:
                i += 1
        return frec_obs, frec_esp, limites_inf, limites_sup
    
    def _calcular_prueba(self):
        n = len(self.datos)
        min_val = min(self.datos)
        max_val = max(self.datos)
        
        # Ajuste automático de intervalos si hay muchos valores únicos
        valores_unicos = len(set(self.datos))
        if valores_unicos < self.intervalos:
            self.intervalos = valores_unicos
            self.advertencias.append(f"Se redujeron los intervalos a {valores_unicos} por valores únicos insuficientes")
        
        # Cálculo inicial de intervalos
        frec_obs, limites_inf, limites_sup = self._calcular_frecuencias_observadas(min_val, max_val)
        frec_esp = self._calcular_frecuencias_esperadas(n, limites_inf, limites_sup)
        
        # Agrupamiento automático si frecuencias esperadas <5
        frec_obs, frec_esp, limites_inf, limites_sup = self._agrupar_intervalos(frec_obs, frec_esp, limites_inf, limites_sup)
        
        # Cálculo del estadístico Chi-cuadrado
        chi_acumulado = 0
        for i in range(len(frec_esp)):
            if frec_esp[i] > 0:
                chi = (frec_obs[i] - frec_esp[i])**2 / frec_esp[i]
                chi_acumulado += chi
                
                self.resultados.append((
                    round(limites_inf[i], 4),
                    round(limites_sup[i], 4),
                    frec_obs[i],
                    round(frec_esp[i], 4),
                    round(chi, 4),
                    round(chi_acumulado, 4)
                ))
        
        # Grados de libertad
        m = self._calcular_parametros_estimados()
        gl = max(1, len(frec_esp) - 1 - m)  # Mínimo 1 grado de libertad
        
        # Valor crítico y conclusión
        self.estadistico = chi_acumulado
        self.valor_critico = chi2.ppf(0.95, gl)
        
        self.conclusion = self._generar_conclusion(gl)
    
    def _calcular_frecuencias_observadas(self, min_val, max_val):
        """Calcula frecuencias observadas y límites de intervalos"""
        frec_obs = [0] * self.intervalos
        limites_inf = []
        limites_sup = []
        ancho = (max_val - min_val) / self.intervalos
        
        for i in range(self.intervalos):
            lim_inf = min_val + i * ancho
            lim_sup = min_val + (i + 1) * ancho
            if i == self.intervalos - 1:
                lim_sup = max_val + 0.0001  # Incluir valor máximo
            
            limites_inf.append(lim_inf)
            limites_sup.append(lim_sup)
            
            for x in self.datos:
                if lim_inf <= x < lim_sup:
                    frec_obs[i] += 1
        
        return frec_obs, limites_inf, limites_sup
    
    def _calcular_frecuencias_esperadas(self, n, limites_inf, limites_sup):
        """Calcula frecuencias esperadas según la distribución"""
        frec_esp = []
        
        if self.distribucion == "Uniforme [a,b]":
            for i in range(len(limites_inf)):
                frec_esp.append(n / len(limites_inf))
                
        elif self.distribucion == "Exponencial":
            lambd = 1 / (sum(self.datos) / n)
            for i in range(len(limites_inf)):
                lim_inf = max(limites_inf[i], 0)
                lim_sup = limites_sup[i]
                prob = math.exp(-lambd * lim_inf) - math.exp(-lambd * lim_sup)
                frec_esp.append(prob * n)
                
        elif self.distribucion == "Normal":
            media = np.mean(self.datos)
            desviacion = np.std(self.datos)
            for i in range(len(limites_inf)):
                prob = norm.cdf(limites_sup[i], media, desviacion) - norm.cdf(limites_inf[i], media, desviacion)
                frec_esp.append(prob * n)
        
        return frec_esp
    
    def _calcular_parametros_estimados(self):
        """Determina cuántos parámetros se estimaron para la distribución"""
        if self.distribucion == "Uniforme [a,b]":
            return 0
        elif self.distribucion == "Exponencial":
            return 1
        elif self.distribucion == "Normal":
            return 2
        return 0
    
    def _generar_conclusion(self, gl):
        """Genera la conclusión de la prueba con información adicional"""
        base = ("No se rechaza la hipótesis de que los datos siguen la distribución"
               if self.estadistico <= self.valor_critico
               else "Se rechaza la hipótesis de que los datos siguen la distribución")
        
        detalles = [
            f"Estadístico χ² = {self.estadistico:.4f}",
            f"Valor crítico = {self.valor_critico:.4f} (α=0.05, gl={gl})",
            f"Intervalos utilizados: {len(self.resultados)}"
        ]
        
        if self.advertencias:
            detalles.append("\nAdvertencias:")
            detalles.extend(self.advertencias)
        
        return f"{base}\n\n" + "\n".join(detalles)