import sys
import os.path
import combinar
from parser import *

def principal():
	if(len(sys.argv) != 2):
		print('Formato de ejecucion:\n\t python main.py <ficheroParseo.txt>')
		return	

	fichero = sys.argv[1]	
	numFotos, photos = parser(fichero) 
	
	verts=photos['v']
	hors=photos['h']
	slides=[]
	
	slides.append(hors[0]['id'])
	actual_set=hors[0]['tags']
	hors.remove(hors[0])
	aux_v = combinar.combinarVerticales(verts)
	i=-1
	while len(hors) + len(aux_v) > 1:
		maximum=-1
		max_f = None
		aux = hors + aux_v
			# Pruebo las horizontales
		for foto in aux:
			c_set = foto['tags']
			valor = min(len(c_set.intersection(actual_set)), len(c_set.difference(actual_set)), len(actual_set.difference(c_set)))
			if valor > maximum:
				maximum = valor
				max_f = foto
		# Para borrarlo
		slides.append(max_f['id'])
		if (len(max_f['id'].split(' ')) > 1):
			buff = []
			for cosa in aux_v:
				if cosa['f1'] != max_f['f1'] and cosa['f2'] != max_f['f2'] and cosa['f1'] != max_f['f2'] and cosa['f2'] != max_f['f1']:
					buff.append(cosa)
			aux_v = buff
		else:
			hors.remove(max_f)
		actual_set = max_f['tags']
		i+=1
		print(len(slides), slides[i])

	aux = hors + aux_v
	if len(aux) > 0:
		slides.append(aux[0]['id'])
	with open('out.txt', 'w') as f:
		f.writelines(str(len(slides))+'\n')
		for s in slides:
			f.writelines(str(s)+'\n')

if(__name__ == '__main__'):
  principal()
