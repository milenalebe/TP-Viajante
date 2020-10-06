import numpy as np 
import matplotlib.pyplot as plt 

import pandas as pd
import os


path = 'C:/UTN 2020/Alg. geneticos/viajante/datos.xlsx'
df = pd.read_excel(path) 
# df contiene los datos de ciudades y distancias

recorrido = []
distancias = []

df = df.set_index('name')

#aca esta hardcodeado la ciudad de inicio, y eliminar la fila de esa ciudad de inicio
ciudadini = 'San Luis'
df = df.drop(['San Luis'])
recorrido.append(ciudadini)

def getRecorrido(recorrido=recorrido,distancias=distancias,df=df):
    if (len(recorrido)==len(df.columns)): 
        recorrido.append(sum(distancias))
        recorrido.append(ciudadini)
        return recorrido
    else:
        for col in df.columns:
            if recorrido[len(recorrido)-1] == col: # busca columna de el ultimo añadido
                mascercana = df[col].idxmin()
                distancias.append(df[col][mascercana]) 
                recorrido.append(mascercana)
                df = df.drop([mascercana])
                getRecorrido(recorrido, distancias, df)
                break;
                

getRecorrido()
print("R: ", recorrido)