class Lineal:

    def __init__(self, rango, digitos_clave):
        self.__rango = rango
        self.__digitos_clave = digitos_clave

    @property
    def rango(self):
        return self.__rango

    @property
    def digitos_clave(self):
        return self.__digitos_clave

    @rango.setter
    def rango(self, value):
        self.__rango = value

    @digitos_clave.setter
    def digitos_clave(self, value):
        self.__digitos_clave = value