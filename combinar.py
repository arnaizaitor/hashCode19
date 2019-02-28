def combinarVerticales(listaVerticales):
	longitud = len(listaVerticales)
	COMBINADA = []

	for i in range(0, longitud):
		for j in range(i, longitud):
			if(i!=j):
				COMBINADA.append([listaVerticales[i], listaVerticales[j]])

	return COMBINADA

if(__name__ == "__main__"):
	C = combinarVerticales([1, 2, 3, 4])			
	print C