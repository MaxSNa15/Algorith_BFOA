# Alineamiento de secuencias de ADN
# Codigo creado por: David Del Toro
# Ultima modificación: 08/05/2023
# Descripción: Programa que simula el alineamiento de secuencias de ADN

# Importando librerías
from colorama import Fore, Style # Librería para dar color a la salida de texto en la consola
import numpy as np # Librería para trabajar con matrices
import random as rd # Librería para generar números aleatorios
import bacterias_str as bacs # Librería para trabajar con bacterias

# Variables constantes
_GENES = ['A', 'C', 'T', 'G']  # Los cuatro genes posibles en las secuencias de ADN
_NUM_BACTERIAS = 2 # Número de bacterias en cada generación

# Variables globales
NUM_CICLOS = 100 # Número de ciclos
NUM_PASOS = 10 # Número de pasos
LONGITUD_ADN = 654  # Longitud de las secuencias de ADN
GENERACION = 1 # Número de generaciones
PROB_ELIMINACION = 0.25 # Probabilidad de eliminación
LIMITES = [-10, 10] # Límites de la población
FAMILIA = 1 # Número de familias


# Función para generar una secuencia de ADN
def generar_adn():
    # Generando la población de bacterias
    seudo_poblcion = np.random.randint(0, 4, size=(_NUM_BACTERIAS, LONGITUD_ADN))  # Generando la población de bacterias 
    poblacion_bacterias = [] # Lista para almacenar las bacterias
    # Iterar a través de cada fila de la matriz de seudo población 
    for i in range(seudo_poblcion.shape[0]):
        fila_letra = []
        # Iterar a través de cada columna de la matriz de seudo población
        for j in range(seudo_poblcion.shape[1]):
            fila_letra.append(_GENES[seudo_poblcion[i][j]])
        # Agregar la lista de cadenas de la fila a la matriz de letras de bases
        poblacion_bacterias.append(fila_letra) 
    return poblacion_bacterias # Retornar la población de bacterias

# Función para imprimir la población de bacterias
def imprimir_poblacion(x):
    # Iterar a través de cada elemento de la matriz de bacterias
    for i in range(len(x)):
        for j in range(len(x[0])):
            # Imprimir la matriz de bacterias
            print(x[i][j], end='')
        print('') 

def quimiotaxis(bacteria):
    # Realiza una permutación aleatoria de la bacteria
    nueva_bacteria = list(bacteria)  # Creamos una copia para no modificar la original
    rd.shuffle(nueva_bacteria)
    return nueva_bacteria

# Función para calcular la función objetivo de la población de bacterias
def funcion_objetivo(adn):
    resultados = [] # Lista para almacenar los resultados
    for base1, base2 in zip(bacs.strain, adn): # Iterar a través de cada elemento de las secuencias de ADN zip permite iterar a través de dos listas al mismo tiempo
        if base1 == base2:
            resultados.append(1) 
        else:
            resultados.append(0) 
    suma = sum(resultados)
    cant = len(resultados)
    porcetaje = (suma / cant) * 100 # Se calcula el porcentaje de similitud entre las secuencias de ADN
    return porcetaje

"""# Función para realizar un gap en las secuencias de ADN
def gap(adn):
    resultado = [] # Lista para almacenar las secuencias de ADN con el gap
    posicion = rd.randint(0, len(adn)) 
    adn.insert(posicion, '-')
    resultado.append(adn)
    return resultado"""

def reproduccion(poblacion, costos):
    # Ordena la población y los costos en función de los costos
    orden = np.argsort(costos)
    poblacion = poblacion[orden[0]]
    costos = costos[orden[0]]
    # Las bacterias más saludables se reproducen
    poblacion = np.repeat(poblacion[:len(poblacion)//2], 2, axis=0)
    return poblacion, costos

def eliminacion_y_dispersion(poblacion, prob_eliminacion, limites):
    # Decide aleatoriamente qué bacterias se eliminan
    eliminacion = np.random.uniform(size=len(poblacion)) < prob_eliminacion
    # Introduce nuevas bacterias en la población
    for i in range(len(poblacion)):
        if eliminacion[i]:
            poblacion[i] = np.random.uniform(limites[0], limites[1], size=1)[0]
    return poblacion


# Creando la sentencia main
if __name__ == '__main__':
    print(Fore.RED + 'programa iniciado')
    print(Fore.RED + 'Alineamiento de secuencias de ADN')
    print(Fore.WHITE + '='*50)

    poblacion = generar_adn()

    for ciclo in range(NUM_CICLOS):
        # Calcular los costos iniciales
        costos = np.array([funcion_objetivo(bacteria) for bacteria in poblacion]) # Se calcula la función objetivo de cada bacteria

        print(Fore.YELLOW + 'costos: ', costos)

        for paso in range(NUM_PASOS): 
            # Guarda la población y los costos actuales
            poblacion_antigua = poblacion.copy()
            costos_antiguos = costos.copy()

            # Realiza un paso de quimiotaxis para cada bacteria
            for i in range(_NUM_BACTERIAS):

                poblacion[i] = quimiotaxis(poblacion[i])
                costos[i] = funcion_objetivo(poblacion[i])
            
            # Si el nuevo costo es peor, revierte el paso
            for i in range(_NUM_BACTERIAS):
                if costos[i] > costos_antiguos[i]:
                    poblacion[i] = poblacion_antigua[i]
                    costos[i] = costos_antiguos[i]

        # Reproducción
        poblacion, costos = reproduccion(poblacion, costos)
        
        
        # Eliminación y dispersión
        poblacion = eliminacion_y_dispersion(poblacion, PROB_ELIMINACION, LIMITES)
        break
    
    # Imprime la mejor solución encontrada
    mejor_indice = np.argmin(costos)
    print('Mejor solución:', poblacion[mejor_indice])
