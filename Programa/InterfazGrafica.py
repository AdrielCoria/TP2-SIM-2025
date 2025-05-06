import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from distribuciones.Uniforme import Uniforme
from distribuciones.Normal import Normal
from distribuciones.Exponencial import Exponencial
from pruebas.ChiCuadrado import ChiCuadrado
from pruebas.KS import KS

class AplicacionGeneradora:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Generador de Números Aleatorios")
        self.ventana.geometry("900x600")
        
        # Paleta de colores moderna
        self.colores = {
            'fondo': '#f8f9fa',
            'panel': '#ffffff',
            'accent': '#6c757d',
            'texto': '#495057',
            'boton': '#6c757d',
            'boton_hover': '#5a6268',
            'exito': '#28a745',
            'error': '#dc3545'
        }
        
        # Variables de control
        self.distribucion_seleccionada = tk.StringVar()
        self.tamano_muestra = tk.StringVar()
        self.intervalos_seleccionados = tk.StringVar()
        
        # Parámetros para cada distribución
        self.a_Uniforme = tk.StringVar()
        self.b_Uniforme = tk.StringVar()
        self.lambda_exponencial = tk.StringVar()
        self.media_Normal = tk.StringVar()
        self.desviacion_Normal = tk.StringVar()
        
        # Datos generados
        self.datos_generados = []
        self.prueba_chi = None
        self.prueba_ks = None
        
        # Configurar la interfaz
        self._configurar_interfaz()
        
    def ejecutar(self):
        self.ventana.mainloop()
        
    def _configurar_interfaz(self):
        # Configurar estilo
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configurar colores
        style.configure('.', 
                       background=self.colores['fondo'],
                       foreground=self.colores['texto'],
                       font=('Segoe UI', 10))
        
        style.configure('TFrame', background=self.colores['fondo'])
        style.configure('TLabel', background=self.colores['fondo'], foreground=self.colores['texto'])
        style.configure('TButton', 
                       background=self.colores['boton'],
                       foreground='white',
                       padding=8,
                       borderwidth=0)
        style.map('TButton',
                 background=[('active', self.colores['boton_hover'])])
        
        style.configure('TEntry', 
                      fieldbackground='white',
                      bordercolor='#ced4da',
                      lightcolor='#ced4da',
                      darkcolor='#ced4da')
        
        style.configure('TCombobox', fieldbackground='white')
        style.configure('Treeview', 
                      background='white',
                      fieldbackground='white',
                      foreground=self.colores['texto'])
        
        # Configurar ventana principal
        self.ventana.configure(bg=self.colores['fondo'])
        
        # Contenedor principal
        main_frame = ttk.Frame(self.ventana, padding=(20, 15))
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Panel superior - Controles
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Sección izquierda - Configuración básica
        config_frame = ttk.LabelFrame(control_frame, text=" Configuración ", padding=15)
        config_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 15))
        
        ttk.Label(config_frame, text="Tamaño de muestra:").grid(row=0, column=0, sticky='w', pady=3)
        ttk.Entry(config_frame, textvariable=self.tamano_muestra, width=15).grid(row=0, column=1, pady=3)
        
        ttk.Label(config_frame, text="Distribución:").grid(row=1, column=0, sticky='w', pady=3)
        cb_dist = ttk.Combobox(config_frame, textvariable=self.distribucion_seleccionada, 
                             values=["Uniforme [a,b]", "Exponencial", "Normal"], 
                             state="readonly", width=13)
        cb_dist.grid(row=1, column=1, pady=3)
        cb_dist.bind("<<ComboboxSelected>>", self._mostrar_parametros_distribucion)
        
        ttk.Label(config_frame, text="Intervalos:").grid(row=2, column=0, sticky='w', pady=3)
        ttk.Combobox(config_frame, textvariable=self.intervalos_seleccionados, 
                    values=["10", "15", "20", "25"], state="readonly", width=13).grid(row=2, column=1, pady=3)
        
        # Sección derecha - Parámetros
        self.frame_parametros = ttk.LabelFrame(control_frame, text=" Parámetros ", padding=15)
        self.frame_parametros.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Botón de generación
        btn_frame = ttk.Frame(control_frame)
        btn_frame.pack(side=tk.LEFT, fill=tk.Y, padx=15)
        ttk.Button(btn_frame, text="Generar Datos", command=self._generar_distribucion).pack(pady=10)
        
        # Panel central - Datos generados
        data_frame = ttk.LabelFrame(main_frame, text=" Datos Generados ", padding=10)
        data_frame.pack(fill=tk.BOTH, expand=True)
        
        self.tabla_datos = ttk.Treeview(data_frame, columns=("valor",), show="headings", height=10)
        self.tabla_datos.heading("valor", text="Valor")
        self.tabla_datos.column("valor", width=120)
        scrollbar = ttk.Scrollbar(data_frame, orient="vertical", command=self.tabla_datos.yview)
        self.tabla_datos.configure(yscrollcommand=scrollbar.set)
        
        self.tabla_datos.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Panel inferior - Botones de visualización
        btn_vis_frame = ttk.Frame(main_frame)
        btn_vis_frame.pack(fill=tk.X, pady=(15, 0))
        
        ttk.Button(btn_vis_frame, text="Ver Histograma", 
                  command=self._mostrar_histograma).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_vis_frame, text="Ver Resultados", 
                  command=self._mostrar_resultados).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_vis_frame, text="Prueba Chi-Cuadrado", 
                  command=self._mostrar_ventana_chi).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_vis_frame, text="Prueba K-S", 
                  command=self._mostrar_ventana_ks).pack(side=tk.LEFT, padx=5)
    
    def _mostrar_parametros_distribucion(self, event=None):
        # Limpiar frame de parámetros
        for widget in self.frame_parametros.winfo_children():
            widget.destroy()
            
        distribucion = self.distribucion_seleccionada.get()
        
        if distribucion == "Uniforme [a,b]":
            ttk.Label(self.frame_parametros, text="A (desde):").grid(row=0, column=0, sticky="w")
            ttk.Entry(self.frame_parametros, textvariable=self.a_Uniforme).grid(row=0, column=1, sticky="ew")
            
            ttk.Label(self.frame_parametros, text="B (hasta):").grid(row=1, column=0, sticky="w")
            ttk.Entry(self.frame_parametros, textvariable=self.b_Uniforme).grid(row=1, column=1, sticky="ew")
            
        elif distribucion == "Exponencial":
            ttk.Label(self.frame_parametros, text="Lambda:").grid(row=0, column=0, sticky="w")
            ttk.Entry(self.frame_parametros, textvariable=self.lambda_exponencial).grid(row=0, column=1, sticky="ew")
            
        elif distribucion == "Normal":
            ttk.Label(self.frame_parametros, text="Media:").grid(row=0, column=0, sticky="w")
            ttk.Entry(self.frame_parametros, textvariable=self.media_Normal).grid(row=0, column=1, sticky="ew")
            
            ttk.Label(self.frame_parametros, text="Desviación estándar:").grid(row=1, column=0, sticky="w")
            ttk.Entry(self.frame_parametros, textvariable=self.desviacion_Normal).grid(row=1, column=1, sticky="ew")
    
    def _generar_distribucion(self):
        try:
            # Validar tamaño de muestra
            if not self.tamano_muestra.get():
                raise ValueError("Debe ingresar el tamaño de muestra")
                
            n = int(self.tamano_muestra.get())
            if n <= 0 or n > 1000000:
                raise ValueError("El tamaño de muestra debe estar entre 1 y 1,000,000")
                
            # Validar intervalos
            if not self.intervalos_seleccionados.get():
                raise ValueError("Debe seleccionar la cantidad de intervalos")
                
            intervalos = int(self.intervalos_seleccionados.get())
            
            # Validar distribución seleccionada
            distribucion = self.distribucion_seleccionada.get()
            if not distribucion:
                raise ValueError("Seleccione una distribución")
                
            # Validar parámetros específicos según la distribución
            if distribucion == "Uniforme [a,b]":
                if not self.a_Uniforme.get() or not self.b_Uniforme.get():
                    raise ValueError("Debe ingresar ambos parámetros (A y B) para la distribución Uniforme")
                    
                a = float(self.a_Uniforme.get())
                b = float(self.b_Uniforme.get())
                if a >= b:
                    raise ValueError("A debe ser menor que B")
                generador = Uniforme(a, b)
                
            elif distribucion == "Exponencial":
                if not self.lambda_exponencial.get():
                    raise ValueError("Debe ingresar el parámetro Lambda para la distribución Exponencial")
                    
                lambd = float(self.lambda_exponencial.get())
                if lambd <= 0:
                    raise ValueError("Lambda debe ser mayor que 0")
                generador = Exponencial(lambd)
                
            elif distribucion == "Normal":
                if not self.media_Normal.get() or not self.desviacion_Normal.get():
                    raise ValueError("Debe ingresar ambos parámetros (Media y Desviación) para la distribución Normal")
                    
                media = float(self.media_Normal.get())
                desviacion = float(self.desviacion_Normal.get())
                if desviacion <= 0:
                    raise ValueError("La desviación estándar debe ser mayor que 0")
                generador = Normal(media, desviacion)
                
            # Generar los datos
            self.datos_generados = generador.generar_muestra(n)
            
            # Actualizar tabla de datos
            self.tabla_datos.delete(*self.tabla_datos.get_children())
            for dato in self.datos_generados:
                self.tabla_datos.insert("", tk.END, values=(dato,))
            
            # Realizar pruebas de bondad de ajuste
            self.prueba_chi = ChiCuadrado(self.datos_generados, distribucion, intervalos)
            self.prueba_ks = KS(self.datos_generados, distribucion, intervalos) 
                
            messagebox.showinfo("Éxito", "Datos generados correctamente", parent=self.ventana)
                
        except ValueError as e:
            messagebox.showerror("Error", f"Parámetros requeridos: {str(e)}", parent=self.ventana)
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {str(e)}", parent=self.ventana)
    
    def _mostrar_histograma(self):
        if not self.datos_generados:
            messagebox.showwarning("Advertencia", "Primero debe generar datos", parent=self.ventana)
            return
            
        # Crear ventana para histograma
        hist_window = tk.Toplevel(self.ventana)
        hist_window.title("Histograma")
        hist_window.geometry("800x500")
        hist_window.configure(bg=self.colores['fondo'])
        
        # Configurar figura
        fig, ax = plt.subplots(figsize=(8, 5))
        intervalos = int(self.intervalos_seleccionados.get())
        n, bins, patches = ax.hist(self.datos_generados, bins=intervalos, 
                                  edgecolor='white', color=self.colores['boton'])
        
        # Personalizar estilo del histograma
        ax.set_title(f'Histograma - Distribución {self.distribucion_seleccionada.get()}', 
                    pad=20, color=self.colores['texto'])
        ax.set_xlabel('Valores', color=self.colores['texto'])
        ax.set_ylabel('Frecuencia', color=self.colores['texto'])
        ax.grid(True, linestyle='--', alpha=0.7)
        
        # Configurar colores del gráfico
        fig.patch.set_facecolor(self.colores['fondo'])
        ax.set_facecolor(self.colores['panel'])
        ax.spines['bottom'].set_color(self.colores['texto'])
        ax.spines['left'].set_color(self.colores['texto'])
        ax.tick_params(axis='x', colors=self.colores['texto'])
        ax.tick_params(axis='y', colors=self.colores['texto'])
        
        # Mostrar en la ventana
        canvas = FigureCanvasTkAgg(fig, master=hist_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Botón para cerrar
        ttk.Button(hist_window, text="Cerrar", command=hist_window.destroy).pack(pady=10)
    
    def _mostrar_resultados(self):
        if not self.prueba_chi or not self.prueba_ks:
            messagebox.showwarning("Advertencia", "Primero debe generar datos", parent=self.ventana)
            return
            
        # Crear ventana para resultados
        res_window = tk.Toplevel(self.ventana)
        res_window.title("Resultados Estadísticos")
        res_window.geometry("700x400")
        res_window.configure(bg=self.colores['fondo'])
        
        # Frame principal
        main_frame = ttk.Frame(res_window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Área de texto con scroll
        texto_resultados = scrolledtext.ScrolledText(
            main_frame, 
            wrap=tk.WORD,
            font=('Consolas', 10),
            background=self.colores['panel'],
            foreground=self.colores['texto'],
            padx=10,
            pady=10
        )
        texto_resultados.pack(fill=tk.BOTH, expand=True)
        
        # Obtener distribución seleccionada
        distribucion = self.distribucion_seleccionada.get()
        
        # Insertar resultados
        texto_resultados.insert(tk.END, 
            f"RESULTADOS PARA DISTRIBUCIÓN {distribucion.upper()}\n")
        texto_resultados.insert(tk.END, "="*50 + "\n\n")
        
        # Resultado Chi-cuadrado
        texto_resultados.insert(tk.END, "PRUEBA CHI-CUADRADO\n")
        texto_resultados.insert(tk.END, "-"*30 + "\n")
        texto_resultados.insert(tk.END, f"Valor calculado: {self.prueba_chi.estadistico:.4f}\n")
        texto_resultados.insert(tk.END, f"Valor crítico: {self.prueba_chi.valor_critico:.4f}\n")
        texto_resultados.insert(tk.END, f"Conclusión: {self.prueba_chi.conclusion}\n\n")
        
        # Resultado KS
        texto_resultados.insert(tk.END, "PRUEBA KOLMOGOROV-SMIRNOV\n")
        texto_resultados.insert(tk.END, "-"*30 + "\n")
        texto_resultados.insert(tk.END, f"Valor calculado: {self.prueba_ks.estadistico:.4f}\n")
        texto_resultados.insert(tk.END, f"Valor crítico: {self.prueba_ks.valor_critico:.4f}\n")
        texto_resultados.insert(tk.END, f"Conclusión: {self.prueba_ks.conclusion}\n")
        
        # Hacer el texto de solo lectura
        texto_resultados.config(state=tk.DISABLED)
        
        # Botón para cerrar
        ttk.Button(main_frame, text="Cerrar", command=res_window.destroy).pack(pady=10)
    
    def _mostrar_ventana_chi(self):
        if not self.prueba_chi:
            messagebox.showwarning("Advertencia", "Primero debe generar una distribución", parent=self.ventana)
            return
            
        ventana_chi = tk.Toplevel(self.ventana)
        ventana_chi.title("Prueba Chi-Cuadrado - Detalles")
        ventana_chi.geometry("800x600")
        ventana_chi.configure(bg=self.colores['fondo'])
        
        # Frame principal
        frame_principal = ttk.Frame(ventana_chi, padding="10")
        frame_principal.pack(fill=tk.BOTH, expand=True)
        
        # Tabla de resultados
        tabla_chi = ttk.Treeview(frame_principal, 
                               columns=("desde", "hasta", "frec_obs", "frec_esp", "chi", "chi_acum"), 
                               show="headings", height=20)
        
        # Configurar columnas
        columnas = [
            ("desde", "Desde", 100),
            ("hasta", "Hasta", 100),
            ("frec_obs", "Frec. Obs", 90),
            ("frec_esp", "Frec. Esp", 90),
            ("chi", "Chi²", 90),
            ("chi_acum", "Chi² Acum", 90)
        ]
        
        for col_id, col_text, col_width in columnas:
            tabla_chi.heading(col_id, text=col_text)
            tabla_chi.column(col_id, width=col_width, anchor=tk.CENTER)
        
        # Agregar scrollbar
        scrollbar = ttk.Scrollbar(frame_principal, orient="vertical", command=tabla_chi.yview)
        tabla_chi.configure(yscrollcommand=scrollbar.set)
        
        # Posicionar widgets
        tabla_chi.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Llenar tabla con datos
        for fila in self.prueba_chi.resultados:
            tabla_chi.insert("", tk.END, values=fila)
        
        # Mostrar conclusiones
        frame_conclusion = ttk.LabelFrame(frame_principal, text="Conclusiones", padding="10")
        frame_conclusion.pack(fill=tk.X, pady=10)
        
        texto_conclusion = tk.Text(frame_conclusion, height=4, wrap=tk.WORD, 
                                 font=("Consolas", 10), 
                                 bg=self.colores['panel'],
                                 fg=self.colores['texto'])
        texto_conclusion.pack(fill=tk.BOTH, expand=True)
        
        texto_conclusion.insert(tk.END, f"Valor calculado: {self.prueba_chi.estadistico:.4f}\n")
        texto_conclusion.insert(tk.END, f"Valor crítico: {self.prueba_chi.valor_critico:.4f}\n")
        texto_conclusion.insert(tk.END, self.prueba_chi.conclusion)
        texto_conclusion.config(state=tk.DISABLED)
        
        # Botón para cerrar
        ttk.Button(frame_principal, text="Cerrar", command=ventana_chi.destroy).pack(pady=10)

    def _mostrar_ventana_ks(self):
        if not self.prueba_ks:
            messagebox.showwarning("Advertencia", "Primero debe generar una distribución", parent=self.ventana)
            return
            
        ventana_ks = tk.Toplevel(self.ventana)
        ventana_ks.title("Prueba Kolmogorov-Smirnov - Detalles")
        ventana_ks.geometry("1000x600")
        ventana_ks.configure(bg=self.colores['fondo'])
        
        # Frame principal
        frame_principal = ttk.Frame(ventana_ks, padding="10")
        frame_principal.pack(fill=tk.BOTH, expand=True)
        
        # Tabla de resultados
        tabla_ks = ttk.Treeview(frame_principal, 
                            columns=("lim_inf", "lim_sup", "frec_obs", "prob_obs", "prob_esp", "po_acum", "pe_acum", "dif", "max_dif"), 
                            show="headings", height=20)
        
        # Configurar columnas
        columnas = [
            ("lim_inf", "Lím. Inf.", 80),
            ("lim_sup", "Lím. Sup.", 80),
            ("frec_obs", "Frec. Obs", 80),
            ("prob_obs", "Prob. Obs", 80),
            ("prob_esp", "Prob. Esp", 80),
            ("po_acum", "PO Acum.", 80),
            ("pe_acum", "PE Acum.", 80),
            ("dif", "Diferencia", 80),
            ("max_dif", "Máx. Dif.", 80)
        ]
        
        for col_id, col_text, col_width in columnas:
            tabla_ks.heading(col_id, text=col_text)
            tabla_ks.column(col_id, width=col_width, anchor=tk.CENTER)
        
        # Agregar scrollbar
        scrollbar = ttk.Scrollbar(frame_principal, orient="vertical", command=tabla_ks.yview)
        tabla_ks.configure(yscrollcommand=scrollbar.set)
        
        # Posicionar widgets
        tabla_ks.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Llenar tabla con datos
        for fila in self.prueba_ks.resultados:
            tabla_ks.insert("", tk.END, values=fila)
        
        # Mostrar conclusiones
        frame_conclusion = ttk.LabelFrame(frame_principal, text="Conclusiones", padding="10")
        frame_conclusion.pack(fill=tk.X, pady=10)
        
        texto_conclusion = tk.Text(frame_conclusion, height=4, wrap=tk.WORD, 
                                font=("Consolas", 10), 
                                bg=self.colores['panel'],
                                fg=self.colores['texto'])
        texto_conclusion.pack(fill=tk.BOTH, expand=True)
        
        texto_conclusion.insert(tk.END, f"Valor calculado: {self.prueba_ks.estadistico:.4f}\n")
        texto_conclusion.insert(tk.END, f"Valor crítico: {self.prueba_ks.valor_critico:.4f}\n")
        texto_conclusion.insert(tk.END, self.prueba_ks.conclusion)
        texto_conclusion.config(state=tk.DISABLED)
        
        # Botón para cerrar
        ttk.Button(frame_principal, text="Cerrar", command=ventana_ks.destroy).pack(pady=10)