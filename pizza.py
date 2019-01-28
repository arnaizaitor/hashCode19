import os

class Ingredient:
	def __init__(ingredient, type):
		ingredient.data = [ingredient.type, True] #type es si es 'T' o 'M'

	def tipo(ingredient):
		return ingredient.type

	def presente(ingredient):
		return ingredient.data[1]

	def cortar(ingredient): #llamar para cada ingrediente de un trozo cortado
		if(ingredient.data[1]):
			ingrediente.data[1] = False
			return True
		else:
			return False #ya estaba cortado

class Pizza:
	def __init__(pizza, file):
		#abrir fichero, leer, rellenar pizza con ingredientes apropiados
		f = open(file, "r")

		columns = 
		rows = 

		pizza.data = [[Ingredient() for j in range(columns)] for i in range(rows)] #falta llenar el inicializador de Igredient con cosas del fichero
		pizza.minIngr = 
		pizza.maxIngr = 

	#funcion objetivo
	def cutPizza(pizza):


#completar
if(name == '__main__'):

	pizza = Pizza(fichero) #pasarselo por linea de comandos
	pizza.cutPizza()




			


