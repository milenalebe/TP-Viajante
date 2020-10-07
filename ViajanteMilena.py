import numpy as np 
import matplotlib.pyplot as plt 

import pandas as pd
import os


path = 'C:/Users/Luciano/Desktop/elViajante-main/datos.xlsx'
df = pd.read_excel(path) 
# df contiene los datos de ciudades y distancias

recorrido = []
distancias = []

df = df.set_index('Distancias en kilómetros')  # columna indice

# aca esta hardcodeado la ciudad de inicio, y eliminar la fila de esa ciudad de inicio
ciudadIni = 'San Luis'
df = df.drop(['San Luis'])  #elimina fila de la ciudad
recorrido.append(ciudadIni)

def getRecorrido(recorrido=recorrido,distancias=distancias,df=df):
    if (len(recorrido)==len(df.columns)):  # si entra por true es porque ya termino , parece que no da true nunca
        print(sum(distancias))
        # recorrido.append(sum(distancias)) para que sirve esta linea?
        # recorrido.append(ciudadIni) para que sirve esta linea?
        return recorrido
    else:
        for col in df.columns:
            print(col)
            if recorrido[len(recorrido)-1] == col: # busca columna de el ultimo añadido
                masCercana = df[col].idxmin()  # idxmin devuelve el valor minimo de cada columna
                distancias.append(df[col][masCercana]) 
                recorrido.append(masCercana)
                df = df.drop([masCercana])
                getRecorrido(recorrido, distancias, df)
                
                break
                

                
getRecorrido()
print("R: ", recorrido)
