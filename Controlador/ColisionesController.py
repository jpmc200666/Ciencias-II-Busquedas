class ColisionesController:
    def __init__(self, tamaño, metodo_hash):
        self.tamaño = tamaño
        self.metodo_hash = metodo_hash
        self.estructura = [None] * tamaño              # 0..tamaño-1
        self.estructura_anidada = [None] * tamaño     # 0..tamaño-1
        self.estrategia_fija = None
        self.capacidad = tamaño


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

    def insertar_arreglo_anidado(self, pos, clave):
        # pos: ya 0-based
        if self.estructura[pos] is None:
            self.estructura[pos] = clave
        else:
            if self.estructura_anidada[pos] is None:
                self.estructura_anidada[pos] = []
            self.estructura_anidada[pos].append(clave)

    def insertar(self, clave, estrategia="Lineal"):
        if self.estrategia_fija is not None:
            estrategia = self.estrategia_fija

        pos = self.calcular_posicion(clave)  # pos es 0-based

        # fijar estrategia si hay colisión y no estaba fijada
        if self.estructura[pos] is not None and self.estrategia_fija is None:
            self.estrategia_fija = estrategia
            print(f"⚙️ Estrategia de colisión establecida: {estrategia}")

        # Arreglo anidado (misma semántica que lista encadenada en almacenamiento)
        if estrategia == "Arreglo anidado":
            self.insertar_arreglo_anidado(pos, clave)
            tiene_anidado = (self.estructura_anidada[pos] is not None and len(self.estructura_anidada[pos]) > 0)
            return pos, tiene_anidado

        # Si la posición está vacía -> insertar y retornar sin colisión
        if self.estructura[pos] is None:
            self.estructura[pos] = clave
            return pos, False

        # Sondaje lineal
        if estrategia == "Lineal":
            intento = 1
            nuevo_pos = (pos + intento) % self.tamaño
            while self.estructura[nuevo_pos] is not None:
                intento += 1
                nuevo_pos = (pos + intento) % self.tamaño
            self.estructura[nuevo_pos] = clave
            return nuevo_pos, True

        # Sondaje cuadrático
        if estrategia == "Cuadrática":
            intento = 1
            nuevo_pos = (pos + intento ** 2) % self.tamaño
            while self.estructura[nuevo_pos] is not None:
                intento += 1
                nuevo_pos = (pos + intento ** 2) % self.tamaño
            self.estructura[nuevo_pos] = clave
            return nuevo_pos, True

        # Lista encadenada: almacenamos en estructura_anidada[pos]
        if estrategia == "Lista encadenada":
            if self.estructura[pos] is None:
                self.estructura[pos] = clave
                return pos, False
            else:
                if self.estructura_anidada[pos] is None:
                    self.estructura_anidada[pos] = []
                self.estructura_anidada[pos].append(clave)
                return pos, True

        # Doble hash
        if estrategia == "Doble función hash":
            intento = 1
            h2 = 7 - (int(clave) % 7)
            nuevo_pos = (pos + intento * h2) % self.tamaño
            while self.estructura[nuevo_pos] is not None:
                intento += 1
                nuevo_pos = (pos + intento * h2) % self.tamaño
            self.estructura[nuevo_pos] = clave
            return nuevo_pos, True

        raise ValueError(f"Estrategia de colisión no soportada: {estrategia}")


    def insertar_clave_encadenada(self, clave):
        # Obtener posición base
        pos = self.hash_funcion(clave)

        # Si está vacío, se guarda directamente
        if self.estructura[pos] in (None, "", 0):
            self.estructura[pos] = clave

        else:
            # ⚠️ Hay colisión → agregar a la lista encadenada
            if self.estructura_anidada[pos] in (None, [], "", 0):
                self.estructura_anidada[pos] = []

            # Agregar la nueva clave a la lista en esa posición
            self.estructura_anidada[pos].append(clave)

        print(f"[DEBUG] Estructura principal: {self.estructura}")
        print(f"[DEBUG] Estructura encadenada: {self.estructura_anidada}")
