import os
from Modelo.manejador_archivos import ManejadorArchivos
from Controlador.ColisionesController import ColisionesController


class ModController:
    def __init__(self, ruta_archivo="data/mod.json"):
        self.ruta_archivo = ruta_archivo
        self.estructura = {}
        self.capacidad = 0
        self.digitos = 0
        self.historial = []
        self.colisiones_controller = None
        self.estructura_anidada = []
        self.ultima_estrategia = None

        os.makedirs(os.path.dirname(self.ruta_archivo), exist_ok=True)

    def _guardar_estado(self):
        """Guarda el estado actual en el historial para poder deshacer."""
        self.historial.append({
            "estructura": self.estructura.copy(),
            "estructura_anidada": [lst.copy() if lst else [] for lst in self.estructura_anidada]
        })

    def crear_estructura(self, capacidad: int, digitos: int, metodo_hash="mod"):
        """Crea una nueva estructura hash."""
        self.capacidad = capacidad
        self.digitos = digitos
        self.estructura = {i: "" for i in range(1, capacidad + 1)}
        self.historial.clear()
        self.colisiones_controller = ColisionesController(capacidad, metodo_hash)

        # Inicializar estructura_anidada como lista de listas vacías
        self.estructura_anidada = [[] for _ in range(capacidad)]

        # Sincronizar con el controlador
        self.colisiones_controller.estructura_anidada = [[] for _ in range(capacidad)]

        self.guardar()

    def adicionar_clave(self, clave: str, estrategia=None) -> str:
        if len(clave) != self.digitos:
            return "LONGITUD"

        if clave in [v for v in self.estructura.values() if v]:
            return "REPETIDA"

        try:
            clave_int = int(clave)
            self._guardar_estado()

            pos_base = self.colisiones_controller.calcular_posicion(clave_int)

            # Si la posición primaria está vacía
            if self.colisiones_controller.estructura[pos_base] is None:
                self.colisiones_controller.estructura[pos_base] = clave_int
                self.estructura[pos_base + 1] = str(clave).zfill(self.digitos)
                self.guardar()
                return "OK"

            # Hay colisión
            if estrategia is None:
                self.historial.pop()
                return "COLISION"

            # Registrar estrategia
            self.ultima_estrategia = estrategia

            # --- Lista encadenada ---
            if estrategia == "Lista encadenada":
                pos_final, hubo_colision = self.colisiones_controller.insertar(clave_int, estrategia)

                # 🔹 SINCRONIZAR estructura_anidada desde el controlador
                raw = self.colisiones_controller.estructura_anidada
                self.estructura_anidada = [lst.copy() if lst else [] for lst in raw]

                # Actualizar estructura principal (mantener formato)
                for i in range(1, self.capacidad + 1):
                    val = self.estructura.get(i, "")
                    if val and str(val).isdigit():
                        self.estructura[i] = str(val).zfill(self.digitos)

                print(f"[DEBUG] Después de insertar '{clave}' en pos {pos_base}:")
                print(f"  estructura[{pos_base + 1}] = {self.estructura.get(pos_base + 1)}")
                print(f"  estructura_anidada[{pos_base}] = {self.estructura_anidada[pos_base]}")

                self.guardar()
                return "OK"

            # --- Arreglo anidado ---
            if estrategia == "Arreglo anidado":
                pos_final, hubo_colision = self.colisiones_controller.insertar(clave_int, estrategia)

                # Sincronizar estructura_anidada
                raw = self.colisiones_controller.estructura_anidada
                self.estructura_anidada = [lst.copy() if lst else [] for lst in raw]

                # Formatear estructura principal
                for i in range(1, self.capacidad + 1):
                    val = self.estructura.get(i, "")
                    if val and str(val).isdigit():
                        self.estructura[i] = str(val).zfill(self.digitos)

                self.guardar()
                return "OK"

            # --- Otras estrategias (lineal/cuadrática/doble) ---
            pos_final, hubo_colision = self.colisiones_controller.insertar(clave_int, estrategia)
            self._sincronizar_estructura()
            self.guardar()
            return "OK"

        except ValueError:
            return "ERROR: La clave debe ser numérica"
        except Exception as e:
            return f"ERROR: {e}"

    def _sincronizar_estructura(self):
        """Sincroniza self.estructura con colisiones_controller.estructura"""
        for i in range(self.capacidad):
            valor = self.colisiones_controller.estructura[i]
            if valor is not None:
                if isinstance(valor, list):
                    self.estructura[i + 1] = ", ".join(map(str, valor))
                else:
                    self.estructura[i + 1] = str(valor).zfill(self.digitos)
            else:
                self.estructura[i + 1] = ""

    def deshacer(self):
        """Deshace el último cambio (restaura estructura principal y anidada)."""
        if not self.historial:
            return "VACIO"

        estado_anterior = self.historial.pop()

        # Restaurar estructura principal
        self.estructura = estado_anterior["estructura"].copy()

        # Restaurar estructura anidada
        self.estructura_anidada = [
            lst.copy() if lst else []
            for lst in estado_anterior["estructura_anidada"]
        ]

        # Sincronizar con el controlador de colisiones
        if self.colisiones_controller:
            # Limpiar estructura del controlador
            self.colisiones_controller.estructura = [None] * self.capacidad
            self.colisiones_controller.estructura_anidada = [
                lst.copy() if lst else []
                for lst in self.estructura_anidada
            ]

            # Reconstruir estructura principal del controlador
            for pos, valor in self.estructura.items():
                if valor and valor != "":
                    idx = pos - 1
                    try:
                        self.colisiones_controller.estructura[idx] = int(valor)
                    except ValueError:
                        self.colisiones_controller.estructura[idx] = valor

        # Guardar estado restaurado
        self.guardar()

        # Retornar dict con el estado completo para la vista
        return {
            "estructura": self.estructura,
            "estructura_anidada": self.estructura_anidada,
            "capacidad": self.capacidad,
            "digitos": self.digitos
        }

    def eliminar_clave(self, clave: str) -> str:
        """Elimina una clave si existe en la estructura."""
        clave = str(clave)
        encontrada = False

        # Eliminar de la estructura principal
        for k, v in list(self.estructura.items()):
            if str(v) == clave:
                encontrada = True
                self._guardar_estado()
                self.estructura[k] = ""

                if self.colisiones_controller:
                    idx = k - 1
                    self.colisiones_controller.estructura[idx] = None
                break

        # Eliminar de cada sublista anidada
        for i, sub in enumerate(self.estructura_anidada):
            if sub and clave in [str(x) for x in sub]:
                encontrada = True
                sub.remove(int(clave))
                # Sincronizar con el controlador
                if self.colisiones_controller:
                    self.colisiones_controller.estructura_anidada[i] = sub.copy()

        self.guardar()
        return "OK" if encontrada else "NO_EXISTE"

    def guardar(self):
        """Guarda la estructura en archivo JSON."""
        datos = {
            "capacidad": self.capacidad,
            "digitos": self.digitos,
            "estructura": self.estructura,
            "estructura_anidada": self.estructura_anidada,
            "ultima_estrategia": self.ultima_estrategia
        }
        ManejadorArchivos.guardar_json(self.ruta_archivo, datos)

    def cargar(self):
        """Carga la estructura desde archivo JSON."""
        datos = ManejadorArchivos.leer_json(self.ruta_archivo)
        if datos:
            self.capacidad = datos.get("capacidad", 0)
            self.digitos = datos.get("digitos", 0)
            self.estructura = {int(k): v for k, v in datos.get("estructura", {}).items()}
            self.estructura_anidada = datos.get("estructura_anidada", [])
            self.ultima_estrategia = datos.get("ultima_estrategia", None)

            # Crear nuevo controlador de colisiones
            self.colisiones_controller = ColisionesController(self.capacidad, "mod")

            # Copiar estructura anidada al controlador
            self.colisiones_controller.estructura_anidada = [lst.copy() if lst else [] for lst in
                                                             self.estructura_anidada]

            # Reconstruir el arreglo principal
            for pos, valor in self.estructura.items():
                if valor and valor != "":
                    idx = pos - 1
                    try:
                        self.colisiones_controller.estructura[idx] = int(valor)
                    except ValueError:
                        self.colisiones_controller.estructura[idx] = valor

            return True
        return False

    def obtener_datos_vista(self):
        """Retorna los datos para la vista."""
        return {
            "capacidad": self.capacidad,
            "digitos": self.digitos,
            "estructura": self.estructura,
            "estructura_anidada": self.estructura_anidada
        }