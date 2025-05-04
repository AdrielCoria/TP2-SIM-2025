import random
from distribuciones.Uniforme import Uniforme
from distribuciones.Exponencial import Exponencial
from distribuciones.Normal import Normal

# Solicita al usuario el tamaño de la muestra
def muestra():
    while True:
        muestra = input("Digite el tamaño de muestra (numero entero entre 0 y 1.000.000): ")
        try: 
            muestra = int(muestra)
            if 0 <= muestra <= 1000000:
                break
            else:
                print("La muestra digitada debe ser entre 0 y 1000000")
        except:
            print("Debe ser un NUMERO entero")
    return muestra

# Solicita al usuario un número mayor a 0, opcionalmente mayor a un límite inferior
def gen_num(b=None):
    try:
        while True:
            n = input()
            n = float(n)
            if b:
                if b < n and n > 0:
                    return n
                else:
                    print("debe ser un numero mayor a cero y mayor al limite inferior")
            else:
                if n > 0:
                    return n
                else:  
                    print("debe ser un numero mayor a cero")
    except:
        print("Debe ser un numero")

# Solicita al usuario la distribución a utilizar y crea una instancia de la clase correspondiente
def distribucion(muestras):
    while True:
        try:
            inter = input("Cantidad de intervalos(10, 15, 20, 25): ")
            inter = int(inter)
            if inter in [10,15,20,25]:
                break
            else:
                print("Deben ser: 10, 15, 20 o 25")
        except:
            print("Digite: 10, 15, 20 o 25")
    
    selec = input("Seleccione la distribucion: \n 1. Uniforme \n 2. Exponencial \n 3. Normal \n")
    
    match selec:
        case "1":
            print("Extremo inferiror: ")
            a = gen_num()
            print("Extremo superior: ")
            b = gen_num(a)
            dist = Uniforme(a, b, muestras, inter)
        case "2": 
            print("lambda: ")  # No se usa "lambda" porque es palabra reservada
            lam = gen_num()
            dist = Exponencial(lam, muestras, inter)
        case "3":
            print("Media: ")
            media = gen_num()
            print("Desviación Estándar")
            desviacion = gen_num()
            dist = Normal(media, desviacion, muestras, inter)
    
    return dist

# Solicita una semilla para el generador de números aleatorios
def semillas():
    try: 
        while True:
            s = input("semilla: ")
            s = int(s)
            if s > 0:
                break
            else: 
                print("Debe ser mayor a cero")
    except:
        print("Debe ser un numero mayor a cero")

# Función principal que ejecuta todo el flujo
def main():
    semilla = semillas()
    random.seed = semilla  # Esto no funciona bien, debería ser random.seed(semilla)
    muestras = muestra()
    dist = distribucion(muestras)
    dist.generar_numeros()
    # dist.mostrar_lista()  # Podés descomentar esto para ver los números generados
    dist.calcular_frecuencias()

# Llamada al programa principal
if __name__ == "__main__":
    main()
