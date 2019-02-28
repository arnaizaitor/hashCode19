def combinarVerticales(listaVerticales):
	longitud = len(listaVerticales)
	COMBINADA = []

	for i in range(0, longitud):
		for j in range(i, longitud):
			if(i!=j):
				COMBINADA.append({'id': listaVerticales[i]['id']+' '+listaVerticales[j]['id'], 'tags':listaVerticales[i]['tags'].union(listaVerticales[j]['tags']), 'f1':listaVerticales[i], 'f2':listaVerticales[j]})
	return COMBINADA
