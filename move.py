def get_mov(str):
    pos = int(str.find("0"))+1
    if pos == 1:
        return "rd"
    elif pos == 2:
        return "lrd"
    elif pos == 3:
        return "ld"
    elif pos == 4:
        return "udr"
    elif pos == 5:
        return "lrud"
    elif pos == 6:
        return "udl"
    elif pos == 7:
        return "ru"
    elif pos == 8:
        return "lru"
    elif pos == 9:
        return "lu"

def movement(str,mstr):
    idm = 0
    if mstr  == "u":
        idm = -3
    if mstr  == "d":
        idm = +3
    if mstr == "l":
        idm = -1
    if mstr == "r":
        idm = +1
    
    pos = int(str.find("0"))
    arreglo = list(str)
    arreglo[pos] , arreglo[pos+idm] = arreglo[pos+idm] , arreglo[pos]
    return ''.join(arreglo)

def distancia(str1,str2):
    cont = 0
    for i in range(len(str1)):
        if str1[i] != str2[i]:
            cont +=1 
    return cont


## Tomado de Wikipedia
def distanciaL(str1, str2):
  d=dict()
  for i in range(len(str1)+1):
     d[i]=dict()
     d[i][0]=i
  for i in range(len(str2)+1):
     d[0][i] = i
  for i in range(1, len(str1)+1):
     for j in range(1, len(str2)+1):
        d[i][j] = min(d[i][j-1]+1, d[i-1][j]+1, d[i-1][j-1]+(not str1[i-1] == str2[j-1]))
  return d[len(str1)][len(str2)]