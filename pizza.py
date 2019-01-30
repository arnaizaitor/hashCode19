from ingredient import *

class Pizza:
	def __init__(pizza, file):
		#abrir fichero, leer, rellenar pizza con ingredientes apropiados
		parser = hashParser()
		results = parser.parseFile(file)

		FIRST = results[0]
		REST = results[1]

		pizza.rows = FIRST[0]
		pizza.columns = FIRST[1]
		pizza.minIngr = FIRST[2]
		pizza.maxIngr = FIRST[3]
		

		pizza.data = [[Ingredient(posicX = i, posicY = j) for j in range(pizza.columns)] for i in range(pizza.rows)] #falta llenar el inicializador de Igredient con cosas del fichero

		for i in range(pizza.rows):
			for j in range(pizza.columns):
				pizza.data[i][j].setTipo(REST[i][j])

	#funcion objetivo
	def cutPizza(pizza):
		return True

	def printPizza(pizza):
		for i in pizza.rows:
			for j in pizza.columns:
				if(pizza.data[i][j].presente()):
					print(str(pizza.data[i][j].tipo()) + ' ')
				else:
					continue	

			print('\n')




			


