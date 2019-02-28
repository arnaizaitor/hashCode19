def parser(file):
    with open(file, 'r') as f:
        n = int(f.readline())
        fotos_h = []
        fotos_v = []
        i = 0
        for line in f:
            a = line.split('\n')
            s = a[0].split(' ')
            foto = {'ori':s[0], 'id':i, 'tags':s[2:]}
            if s[0] == 'H':
                fotos_h.append(foto)
            else:
                fotos_v.append(foto)
            i += 1
        fotos = {'v':fotos_v, 'h':fotos_h}
    return n, fotos
    
n, fotos = parser('a_example.txt')
print(fotos)