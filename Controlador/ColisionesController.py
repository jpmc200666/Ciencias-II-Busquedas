class ColisionesController:
    """
    Clase para manejar las colisiones en funciones hash
    Estrategias soportadas:
        - Lineal
        - Cuadrática
        - Doble función hash
        - Arreglo anidado
        - Lista encadenada
    """

    def __init__(self, tamaño, metodo_hash):
        self.tamaño = tamaño
        self.metodo_hash = metodo_hash  # "mod", "cuadrado", "truncamiento", "plegamiento"
        self.estructura = [None] * tamaño  # estructura base

    # -------------------------------
    # Cálculo de posición base
    # -------------------------------
    def calcular_posicion(self, clave):
        if self.metodo_hash == "mod":
            return clave % self.tamaño
        elif self.metodo_hash == "cuadrado":
            return (clave * clave) % self.tamaño
        elif self.metodo_hash == "truncamiento":
            return int(str(clave)[:2]) % self.tamaño
        elif self.metodo_hash == "plegamiento":
            partes = [int(str(clave)[i:i + 2]) for i in range(0, len(str(clave)), 2)]
            return sum(partes) % self.tamaño
        else:
            return clave % self.tamaño

    # -------------------------------
    # Estrategias de sondeo abierto
    # -------------------------------
    def sondeo_lineal(self, pos, intento):
        return (pos + intento) % self.tamaño

    def sondeo_cuadratico(self, pos, intento):
        return (pos + intento ** 2) % self.tamaño

    def doble_hash(self, clave, pos, intento, primo=7):
        h2 = primo - (clave % primo)
        return (pos + intento * h2) % self.tamaño

    # -------------------------------
    # Estrategias de encadenamiento
    # -------------------------------
    def insertar_arreglo_anidado(self, pos, clave):
        if self.estructura[pos] is None:
            self.estructura[pos] = []
        self.estructura[pos].append(clave)

    def insertar_lista_encadenada(self, pos, clave):
        if self.estructura[pos] is None:
            self.estructura[pos] = []
        self.estructura[pos].append(clave)

    # -------------------------------
    # Inserción general
    # -------------------------------
    def insertar(self, clave, estrategia="Lineal"):
        """
        Inserta una clave en la tabla usando la estrategia seleccionada.
        Devuelve (pos, colision) donde:
            - pos = índice en la tabla
            - colision = True si hubo colisión
        """
        pos = self.calcular_posicion(clave)

        # Caso normal: no hay colisión
        if self.estructura[pos] is None:
            self.estructura[pos] = clave
            return pos, False  # False = no hubo colisión

        # Hubo colisión → aplicar estrategia
        if estrategia == "Lineal":
            intento = 1
            nuevo_pos = self.sondeo_lineal(pos, intento)
            while self.estructura[nuevo_pos] is not None:
                intento += 1
                nuevo_pos = self.sondeo_lineal(pos, intento)
            self.estructura[nuevo_pos] = clave
            return nuevo_pos, True

        elif estrategia == "Cuadrática":
            intento = 1
            nuevo_pos = self.sondeo_cuadratico(pos, intento)
            while self.estructura[nuevo_pos] is not None:
                intento += 1
                nuevo_pos = self.sondeo_cuadratico(pos, intento)
            self.estructura[nuevo_pos] = clave
            return nuevo_pos, True

        elif estrategia == "Doble función hash":
            intento = 1
            nuevo_pos = self.doble_hash(clave, pos, intento)
            while self.estructura[nuevo_pos] is not None:
                intento += 1
                nuevo_pos = self.doble_hash(clave, pos, intento)
            self.estructura[nuevo_pos] = clave
            return nuevo_pos, True

        elif estrategia == "Arreglo anidado":
            self.insertar_arreglo_anidado(pos, clave)
            return pos, True

        elif estrategia == "Lista encadenada":
            self.insertar_lista_encadenada(pos, clave)
            return pos, True

        else:
            raise ValueError(f"Estrategia de colisión no soportada: {estrategia}")

