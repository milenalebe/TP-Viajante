
import random
import time
import numpy
import xlsxwriter
from operator import attrgetter
import os
import pandas as pd
import matplotlib.pyplot as plt


"Datos de las ciudades"

#por ahora, esta harcodeado:
cantCiudades = 23


"EJERCICIO: Método de Selección: Ruleta. Método de Crossover: 1 Punto. Método de Mutación: invertida."
"Datos del algoritmo genetico (para distintos ejercicios, a menos que cambie el metodo de crossover y mutacion, solo hay que modificar estos datos y f(x))"
pCrossover = 0.75
pMutacion = 0.05
cantIndividuos = 10
cantGenes = cantCiudades
ciclos = 200
tamanoElite = 2
nombreExcel = 'ag.xlsx'
"Variables globales"




class Poblacion:
    def __init__(self,cromosomas):
        self.cromosomas = cromosomas
        
        self.cromMaxCiclo = Cromosoma() #Inicializamos el cromosoma maximo del ciclo un cromosoma con objetivo 0 (para fxMax usamos el objeto del cromosoma maximo)
        self.fxMin = 100
        self.fxSum = 0
        self.fxProm = 0
    
    #Etapa 2: Guardado de datos
    def calcularYSetearDatos(self):
        for cromosoma in self.cromosomas:
            
            #Calculo del fxMax
            if(cromosoma.fx > self.cromMaxCiclo.fx):
                self.cromMaxCiclo = cromosoma

            #Calculo del fxMin
            if(cromosoma.fx < self.fxMin):
                self.fxMin = cromosoma.fx
            
            #Calculo de la suma
            self.fxSum += cromosoma.fx
        
        #Calculo del promedio
        self.fxProm = (self.fxSum/len(self.cromosomas))

        #Calculo del fitness de cada cromosoma
        for cromosoma in self.cromosomas:
            cromosoma.calcularFitness(self.fxSum)

    #Etapa 3: Seleccion
    def seleccionRuleta(self,elitismo):
        individuos = cantIndividuos
        if(elitismo): 
            individuos -= 2

        pares = []
        for i in range(int(individuos/2)):
            pares.append([])
            for j in range(2):
                pares[i].append(random.choices(self.cromosomas,self.getListaFtn())[0])

        return pares

    #Etapa 4: Crossover y mutación
    def aplicarCrossoverMutacion(self,pares):
        #Aplica tanto el crossover como la mutacion (solo en caso de que hayan sido aprobados)
        sigPoblacion = []
        for par in pares:
            if(self.realizar(pCrossover)):
                puntoCorte = random.randint(0,cantGenes)
            else:
                puntoCorte = cantGenes
            
            for i in range(2):
                indRec = []
                for j in range(puntoCorte):
                    indRec.append(par[i].indRec[j])
                for j in range(puntoCorte,cantGenes):
                    indRec.append(par[abs(i-1)].indRec[j])
                
                if(self.realizar(pMutacion)):
                    puntoAMutar = random.randint(0,cantGenes-1)
                    indRec[puntoAMutar] = abs(indRec[puntoAMutar]-1)

                cromosoma = Cromosoma(indRec)

                sigPoblacion.append(cromosoma)
        return sigPoblacion
    def realizar(self,probabilidadTrue):
        #Recibe una probabilidad para realizar algo y devuelve True si se debe realizar o False si no (usado para decidir crossover y mutacion)
        return (random.choices([0,1],[1-probabilidadTrue,probabilidadTrue])[0] == 1)

    #Helpers
    def aplicarElitismo(self,tamanoElite):
        cromosomasElite = []
        for i in range(tamanoElite):
            unMaximo = max(self.cromosomas,key=attrgetter('ftn')) #Sacamos el cromosoma con mayor fitness

            #Lo eliminamos de los cromosomas de la pobl actual y a la vez lo asignamos a la lista de elite (pop elimina el objeto y a su vez lo devuelve)
            cromosomasElite.append(self.cromosomas.pop(self.cromosomas.index(unMaximo))) 
        
        return cromosomasElite
    def getListaFtn(self):
        listaFtn = []
        for cromosoma in self.cromosomas:
            listaFtn.append(cromosoma.ftn)
        return listaFtn



class Cromosoma:
    def __init__(self, indRec=None):
        #Para el cromosoma maximo inicial, lo inicializamos con indRec = None, en ese caso lo unico que nos interesa es el Fx para luego poder compararlo
        if(indRec != None):
            self.indRec = indRec
            self.fx = self.f()
            self.ftn = 0
        else:
            self.fx = 0
    
    def calcularFitness(self,sumaFx):
        self.ftn = (self.fx/sumaFx)

    def f(self):
        #Obtiene la distancia total del recorrido, segun el orden de recorrido propuesto
        return 1
    
    def getBinario(self):
        #Concatena en un string todos los elementos del cromosoma (genes) y los devuelve
        binario = ""
        for gen in self.indRec:
            binario += str(gen)

        return binario


#Etapa 1: Generación de la población inicial

def getPoblacionInicial():
    cromosomas = []
    for indRec in generarPoblacionInicial():
        cromosomas.append(Cromosoma(indRec))
    return cromosomas
def generarPoblacionInicial():
    return [generarCromosomaInicial() for i in range(cantIndividuos)]
def generarCromosomaInicial():
    rec = list(range(1,cantGenes+1))
    random.shuffle(rec)
    return rec



def empezar():
    global poblacion,cromosomaMaximoCorrida
    #Inicializaciones
    #inicializarExcel() #Para tabla y graficos
    cromosomaMaximoCorrida = Cromosoma() #Inicializamos el cromosoma maximo como un cromosoma con objetivo 0
    #elitismo = 1
    poblacion = Poblacion(getPoblacionInicial())

empezar()

for c in poblacion.cromosomas:
    print(c.getBinario())
