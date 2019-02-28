def parser(file):
    with open(file, 'r') as f:
        n = int(f.readline())
        fotos = []
        for line in f:
            a = line.split('\n')
            s = a[0].split(' ')
            foto = {'ori':s[0], 'tags':s[2:]}
            fotos.append(foto)
    return n, fotos
    
