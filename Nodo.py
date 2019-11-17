class Nodo():
    def __init__(self,clave,padre=None):
        self.parent = padre
        self.clave = clave
        self.g = 0
        self.h = 0
        self.f = 0

    def __lt__(self, other):
        return self.f < other.f

    def __eq__(self, other):
        return self.clave == other.clave

    def __hash__(self):
        return hash( self.clave )