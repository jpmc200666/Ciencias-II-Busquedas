from Controlador.Externas.ZonaColisionesController import ZonaColisionesController
import copy, json, math, os

class ModExternaController:
    def __init__(self):
        self.bloques = []
        self.num_claves = 0
        self.tamanio_bloque = 0
        self.historial = []
        self.zona_colisiones = ZonaColisionesController()

    # ==================== CREACIÓN ====================
    def crear_estructura(self, num_claves):
        if num_claves < 1:
            raise ValueError("num_claves debe ser >= 1")

        self.num_claves = int(num_claves)
        b = max(1, int(math.floor(math.sqrt(self.num_claves))))
        num_bloques = int(math.ceil(self.num_claves / b))

        self.tamanio_bloque = b
        self.bloques = [[None for _ in range(b)] for _ in range(num_bloques)]

        self.historial.clear()
        self.zona_colisiones = ZonaColisionesController()
        return {
            "bloques": copy.deepcopy(self.bloques),
            "num_claves": self.num_claves,
            "tamanio_bloque": self.tamanio_bloque
        }

    # ==================== INSERCIÓN ====================
    def insertar_clave(self, clave):
        # 🔹 Validar que la clave sea numérica (solo dígitos)
        if not str(clave).isdigit():
            return False, "La clave debe ser numérica."

        clave_s = str(clave)  # se mantiene con ceros a la izquierda
        k = int(clave_s)      # solo para hash

        # 🔹 Verificar límite total
        total_insertadas = sum(
            1 for bloque in self.bloques for c in bloque if c is not None
        ) + len(self.zona_colisiones.zona)

        if total_insertadas >= self.num_claves:
            return False, f"No se pueden insertar más claves. Límite de {self.num_claves} alcanzado."

        # 🔹 Evitar duplicados
        if self.buscar_clave(clave_s) is not None or clave_s in self.zona_colisiones.zona:
            return False, "La clave ya existe en la estructura."

        num_bloques = len(self.bloques)
        bloque_idx = k % num_bloques
        pos_idx = k % self.tamanio_bloque

        # 🔹 Intento de inserción normal
        for step_b in range(num_bloques):
            b_idx = (bloque_idx + step_b) % num_bloques
            bloque = self.bloques[b_idx]
            for step_p in range(self.tamanio_bloque):
                p_idx = (pos_idx + step_p) % self.tamanio_bloque
                if bloque[p_idx] is None:
                    if step_b == 0 and step_p == 0:
                        self._guardar_historial()
                        bloque[p_idx] = clave_s  # guarda "0000" intacto
                        return True, f"Insertada en bloque {b_idx + 1}, posición {p_idx + 1}."
                    else:
                        return (None, "collision", {
                            "clave": clave_s,
                            "hash_bloque": bloque_idx,
                            "bloque_objetivo": b_idx,
                            "hash_pos": pos_idx,
                            "pos_objetivo": p_idx
                        })

        # 🔹 Si no hay hueco → zona de colisiones
        return (None, "collision", {
            "clave": clave_s,
            "hash_bloque": bloque_idx,
            "bloque_objetivo": None,
            "hash_pos": pos_idx,
            "pos_objetivo": None
        })

    def insertar_en_zona_colisiones(self, clave):
        """Maneja la inserción en la zona de colisiones (controlador dedicado)."""
        ok, msg = self.zona_colisiones.insertar(clave)
        if ok:
            self._guardar_historial()
        return ok, msg

    # ==================== BÚSQUEDA / ELIMINACIÓN ====================
    def buscar_clave(self, clave):
        clave = str(clave)
        for i, bloque in enumerate(self.bloques):
            for j, val in enumerate(bloque):
                if val == clave:
                    return ("estructura", i, j)
        idx = self.zona_colisiones.buscar(clave)
        if idx is not None:
            return ("colision", idx)
        return None

    def eliminar_clave(self, clave):
        clave = str(clave)
        # Buscar en los bloques principales
        for i, bloque in enumerate(self.bloques):
            for j, val in enumerate(bloque):
                if val == clave:
                    self._guardar_historial()
                    bloque[j] = None
                    return True, f"Clave {clave} eliminada del bloque {i + 1}, posición {j + 1}."

        # Buscar en la zona de colisiones
        idx = self.zona_colisiones.buscar(clave)
        if idx is not None:
            ok, msg = self.zona_colisiones.eliminar(clave)
            if ok:
                self._guardar_historial()
            return ok, msg

        return False, f"La clave {clave} no se encontró en la estructura ni en la zona de colisiones."

    # ==================== HISTORIAL / DESHACER ====================
    def _guardar_historial(self):
        self.historial.append({
            "bloques": copy.deepcopy(self.bloques),
            "zona": copy.deepcopy(self.zona_colisiones.zona)
        })

    def deshacer(self):
        if not self.historial:
            return False
        estado = self.historial.pop()
        self.bloques = estado["bloques"]
        self.zona_colisiones.zona = estado["zona"]
        return True

    # ==================== GUARDAR / CARGAR / ELIMINAR ====================
    def guardar_estructura(self, ruta):
        """Guarda toda la estructura (bloques + zona de colisiones) en un archivo JSON."""
        datos = {
            "num_claves": self.num_claves,
            "tamanio_bloque": self.tamanio_bloque,
            "bloques": self.bloques,
            "zona_colisiones": self.zona_colisiones.zona
        }
        try:
            with open(ruta, "w", encoding="utf-8") as f:
                json.dump(datos, f, indent=4, ensure_ascii=False)
            return True, f"Estructura guardada correctamente en {ruta}."
        except Exception as e:
            return False, f"Error al guardar la estructura: {e}"

    def cargar_estructura(self, ruta):
        """Carga la estructura completa desde un archivo JSON, incluyendo zona de colisiones."""
        if not os.path.exists(ruta):
            return False, f"No se encontró el archivo: {ruta}"

        try:
            with open(ruta, "r", encoding="utf-8") as f:
                datos = json.load(f)

            self.num_claves = datos.get("num_claves", 0)
            self.tamanio_bloque = datos.get("tamanio_bloque", 0)
            self.bloques = datos.get("bloques", [])
            self.zona_colisiones = ZonaColisionesController()
            self.zona_colisiones.zona = datos.get("zona_colisiones", [])
            self.historial.clear()

            return True, "Estructura cargada correctamente."
        except Exception as e:
            return False, f"Error al cargar la estructura: {e}"

    def eliminar_estructura(self):
        """Borra la estructura completa (bloques, zona y registros)."""
        self.bloques = []
        self.zona_colisiones = ZonaColisionesController()
        self.num_claves = 0
        self.tamanio_bloque = 0
        self.historial.clear()
        return True, "Estructura eliminada correctamente."
