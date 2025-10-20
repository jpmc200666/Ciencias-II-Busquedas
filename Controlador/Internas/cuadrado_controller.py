import os
from Modelo.manejador_archivos import ManejadorArchivos


class CuadradoController:
    def __init__(self, ruta_archivo="data/cuadrado.json"):
        self.ruta_archivo = ruta_archivo
        self.estructura = {}
        self.arreglo_anidado = []  # Para arreglos anidados
        self.lista_encadenada = []  # Para listas encadenadas
        self.capacidad = 0
        self.digitos = 0
        self.historial = []

        os.makedirs(os.path.dirname(self.ruta_archivo), exist_ok=True)

    # -------------------------------
    # UTILIDADES
    # -------------------------------
    def _guardar_estado(self):
        """Guarda el estado actual en el historial para poder deshacer."""
        self.historial.append({
            'estructura': self.estructura.copy(),
            'arreglo_anidado': [sublista.copy() if isinstance(sublista, list) else [] for sublista in
                                self.arreglo_anidado],
            'lista_encadenada': [sublista.copy() if isinstance(sublista, list) else [] for sublista in
                                 self.lista_encadenada]
        })

    # -------------------------------
    # CREACIÓN
    # -------------------------------
    def crear_estructura(self, capacidad: int, digitos: int):
        """Crea una nueva estructura hash con el método del cuadrado medio."""
        self.capacidad = capacidad
        self.digitos = digitos
        self.estructura = {i: "" for i in range(1, capacidad + 1)}
        self.arreglo_anidado = [[] for _ in range(capacidad)]
        self.lista_encadenada = [[] for _ in range(capacidad)]
        self.historial.clear()
        self.guardar()

    # -------------------------------
    # FUNCIÓN HASH
    # -------------------------------
    def funcion_hash(self, clave: int) -> int:
        """
        Función hash por el método del cuadrado medio:
        1. Se eleva la clave al cuadrado.
        2. Se extraen los dígitos centrales.
        3. Se ajusta al rango [1, capacidad].
        """
        cuadrado = str(clave * clave)
        longitud = len(cuadrado)

        # Extraer los dígitos centrales
        if longitud % 2 == 1:  # impar
            mid = longitud // 2
            extraidos = cuadrado[mid - 1: mid + 1]
        else:  # par
            mid = longitud // 2
            extraidos = cuadrado[mid - 1: mid + 1]

        if not extraidos:
            extraidos = "0"

        pos = int(extraidos)
        pos = ((pos - 1) % self.capacidad) + 1  # ajustar al rango 1..capacidad
        return pos

    # -------------------------------
    # ESTRATEGIAS DE COLISIÓN
    # -------------------------------
    def _colision_lineal(self, pos_inicial: int) -> int:
        """Sondeo lineal: busca la siguiente posición disponible."""
        for i in range(1, self.capacidad + 1):
            nueva_pos = ((pos_inicial - 1 + i) % self.capacidad) + 1
            if self.estructura[nueva_pos] == "":
                return nueva_pos
        return None

    def _colision_cuadratica(self, pos_inicial: int) -> int:
        """Sondeo cuadrático: busca con incrementos cuadráticos."""
        for i in range(1, self.capacidad + 1):
            nueva_pos = ((pos_inicial - 1 + i ** 2) % self.capacidad) + 1
            if self.estructura[nueva_pos] == "":
                return nueva_pos
        return None

    def _colision_doble_hash(self, clave: int) -> int:
        """Doble función hash."""
        pos = self.funcion_hash(clave)
        h2 = 7 - (clave % 7)  # Segunda función hash
        for i in range(1, self.capacidad + 1):
            nueva_pos = ((pos - 1 + i * h2) % self.capacidad) + 1
            if self.estructura[nueva_pos] == "":
                return nueva_pos
        return None

    # -------------------------------
    # ADICIÓN DE CLAVES
    # -------------------------------
    def adicionar_clave(self, clave: str, estrategia: str = None) -> str:
        """
        Inserta una clave usando la función hash del cuadrado medio.
        Si hay colisión y se proporciona una estrategia, aplica esa resolución.
        """
        if len(clave) != self.digitos:
            return "LONGITUD"

        # Verificar si existe en estructura principal
        if clave in self.estructura.values():
            return "REPETIDA"

        # Verificar si existe en arreglo anidado
        for sublista in self.arreglo_anidado:
            if sublista and clave in sublista:
                return "REPETIDA"

        # Verificar si existe en lista encadenada
        for sublista in self.lista_encadenada:
            if sublista and clave in sublista:
                return "REPETIDA"

        # VALIDACIÓN: Contar total de claves insertadas
        total_claves = sum(1 for v in self.estructura.values() if v != "")
        for sublista in self.arreglo_anidado:
            if sublista:
                total_claves += len(sublista)
        for sublista in self.lista_encadenada:
            if sublista:
                total_claves += len(sublista)

        if total_claves >= self.capacidad:
            return "LLENO"

        try:
            clave_int = int(clave)
            pos = self.funcion_hash(clave_int)

            if self.estructura[pos] == "":
                self._guardar_estado()
                self.estructura[pos] = clave
                self.guardar()
                return "OK"
            else:
                # --- Si no se envió estrategia, avisar colisión ---
                if not estrategia:
                    return "COLISION"

                # --- Si se envió estrategia, aplicarla ---
                self._guardar_estado()

                # Normalizar estrategia a minúsculas
                estrategia_lower = estrategia.lower()

                if estrategia_lower in ["lineal", "sondeo lineal"]:
                    nueva_pos = self._colision_lineal(pos)
                    if nueva_pos:
                        self.estructura[nueva_pos] = clave
                        self.guardar()
                        return "OK"
                    else:
                        self.historial.pop()
                        return "LLENO"

                elif estrategia_lower in ["cuadrática", "sondeo cuadrático"]:
                    nueva_pos = self._colision_cuadratica(pos)
                    if nueva_pos:
                        self.estructura[nueva_pos] = clave
                        self.guardar()
                        return "OK"
                    else:
                        self.historial.pop()
                        return "LLENO"

                elif estrategia_lower in ["doble función hash", "doble hash"]:
                    nueva_pos = self._colision_doble_hash(clave_int)
                    if nueva_pos:
                        self.estructura[nueva_pos] = clave
                        self.guardar()
                        return "OK"
                    else:
                        self.historial.pop()
                        return "LLENO"

                elif estrategia_lower == "arreglo anidado":
                    # Usar arreglo_anidado específicamente
                    idx = pos - 1
                    if self.arreglo_anidado[idx] is None:
                        self.arreglo_anidado[idx] = []
                    self.arreglo_anidado[idx].append(clave)
                    self.guardar()
                    return "OK"

                elif estrategia_lower == "lista encadenada":
                    # Usar lista_encadenada específicamente
                    idx = pos - 1
                    if self.lista_encadenada[idx] is None:
                        self.lista_encadenada[idx] = []
                    self.lista_encadenada[idx].append(clave)
                    self.guardar()
                    return "OK"
                else:
                    self.historial.pop()
                    return f"ERROR: Estrategia desconocida '{estrategia}'"

        except ValueError:
            return "ERROR: La clave debe ser numérica"
        except Exception as e:
            return f"ERROR: {e}"

    # -------------------------------
    # ELIMINAR CLAVE
    # -------------------------------
    def eliminar_clave(self, clave: str) -> str:
        """Elimina una clave si existe en la estructura principal o anidada."""
        clave = str(clave)

        # Buscar en estructura principal
        for k, v in list(self.estructura.items()):
            if v == clave:
                self._guardar_estado()
                self.estructura[k] = ""
                self.guardar()
                return "OK"

        # Buscar en arreglo anidado
        for idx, sublista in enumerate(self.arreglo_anidado):
            if sublista and isinstance(sublista, list) and clave in sublista:
                self._guardar_estado()
                self.arreglo_anidado[idx].remove(clave)
                self.guardar()
                return "OK"

        # Buscar en lista encadenada
        for idx, sublista in enumerate(self.lista_encadenada):
            if sublista and isinstance(sublista, list) and clave in sublista:
                self._guardar_estado()
                self.lista_encadenada[idx].remove(clave)
                self.guardar()
                return "OK"

        return "NO_EXISTE"

    # -------------------------------
    # DESHACER
    # -------------------------------
    def deshacer(self):
        """Deshace el último cambio."""
        if not self.historial:
            return "VACIO"
        estado_anterior = self.historial.pop()
        self.estructura = estado_anterior['estructura']
        self.arreglo_anidado = estado_anterior['arreglo_anidado']
        self.lista_encadenada = estado_anterior['lista_encadenada']
        self.guardar()
        return "OK"

    # -------------------------------
    # GUARDAR / CARGAR
    # -------------------------------
    def guardar(self):
        """Guarda la estructura en un archivo JSON."""
        datos = {
            "capacidad": self.capacidad,
            "digitos": self.digitos,
            "estructura": self.estructura,
            "arreglo_anidado": self.arreglo_anidado,
            "lista_encadenada": self.lista_encadenada,
        }
        ManejadorArchivos.guardar_json(self.ruta_archivo, datos)

    def cargar(self):
        """Carga la estructura desde archivo JSON."""
        datos = ManejadorArchivos.leer_json(self.ruta_archivo)
        if datos:
            self.capacidad = datos.get("capacidad", 0)
            self.digitos = datos.get("digitos", 0)
            self.estructura = {int(k): v for k, v in datos.get("estructura", {}).items()}

            # Cargar arreglo anidado
            self.arreglo_anidado = datos.get("arreglo_anidado", [])
            if not isinstance(self.arreglo_anidado, list):
                self.arreglo_anidado = []
            while len(self.arreglo_anidado) < self.capacidad:
                self.arreglo_anidado.append([])

            # Cargar lista encadenada
            self.lista_encadenada = datos.get("lista_encadenada", [])
            if not isinstance(self.lista_encadenada, list):
                self.lista_encadenada = []
            while len(self.lista_encadenada) < self.capacidad:
                self.lista_encadenada.append([])

            return True
        return False

    # -------------------------------
    # OBTENER DATOS
    # -------------------------------
    def obtener_datos_vista(self):
        """Retorna los datos que la vista necesita mostrar."""
        return {
            "capacidad": self.capacidad,
            "digitos": self.digitos,
            "estructura": self.estructura,
        }

    def get_claves(self):
        """Devuelve las claves no vacías."""
        claves = [v for v in self.estructura.values() if v != ""]
        # Agregar claves de arreglo anidado
        for sublista in self.arreglo_anidado:
            if sublista:
                claves.extend(sublista)
        # Agregar claves de lista encadenada
        for sublista in self.lista_encadenada:
            if sublista:
                claves.extend(sublista)
        return claves