
class hashParser:
	def __init__(parser):
		parser.author = 'Aitor'

	def parseFile(parser, file):
		
		f = open(file, "r")

		i = 0
		FIRST = []
		REST = []

		for line in f:
			if(i == 0):
				FIRST.append(line.split()) 
			else:
				newline = line[:-1]
				REST.append(newline)	

			i = i + 1

		return (FIRST, REST)