#!/usr/bin/python
# This Python file uses the following encoding: utf-8
import os, sys
import serial
import RPi.GPIO as GPIO
from datetime import *
import datetime
import time

def getCodigoChipFinal(lista,pos1,pos2):
    a = int(lista[pos1])
    b = int(lista[pos2])
    c = str(a) + str(b)
    return c

def getListaParadasEmergencia(listaD , numParadasEmergencia):  #devuelve la lista de las paradas de emergencia
    lista = []
    i = 10
    n = 0
    limit = numParadasEmergencia * 4
    while (n <= (limit - 1)):
        lista.append(listaD[i])
        n = n + 1
        i = i + 1
    if len(lista) > 0:
        return lista
    else:
        lista = [0]
        return lista

def getObtenerNumeroDeParadasObligatorias(datosB, numP): #devuelve el numero de pradas obligatorias que ocurrieron
     if numP == 0:
        a = int(datosB[10])
        return int(a)
     else:
        b = ((numP * 4))
        c = int(datosB[10 + b])
        return int(c)

def getObtenerListaParadasObligatorias(listaB ,numPO):
    n = len(listaB)
    x = (numPO * 4)
    return listaB[-x : n]

def getOrdenarParada(listac):
    lis = []
    for i in listac:
    	lis.append(int(i))
    return lis
    
def ordenarListaEmergeUnitaria(listaD,posCuatroElmen, numEmerg):                 #funcion q devuelve la lista de emergencia con este formato ['E1', 7, 0, '8:30']
	l1,l2 = [0,0]
	l3 = [0,0,0,0,0]
	l1 = getFourElements(listaD,posCuatroElmen)                     #devuleve  la lista de 4 elementos
	l2 = getOrdenarParadaEmergenciaTransitoria(l1)		#ordena la lista de 4 alimentos
	l3 = agregarIndicadorEmdergencia(l2,numEmerg)
	return l3                                        

def getFourElements(listaUno, posActual):  
	#funcion que devuelve una lista de los 4 elementos de otra lista
	n= 0
	l = []
	while (n <= 3):
		l.append(listaUno[n + posActual])
		n = n +1
	return l
	
def getOrdenarParadaEmergenciaTransitoria(listaD):
    lista = []
    a = int(listaD[0])                            #numero de los q bajan en una parada d eterminada
    b = int(listaD[1])                            #numero de los q suben
    c = int(listaD[2])                            #minutos correspondientes a la hora
    d = int(listaD[3])                            #hora , formato 24 horas
    r = str(d) + ":" + str(c)
    lista.append(b)
    lista.append(a)
    lista.append(r)
    return lista
    
def agregarIndicadorEmdergencia(listaE, numInd):    #funcion que agrega el indicador E1, E2 ...... a su respectiva parada de emergencia
	lis = [0]
	a = numInd
	lis[0] = 'E'  + str(a)
	lis.extend(listaE)
	return lis
	
def ordenarEmergrnciaFinal(listaD):
	n = len(listaD)
	l1 = [0,0,0,0]
	l2 = []
	numEmerg = 1
	posCuatroElmen = 0
	while(n > 0):
		l1 = ordenarListaEmergeUnitaria(listaD,posCuatroElmen, numEmerg)
		posCuatroElmen = posCuatroElmen + 4
		numEmerg = numEmerg + 1
		n = n - 4
		l2.extend(l1)
	return l2
	
def ordenarListaObligatoriaUnitaria(listaD,posCuatroElmen,numParada):
	l = []
	l1,l4 = [0,0]
	l3 = [0,0,0,0,0]
	l1 = getFourElements(listaD,posCuatroElmen)                     #devuleve  la lista de 4 elementos
	l3 = getOrdenarParadaEmergenciaTransitoria(l1)		#ordena la lista de 4 alimentos
	r = str(numParada)
	l.append(r)
	l4 = l + l3
	return l4


def ordenarParadasObligatoriasFinal(listaG):
	n = len(listaG)
	l1 = [0,0,0,0]
	l2 = []
	numParada = 1
	posCuatroElmen = 0
	while(n > 0):
		l1 = ordenarListaObligatoriaUnitaria(listaG,posCuatroElmen, numParada)
		posCuatroElmen = posCuatroElmen + 4
		n = n - 4
		numParada = numParada + 1
		l2.extend(l1)
	return l2

def unirlistas(l1,l2):
	return l1+l2



GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.IN)#PIN ELEGIDO PARA SEÑAL DE AVISO

fecha = date.today()
hoy = datetime.datetime.now()
hora = time.strftime("%X")
impfecha = fecha.strftime("%A %B %d %Y")

contadorVueltas = 0


while True:
	print("antes de comprobar el pin de habilitacion")
	if (GPIO.input(12) == 0):   # COMPROBAMOS LA SEÑAL DE AVISO PARA ABRIR EL PUERTO SERIAL
		print ("Estamos por leer los datos")		
		time.sleep(0.2)

		contadorVueltas = contadorVueltas + 1

		ser = serial.Serial('/dev/ttyAMA0', 4800)  #ABRIMOS EL PUERTO SERIAL PARA RECIVIR LOS DATOS

		datosBuffer = []
		
		n = 0

		while  (n < 27):        ## True o 1  o (n <= 55)
	    		if ser.inWaiting():
        			valor = ser.readline(ser.inWaiting()) 
        			datosBuffer.append(valor)
				n = n + 1 
				          ## guardo uno a uno los datos en una lista
		ser.close()     


		anchoBuffer = len(datosB)
		codigoChip1 = datosB[0:2]
		CodigoChipFinal = getCodigoChipFinal(codigoChip1,0,1)
		cod = CodigoChipFinal

		numParadasEmergencia = int(datosB[9])      #numero de paradas de emergencia que ocurrieron
		numParadasObligatorias = getObtenerNumeroDeParadasObligatorias(datosB, numParadasEmergencia)

		listaParadasEmergencia = getListaParadasEmergencia(datosB, numParadasEmergencia)    #tengo la lista de paradas de emergencia
		listaParadasObligatorias = getObtenerListaParadasObligatorias(datosB,numParadasObligatorias )

		l  = getOrdenarParada(listaParadasObligatorias)
		l2 = getOrdenarParada(listaParadasEmergencia)
		l3 = ordenarEmergrnciaFinal(l2)
		l4 = ordenarParadasObligatoriasFinal(l)
		l5 = unirlistas(l4,l3)

		cabezera = [cod]                           #agregamos la fecha como un elemento de una lista
		lk = str(fecha)
		ln = [lk]
		cabezera.extend(ln)
		cabezera.extend(str(contadorVueltas))
		cabezera.extend(l5)


		fo = open("/home/pi/Desktop/4paradas.txt", "w")   #ruta de SAMBA 
		for elemento in cabezera:
  			 fo.write(elemento + '*');
		fo.write('\n');
		fo.close()

		print 'ok'


		time.sleep(0.2)
	else :
		continue


print("exit")
GPIO.cleanup()