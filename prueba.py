f = open("a_example.in", "r")

i = 0
FIRST = []
REST = []

for line in f:
	if(i == 0):
		FIRST.append(line.split()) #este ya esta
	else:
		newline = line[:-1]
		REST.append(newline)	

	i = i + 1

print(FIRST)
print(REST)		
