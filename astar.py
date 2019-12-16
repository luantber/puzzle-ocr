from move import *
import heapq
from Nodo import Nodo

def astar(puzzle_str):
    return []
    puzzle =  puzzle_str #"104253876" #sol
    # puzzle = "123406785" #no sol
    destino = "123456780"

            #    f,g,h   
    abierto = [ Nodo(puzzle) ]
    abierto_set = set ( abierto )

    cerrado = set()

    actual = puzzle
    while len(abierto) != 0:

        # print("Abiertos",len(abierto))
        # print("Cerrados",len(cerrado))

        actual = heapq.heappop(abierto)
        abierto_set.discard(actual)

        #print(actual.clave,"-.-.-.-")
        cerrado.add( actual )

        if actual.clave == destino:
            # print("Fin")
            respuesta = []

            temp = actual
            while temp.clave!=puzzle:
                #print(temp.clave)
                temp = temp.parent
                respuesta.append(temp.clave)
            respuesta.reverse()
            respuesta.pop(0)            
            return respuesta

        movs = get_mov(actual.clave)

        for m in movs:
            nuevo_nodo = Nodo ( movement(actual.clave,m) , actual)
    #        padres[nuevo_nodo]=actual[3]
            if nuevo_nodo not in cerrado:

                nuevo_nodo.g = actual.g + distancia(actual.clave,nuevo_nodo.clave)
                nuevo_nodo.h = distancia(nuevo_nodo.clave,destino)
                nuevo_nodo.f = nuevo_nodo.g+nuevo_nodo.h
                
                if nuevo_nodo in abierto_set:
                    if all( nuevo_nodo.g > x.g for x in abierto )  :
                        # print("here")
                        continue

                heapq.heappush(abierto, nuevo_nodo )
                abierto_set.add(nuevo_nodo)

    print ( "Ruta no encontrada")
    return []
