from ingredient import *
from hashParser import *
import random

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
		pizza.maxCells = int(FIRST[3])
		pizza.pointsDict = {(0, 0) : 0}
		pizza.numPointsdict = 1
		

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
					string = string + '~' + ' '
			print(string)		
			string = ''

		print('\n')	

	#habria que cambiar el retorno a int para cada caso de error, y asi manejar el caso en que te pases del maximo sin encontrar trozo cortable
	def isCutable(pizza, col1, col2, row1, row2):

		numTomatoes = 0
		numMushrooms = 0
		numElemsCut = (col2-col1+1)*(row2-row1+1)

		if((numElemsCut < (pizza.minIngr*2)) or (numElemsCut > pizza.maxCells)):
			return False
		if(col1 > col2):
			return False
		if(row1 > row2):
			return False
		if((col1 >= pizza.columns) or (col2 >= pizza.columns)):
			return False
		if((row1 >= pizza.rows) or (row2 >= pizza.rows)):
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

		if(numTomatoes < pizza.minIngr or numMushrooms < pizza.minIngr or (numTomatoes + numMushrooms) > pizza.maxCells):
			return False							
		
		return True		

	def cutChunk(pizza, col1, col2, row1, row2): #solo hay que llamar a esta cuando se quiere cortar
		
		if(pizza.isCutable(col1, col2, row1, row2) == False):
			return False

		for i in range(row1, row2+1):
			for j in range(col1, col2+1):
				pizza.data[i][j].cortar()

		#meto en el diccionario de puntos de arranque los puntos abajo izqda +1 y arriba dcha +1 del trozo cortado		
		pizza.pointsDict[(col2 + 1, row1)] = pizza.numPointsdict
		pizza.numPointsdict += 1
		
		pizza.pointsDict[(col1, row2 + 1)] = pizza.numPointsdict
		pizza.numPointsdict += 1

		return True									


	#funcion objetivo
	def cutPizza(pizza):
		pizza.printPizza()
		print ('pizza inicial')
		print('------------------------------------------------------------------------------------------------------------------------------\n')

		while((pizza.columns-1, pizza.rows-1) not in pizza.pointsDict.keys()):
			flag = 0
			keys = pizza.pointsDict.keys()
			modRows = 0
			modCols = 0
			
			while (flag == 0):
				for point in keys:
					if(pizza.cutChunk(point[0], point[0] + modCols, point[1], point[1] + modRows) == True):
						pizza.printPizza()
						print('Trozo cortado entre las columnas %d y %d y las filas %d y %d' %(point[0], point[0] + modCols, point[1], point[1] + modRows))
						print('------------------------------------------------------------------------------------------------------------------------------\n')
						flag = 1
						pizza.pointsDict.pop(point)
						break
				if(random.random() >= 0.5):
					modCols += 1
				else:
					modRows += 1

		print('Procesamiento finalizado\n')			
		return True