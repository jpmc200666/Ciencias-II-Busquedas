class ColisionesController:
    """
    Clase para manejar colisiones en funciones hash.
    Estrategias soportadas:
        - Lineal
        - Cuadrática
        - Doble función hash
        - Arreglo anidado
        - Lista encadenada
    """

    def __init__(self, tamaño, metodo_hash):
        self.tamaño = tamaño
        self.metodo_hash = metodo_hash
        self.estructura = [None] * tamaño          # arreglo principal
        self.estructura_anidada = [None] * tamaño  # arreglos anidados (solo si hay colisiones)

    # -------------------------------
    # Cálculo de posición base
    # -------------------------------
    def calcular_posicion(self, clave):
        clave_int = int(clave)
        if self.metodo_hash == "mod":
            return clave_int % self.tamaño
        elif self.metodo_hash == "cuadrado":
            return (clave_int ** 2) % self.tamaño
        elif self.metodo_hash == "truncamiento":
            return int(str(clave_int)[:2]) % self.tamaño
        elif self.metodo_hash == "plegamiento":
            partes = [int(str(clave_int)[i:i + 2]) for i in range(0, len(str(clave_int)), 2)]
            return sum(partes) % self.tamaño
        else:
            return clave_int % self.tamaño

    # -------------------------------
    # Estrategias de encadenamiento
    # -------------------------------
    def insertar_arreglo_anidado(self, pos, clave):
        """ Inserta una clave en arreglo anidado sin reemplazar la original. """
        if self.estructura[pos] is None:
            # Si la posición está vacía, va en el arreglo principal
            self.estructura[pos] = clave
        else:
            # Colisión: crear o agregar en estructura anidada
            if self.estructura_anidada[pos] is None:
                self.estructura_anidada[pos] = []
            self.estructura_anidada[pos].append(clave)

    # -------------------------------
    # Inserción general
    # -------------------------------
    def insertar(self, clave, estrategia="Lineal"):
        pos = self.calcular_posicion(clave)

        # Estrategia especial: arreglo anidado
        if estrategia == "Arreglo anidado":
            self.insertar_arreglo_anidado(pos, clave)
            return pos, (self.estructura_anidada[pos] is not None)

        # --- Estrategias normales ---
        if self.estructura[pos] is None:
            self.estructura[pos] = clave
            return pos, False

        if estrategia == "Lineal":
            intento = 1
            nuevo_pos = (pos + intento) % self.tamaño
            while self.estructura[nuevo_pos] is not None:
                intento += 1
                nuevo_pos = (pos + intento) % self.tamaño
            self.estructura[nuevo_pos] = clave
            return nuevo_pos, True

        elif estrategia == "Cuadrática":
            intento = 1
            nuevo_pos = (pos + intento ** 2) % self.tamaño
            while self.estructura[nuevo_pos] is not None:
                intento += 1
                nuevo_pos = (pos + intento ** 2) % self.tamaño
            self.estructura[nuevo_pos] = clave
            return nuevo_pos, True

        elif estrategia == "Doble función hash":
            intento = 1
            h2 = 7 - (int(clave) % 7)
            nuevo_pos = (pos + intento * h2) % self.tamaño
            while self.estructura[nuevo_pos] is not None:
                intento += 1
                nuevo_pos = (pos + intento * h2) % self.tamaño
            self.estructura[nuevo_pos] = clave
            return nuevo_pos, True

        else:
            raise ValueError(f"Estrategia de colisión no soportada: {estrategia}")
