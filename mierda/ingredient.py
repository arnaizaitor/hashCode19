class Ingredient:
	def __init__(ingredient, tipo = 'nada', posicX = -1, posicY = -1):
		ingredient.data = [tipo, True] #type es si es 'T' o 'M'
		ingredient.posicX = posicX
		ingredient.posicY = posicY

	def tipo(ingredient):
		return ingredient.data[0]

	def setTipo(ingredient, tipo):
		if((tipo != 'T') and (tipo != 'M')):
			return False

		else:
			ingredient.data[0] = tipo
			return True

	def presente(ingredient):
		return ingredient.data[1]

	def cortar(ingredient): #llamar para cada ingrediente de un trozo cortado
		if(ingredient.data[1]):
			ingredient.data[1] = False
			return True
		else:
			return False #ya estaba cortado