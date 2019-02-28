import sys
import os.path
from parser import *

def principal():
	if(len(sys.argv) != 2):
		print('Formato de ejecucion:\n\t python main.py <ficheroParseo.txt>')
		return	

	fichero = sys.argv[1]	
	numFotos, photos = parser(fichero) 
	
	numSlides = 0
	verts=photos.v
	hors=photos.h
	slides=[]
	
	slides.append([hors[0].id])
  numSlides+=1
  actual_set=hors[0].tags
  print(actual_set)
  hors.remove(hors[0])
  maximum=-1

  for foto in hors:
    compare_set=foto

if(__name__ == '__main__'):
  principal()
