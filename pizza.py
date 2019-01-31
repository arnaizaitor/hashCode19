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


	def isCutable(pizza, col1, col2, row1, row2):
		
		numTomatoes = 0
		numMushrooms = 0
		numElemsCut = (col2-col1+1)*(row2-row1+1)

		if((numElemsCut < (pizza.minIngr*2)) or (numElemsCut > (pizza.maxIngr*2))):
			return False
		if(col1 > col2):
			return False
		if(row1 > row2):
			return False
		if((col1 > pizza.columns) or (col2 > pizza.columns)):
			return False
		if((row1 > pizza.rows) or (row2 > pizza.rows)):
			return False

		for i in range(row1, row2+1):  #vemos que ninguno de los ingredientes en el trozo que queremos cortar haya sido cortado previamente
			for j in range(col1, col2+1):
				if(pizza.data[i][j].presente() == False):
					return False

		for i in range(row1, row2+1): 
			for j in range(col1, col2+1):
				if(pizza.data[i][j].tipo() == 'T'):
					numTomatoes += 1	
				elif(pizza.data[i][j].tipo() == 'M'):
					numMushrooms += 1
				else: 
					return False

		if(numTomatoes < pizza.minIngr or numTomatoes > pizza.maxIngr or numMushrooms < pizza.minIngr or numMushrooms > pizza.maxIngr):
			return False							
		
		return True		

	def cutChunk(pizza, col1, col2, row1, row2): #solo hay que llamar a esta cuando se quiere cortar
		
		if(pizza.isCutable(col1, col2, row1, row2) == False):
			return False

		for i in range(row1, row2+1):
			for j in range(col1, col2+1):
				pizza.data[i][j].cortar()
		
		return True									


	#funcion objetivo
	def cutPizza(pizza):
		return True

			


