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
        
        # Configurar tema oscuro
        #self._configurar_tema_oscuro()
        #self.ventana.attributes('-disabled', True) # Pantalla Completa
        
        self.ventana.geometry("1200x800")
        
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
        
        # Configurar la interfaz
        self._configurar_interfaz()
        
    def ejecutar(self):
        self.ventana.mainloop()
        
    def _configurar_tema_oscuro(self):
        """Configura un tema oscuro personalizado sin necesidad de archivos externos"""
        # Colores principales
        bg_color = '#1e1e1e'  # Fondo oscuro
        fg_color = '#ffffff'  # Texto blanco
        accent_color = '#3a3a3a'  # Color de acento
        entry_bg = '#2d2d2d'  # Fondo de campos de entrada
        
        # Configurar el color de fondo de la ventana principal
        self.ventana.configure(bg=bg_color)
        
        # Configurar estilo para ttk widgets
        style = ttk.Style()
        
        # Usar el tema 'clam' como base porque es más personalizable
        style.theme_use('clam')
        
        # Configurar colores para los diferentes widgets
        style.configure('.', 
                      background=bg_color,
                      foreground=fg_color,
                      fieldbackground=entry_bg)
        
        style.configure('TLabel', 
                      background=bg_color,
                      foreground=fg_color,
                      padding=5)
        
        style.configure('TFrame', 
                      background=bg_color)
        
        style.configure('TButton', 
                      background=accent_color,
                      foreground=fg_color,
                      padding=5,
                      relief='flat')
        
        style.map('TButton',
                background=[('active', '#4a4a4a'), ('pressed', '#5a5a5a')])
        
        style.configure('TEntry', 
                      fieldbackground=entry_bg,
                      foreground=fg_color,
                      insertcolor=fg_color,
                      bordercolor=accent_color,
                      lightcolor=accent_color,
                      darkcolor=accent_color)
        
        style.configure('TCombobox', 
                      fieldbackground=entry_bg,
                      foreground=fg_color,
                      background=accent_color)
        
        style.configure('Treeview',
                      background=entry_bg,
                      foreground=fg_color,
                      fieldbackground=entry_bg)
        
        style.map('Treeview',
                background=[('selected', '#4a4a4a')])
        
        style.configure('Treeview.Heading',
                      background=accent_color,
                      foreground=fg_color,
                      relief='flat')
        
        # Configurar matplotlib para tema oscuro
        plt.style.use('dark_background')
        
        # Configurar el área de texto desplazable
        style.configure('Vertical.TScrollbar',
                      background=accent_color,
                      troughcolor=bg_color,
                      bordercolor=bg_color,
                      arrowcolor=fg_color)
        
        style.configure('Horizontal.TScrollbar',
                      background=accent_color,
                      troughcolor=bg_color,
                      bordercolor=bg_color,
                      arrowcolor=fg_color)
        
        # Configurar el notebook (si usas pestañas)
        style.configure('TNotebook',
                      background=bg_color,
                      bordercolor=bg_color)
        
        style.configure('TNotebook.Tab',
                      background=accent_color,
                      foreground=fg_color,
                      padding=[10, 5])
        
        style.map('TNotebook.Tab',
                background=[('selected', bg_color), ('active', '#4a4a4a')],
                foreground=[('selected', fg_color), ('active', fg_color)])

    def _configurar_interfaz(self):
        # Frame principal
        main_frame = ttk.Frame(self.ventana, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Frame de entrada de datos
        frame_datos = ttk.LabelFrame(main_frame, text="Datos", padding="10")
        frame_datos.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        # Tamaño de muestra
        ttk.Label(frame_datos, text="Tamaño de muestra (hasta 1,000,000):").grid(row=0, column=0, sticky="w")
        ttk.Entry(frame_datos, textvariable=self.tamano_muestra).grid(row=0, column=1, sticky="ew")
        
        # Distribución
        ttk.Label(frame_datos, text="Distribución:").grid(row=1, column=0, sticky="w")
        distribuciones = ["Uniforme [a,b]", "Exponencial", "Normal"]
        cb_distribucion = ttk.Combobox(frame_datos, textvariable=self.distribucion_seleccionada, 
                                      values=distribuciones, state="readonly")
        cb_distribucion.grid(row=1, column=1, sticky="ew")
        cb_distribucion.bind("<<ComboboxSelected>>", self._mostrar_parametros_distribucion)
        
        # Intervalos
        ttk.Label(frame_datos, text="Intervalos para histograma:").grid(row=2, column=0, sticky="w")
        intervalos = ["10", "15", "20", "25"]
        cb_intervalos = ttk.Combobox(frame_datos, textvariable=self.intervalos_seleccionados, 
                                     values=intervalos, state="readonly")
        cb_intervalos.grid(row=2, column=1, sticky="ew")
        
        # Botón generar
        ttk.Button(frame_datos, text="Generar", command=self._generar_distribucion).grid(row=3, column=0, columnspan=2, pady=10)
        
        # Frame de parámetros (se actualiza según la distribución seleccionada)
        self.frame_parametros = ttk.LabelFrame(main_frame, text="Parámetros Requeridos", padding="10")
        self.frame_parametros.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        
        # Frame de resultados (gráfico y tabla)
        frame_resultados = ttk.Frame(main_frame)
        frame_resultados.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        
        # Gráfico
        self.fig, self.ax = plt.subplots(figsize=(8, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=frame_resultados)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        # Tabla de datos generados
        self.tabla_datos = ttk.Treeview(frame_resultados, columns=("valor",), show="headings", height=10)
        self.tabla_datos.heading("valor", text="Variables Generadas")
        self.tabla_datos.column("valor", width=150)
        self.tabla_datos.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Frame de pruebas estadísticas
        frame_pruebas = ttk.Frame(main_frame)
        frame_pruebas.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        
        # Prueba Chi-cuadrado
        frame_chi = ttk.LabelFrame(frame_pruebas, text="Prueba Chi-Cuadrado", padding="5")
        frame_chi.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        self.tabla_chi = ttk.Treeview(frame_chi, columns=("desde", "hasta", "frec_obs", "frec_esp", "chi", "chi_acum"), 
                                     show="headings", height=8)
        self.tabla_chi.heading("desde", text="Desde")
        self.tabla_chi.heading("hasta", text="Hasta")
        self.tabla_chi.heading("frec_obs", text="Frec. Obs.")
        self.tabla_chi.heading("frec_esp", text="Frec. Esp.")
        self.tabla_chi.heading("chi", text="Chi")
        self.tabla_chi.heading("chi_acum", text="Chi Acum.")
        
        for col in ("desde", "hasta", "frec_obs", "frec_esp", "chi", "chi_acum"):
            self.tabla_chi.column(col, width=80)
            
        self.tabla_chi.pack(fill=tk.BOTH, expand=True)
        
        # Prueba KS
        frame_ks = ttk.LabelFrame(frame_pruebas, text="Prueba K-S", padding="5")
        frame_ks.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        self.tabla_ks = ttk.Treeview(frame_ks, columns=("desde", "hasta", "frec_obs", "frec_esp", "po", "pe", "calc", "max"), 
                                    show="headings", height=8)
        self.tabla_ks.heading("desde", text="Desde")
        self.tabla_ks.heading("hasta", text="Hasta")
        self.tabla_ks.heading("frec_obs", text="Frec. Obs.")
        self.tabla_ks.heading("frec_esp", text="Frec. Esp.")
        self.tabla_ks.heading("po", text="Po(ac)")
        self.tabla_ks.heading("pe", text="Pe(ac)")
        self.tabla_ks.heading("calc", text="|Po-Pe|")
        self.tabla_ks.heading("max", text="Max")
        
        for col in ("desde", "hasta", "frec_obs", "frec_esp", "po", "pe", "calc", "max"):
            self.tabla_ks.column(col, width=80)
            
        self.tabla_ks.pack(fill=tk.BOTH, expand=True)
        
        # Resultados de las pruebas
        self.texto_resultados = scrolledtext.ScrolledText(main_frame, width=100, height=5)
        self.texto_resultados.grid(row=3, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        
        # Configurar pesos de filas y columnas
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
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
            
            # Mostrar resultados
            self._mostrar_resultados(distribucion, intervalos)
                
        except ValueError as e:
            messagebox.showerror("Error", f"Parámetros requeridos: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")
    
    def _mostrar_resultados(self, distribucion, intervalos):
        # Mostrar datos en la tabla
        self.tabla_datos.delete(*self.tabla_datos.get_children())
        for dato in self.datos_generados:
            self.tabla_datos.insert("", tk.END, values=(dato,))
        
        # Generar histograma
        self.ax.clear()
        n, bins, patches = self.ax.hist(self.datos_generados, bins=intervalos, edgecolor='black')
        self.ax.set_title(f'Histograma - Distribución {distribucion}')
        self.ax.set_xlabel('Valores')
        self.ax.set_ylabel('Frecuencia')
        self.canvas.draw()
        
        # Realizar pruebas de bondad de ajuste
        prueba_chi = ChiCuadrado(self.datos_generados, distribucion, intervalos)
        prueba_ks = KS(self.datos_generados, distribucion)
        
        # Mostrar resultados de las pruebas
        self._mostrar_resultados_pruebas(prueba_chi, prueba_ks, distribucion)
    
    def _mostrar_resultados_pruebas(self, prueba_chi, prueba_ks, distribucion):
        # Limpiar tablas
        self.tabla_chi.delete(*self.tabla_chi.get_children())
        self.tabla_ks.delete(*self.tabla_ks.get_children())
        
        # Mostrar resultados Chi-cuadrado
        for fila in prueba_chi.resultados:
            self.tabla_chi.insert("", tk.END, values=fila)
        
        # Mostrar resultados KS
        for fila in prueba_ks.resultados:
            self.tabla_ks.insert("", tk.END, values=fila)
        
        # Mostrar conclusiones
        self.texto_resultados.delete(1.0, tk.END)
        self.texto_resultados.insert(tk.END, 
            f"Resultados para distribución {distribucion} (nivel de significancia 0.05):\n\n")
        
        # Resultado Chi-cuadrado
        self.texto_resultados.insert(tk.END, "Prueba Chi-cuadrado:\n")
        self.texto_resultados.insert(tk.END, f"Valor calculado: {prueba_chi.estadistico:.4f}\n")
        self.texto_resultados.insert(tk.END, f"Valor crítico: {prueba_chi.valor_critico:.4f}\n")
        self.texto_resultados.insert(tk.END, prueba_chi.conclusion + "\n")
        
        # Resultado KS
        self.texto_resultados.insert(tk.END, "\nPrueba Kolmogorov-Smirnov:\n")
        self.texto_resultados.insert(tk.END, f"Valor calculado: {prueba_ks.estadistico:.4f}\n")
        self.texto_resultados.insert(tk.END, f"Valor crítico: {prueba_ks.valor_critico:.4f}\n")
        self.texto_resultados.insert(tk.END, prueba_ks.conclusion + "\n")