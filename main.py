from ingredient import *
from pizza import *
from hashParser import *
import sys
import os.path

def principal():
	if(len(sys.argv) != 2):
		print('Formato de ejecucion:\n\t python main.py <ficheroPizza.txt>')
		return	

	fichero = sys.argv[1]	
	if(os.path.isfile(fichero) == False):
		print('El fichero ' + fichero + 'no existe o no es un archivo valido, pruebe con un archivo valido:\n\t python main.py <ficheroPizza.txt>')
		return

	pizza = Pizza(fichero)
	pizza.cutPizza()

if(__name__ == '__main__'):
	principal()