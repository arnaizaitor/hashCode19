from ingredient import *
from hashParser import *

class Pizza:
	def __init__(pizza, file):
		#abrir fichero, leer, rellenar pizza con ingredientes apropiados
		parser = hashParser()
		results = parser.parseFile(file)

		FIRST = results[0]
		REST = results[1]

		#print(FIRST)
		#print(REST)

		pizza.rows = int(FIRST[0])
		pizza.columns = int(FIRST[1])
		pizza.minIngr = int(FIRST[2])
		pizza.maxIngr = int(FIRST[3])
		

		pizza.data = [[Ingredient(posicX = i, posicY = j) for j in range(pizza.columns)] for i in range(pizza.rows)] #falta llenar el inicializador de Igredient con cosas del fichero

		for i in range(pizza.rows):
			for j in range(pizza.columns):
				pizza.data[i][j].setTipo(REST[i][j])
				#pizza.data[i][j].posicX = i
				#pizza.data[i][j].posicX = j

	def printPizza(pizza):
		print('\n')
		string = ''

		for i in range(pizza.rows):
			for j in range(pizza.columns):
				if(pizza.data[i][j].presente()):
					string = string + str(pizza.data[i][j].tipo()) + ' '
				else:
					continue	
			print(string)		
			string = ''
			
		print('\n')	


	#funcion objetivo
	def cutPizza(pizza):
		return True

			


