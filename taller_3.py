


import numpy as np
import matplotlib.pyplot as plt

class Tanque:
    def __init__(self, A, k1, k2, a1, a2):
        self.A = A
        self.k1 = k1
        self.k2 = k2
        self.a1 = a1
        self.a2 = a2
        self.registro = []
        self.label = None
    
    def metodo_euler(self, h0, dt, total_time):
        h = h0
        
        for _ in range(int(total_time / dt)):
            
            dh_dt = (self.k1 * self.a1 - self.k2 * self.a2 * h) / self.A
            h += dt * dh_dt
            
            # Aseguramos que la altura no sea negativa
            h = max(h, 0)
            
            self.registro.append(h)
    
    @staticmethod
    def grafica(dt, *tank_simulations):
        time = np.arange(0, len(tank_simulations[0].registro) * dt, dt)
        
        plt.figure(figsize=(10, 6))
        for tank_simulation in tank_simulations:
            plt.plot(time, tank_simulation.registro, label=tank_simulation.label)
        
        plt.xlabel('Tiempo (s)')
        plt.ylabel('Altura del tanque (m)')
        plt.title('Comparación de Respuestas del Sistema de Tanque con Diferentes Tipos de Válvulas')
        plt.legend()
        plt.grid(True)
        plt.show()

class InputData:
    def obtener_dato(self, mensaje, tipo, rango=None):
        while True:
            try:
                if tipo == "int":
                    dato = int(input(mensaje))
                elif tipo == "float":
                    dato = float(input(mensaje))
                else:
                    raise ValueError("Tipo de dato no válido. Utilice 'int' o 'float'.")
                
                if rango is not None and not rango[0] <= dato <= rango[1]:
                    print("Valor fuera de rango. Ingrese un valor dentro del rango especificado.")
                else:
                    return dato
            except ValueError:
                print("Entrada no válida. Ingrese un número.")


def main():
    
    # Crear una instancia de la clase InputData
    datos = InputData()

    # Solicitar datos al usuario
    h_inicial = datos.obtener_dato("Ingrese la altura inicial del tanque (m): ", "int", (0, 10))
    A = datos.obtener_dato("Ingrese el área transversal del tanque (m^2): ", "int", (1, 100))
    k_in = datos.obtener_dato("Ingrese la constante de la válvula de entrada (k_in): ", "float")
    k_out = datos.obtener_dato("Ingrese la constante de la válvula de salida (k_out): ", "float")
    tiempo_simulacion = datos.obtener_dato("Ingrese el tiempo total de simulación (S): ", "int")
    muestreo = datos.obtener_dato("Ingrese el tiempo de paso para la simulación (S): ", "int")
    alpha = datos.obtener_dato("Ingrese el alpha para la válvula isoporcentual: ", "int", (10, 100))
    a1 = datos.obtener_dato("Ingrese el valor de abertura de la válvula de entrada (0 - 1): ", "float", (0, 1))
    a2 = datos.obtener_dato("Ingrese el valor de abertura de la válvula de salida (0 - 1): ", "float", (0, 1))

    # Definir funciones de apertura de válvula
    def a1_isoporcentual(x):
        return alpha ** (x - 1)

    def a1_ab_rap(x):
        return np.sqrt(x)


    # Crear instancias de la clase Tanque con las funciones de apertura de válvula correspondientes
    tk_lineal = Tanque(A, k_in, k_out, a1, a2)
    tk_lineal.label = 'Lineal'

    tk_isoporcentual = Tanque(A, k_in, k_out, a1_isoporcentual(a1), a2)
    tk_isoporcentual.label = 'Isoporcentual'

    tk_ab_rap = Tanque(A, k_in, k_out, a1_ab_rap(a1), a2)
    tk_ab_rap.label = 'Apertura Rápida'

    # Ejecutar método de Euler y graficar el comportamiento del tanque para cada configuración de válvula
    dt = muestreo
    tk_lineal.metodo_euler(h_inicial, dt, tiempo_simulacion)
    tk_isoporcentual.metodo_euler(h_inicial, dt, tiempo_simulacion)
    tk_ab_rap.metodo_euler(h_inicial, dt, tiempo_simulacion)

    # Graficar todas las alturas en una sola gráfica
    Tanque.grafica(dt, tk_lineal, tk_isoporcentual, tk_ab_rap)

if __name__ == "__main__":
    main()
