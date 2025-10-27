class BinariaController:
    def __init__(self):
        self.bloques = []              # Lista de listas (bloques)
        self.num_claves = 0            # Total de claves
        self.tamanio_bloque = 0        # Cantidad máxima de claves por bloque
        self.historial = []            # Para deshacer acciones

    # ================== CREAR ESTRUCTURA ==================
    def crear_estructura(self, num_claves):
        """Crea la estructura con bloques vacíos según el número total de claves."""
        # Tamaño de bloque: máximo 4 claves por bloque (ajustable)
        self.tamanio_bloque = 4
        num_bloques = (num_claves + self.tamanio_bloque - 1) // self.tamanio_bloque

        # Crear bloques vacíos
        self.bloques = [[] for _ in range(num_bloques)]
        self.num_claves = num_claves

        return {
            "exito": True,
            "mensaje": f"Estructura creada con {num_bloques} bloques de tamaño {self.tamanio_bloque}.",
            "bloques": self.bloques,
            "num_claves": self.num_claves,
            "tamanio_bloque": self.tamanio_bloque
        }

    # ================== INSERTAR CLAVE ==================
    def insertar_clave(self, clave):
        """Inserta una clave en orden ascendente dentro de los bloques sin borrar la estructura base."""
        # Guardar estado anterior
        self.historial.append([list(b) for b in self.bloques])

        # Verificar duplicado
        for bloque in self.bloques:
            if clave in bloque:
                return {"exito": False, "mensaje": f"La clave {clave} ya existe."}

        # Obtener todas las claves actuales
        claves_totales = [c for bloque in self.bloques for c in bloque if c != ""]
        claves_totales.append(clave)
        claves_totales.sort(key=lambda x: int(x))  # orden numérico pero conserva ceros

        # Rellenar los bloques existentes sin crear nuevos
        nuevas_bloques = []
        for i in range(len(self.bloques)):
            inicio = i * self.tamanio_bloque
            fin = inicio + self.tamanio_bloque
            bloque = claves_totales[inicio:fin]
            # Rellenar con vacíos si faltan claves
            while len(bloque) < self.tamanio_bloque:
                bloque.append("")
            nuevas_bloques.append(bloque)

        # Si quedan claves que no caben, crear nuevos bloques
        while len(claves_totales) > len(nuevas_bloques) * self.tamanio_bloque:
            inicio = len(nuevas_bloques) * self.tamanio_bloque
            fin = inicio + self.tamanio_bloque
            bloque_extra = claves_totales[inicio:fin]
            while len(bloque_extra) < self.tamanio_bloque:
                bloque_extra.append("")
            nuevas_bloques.append(bloque_extra)

        self.bloques = nuevas_bloques

        return {"exito": True, "mensaje": f"Clave {clave} insertada correctamente."}

    # ================== ELIMINAR CLAVE ==================
    def eliminar_clave(self, clave):
        """Elimina una clave y reacomoda los bloques para no dejar huecos."""
        # Guardar estado anterior para deshacer
        self.historial.append([list(b) for b in self.bloques])

        for bloque in self.bloques:
            if clave in bloque:
                bloque.remove(clave)
                break
        else:
            return {"exito": False, "mensaje": f"La clave {clave} no existe."}

        # Reacomodar claves para eliminar huecos (compactar)
        claves_totales = [c for bloque in self.bloques for c in bloque]
        self.bloques = []
        for i in range(0, len(claves_totales), self.tamanio_bloque):
            self.bloques.append(claves_totales[i:i + self.tamanio_bloque])

        return {"exito": True, "mensaje": f"Clave {clave} eliminada y bloques reacomodados."}

    # ================== BUSCAR CLAVE ==================
    def buscar_clave(self, clave):
        """Busca una clave y devuelve su posición (bloque e índice)."""
        for i, bloque in enumerate(self.bloques):
            if clave in bloque:
                pos = bloque.index(clave)
                return {
                    "exito": True,
                    "mensaje": f"Clave {clave} encontrada en bloque {i + 1}, posición {pos + 1}."
                }
        return {"exito": False, "mensaje": f"La clave {clave} no se encuentra en la estructura."}

    # ================== OBTENER BLOQUES ==================
    def obtener_bloques(self):
        return self.bloques

    # ================== DESHACER ==================
    def deshacer(self):
        """Deshace el último cambio si hay historial."""
        if not self.historial:
            return {"exito": False, "mensaje": "No hay acciones para deshacer."}

        self.bloques = self.historial.pop()
        return {"exito": True, "mensaje": "Última acción deshecha correctamente."}
