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
        self.estructura_anidada = []  # estructura independiente para arreglo anidado
        self.ultima_estrategia = None

        os.makedirs(os.path.dirname(self.ruta_archivo), exist_ok=True)

    def _guardar_estado(self):
        """Guarda el estado actual en el historial para poder deshacer."""
        self.historial.append(self.estructura.copy())

    def crear_estructura(self, capacidad: int, digitos: int, metodo_hash="mod"):
        """Crea una nueva estructura hash."""
        self.capacidad = capacidad
        self.digitos = digitos
        # estructura indexada desde 1 .. capacidad (más intuitivo para la vista)
        self.estructura = {i: "" for i in range(1, capacidad + 1)}
        self.historial.clear()
        # crear controlador de colisiones (usa índices 0..capacidad-1 internamente)
        self.colisiones_controller = ColisionesController(capacidad, metodo_hash)

        # normalizar estructura_anidada a lista de listas (no None)
        raw_anidada = getattr(self.colisiones_controller, "estructura_anidada", None)
        if raw_anidada is None:
            self.estructura_anidada = [[] for _ in range(capacidad)]
        else:
            # convertir posibles None a listas vacías
            self.estructura_anidada = [lst if lst else [] for lst in raw_anidada]

        self.guardar()

    def adicionar_clave(self, clave: str, estrategia=None) -> str:
        if len(clave) != self.digitos:
            return "LONGITUD"

        if clave in [v for v in self.estructura.values() if v]:
            return "REPETIDA"

        try:
            clave_int = int(clave)
            self._guardar_estado()

            # calcular posición 0-based con el colisiones_controller
            pos_base = self.colisiones_controller.calcular_posicion(clave_int)

            # si la posición primaria está vacía -> insertar en principal
            if self.colisiones_controller.estructura[pos_base] is None:
                self.colisiones_controller.estructura[pos_base] = clave_int
                self.estructura[pos_base + 1] = str(clave).zfill(self.digitos)
                self.guardar()
                return "OK"

            # hay colisión
            if estrategia is None:
                self.historial.pop()
                return "COLISION"

            # registrar estrategia
            self.ultima_estrategia = estrategia

            # --- Arreglo anidado: usar el controlador de colisiones para insertar ---
            if estrategia == "Arreglo anidado":
                # delegar en ColisionesController (que debe crear/añadir en estructura_anidada[pos_base])
                pos_final, hubo_colision = self.colisiones_controller.insertar(clave_int, estrategia)

                # sincronizar estructura_anidada desde el controlador (convertir None->[])
                raw = getattr(self.colisiones_controller, "estructura_anidada", [])
                self.estructura_anidada = [lst if lst else [] for lst in raw]

                # (no removemos ni cambiamos la estructura principal; sólo se añade en anidados)
                # formatear visualmente la estructura principal (ceros a la izquierda)
                for i in range(1, self.capacidad + 1):
                    val = self.estructura.get(i, "")
                    if val and str(val).isdigit():
                        self.estructura[i] = str(val).zfill(self.digitos)

                self.guardar()
                return "OK"

            # --- Otras estrategias (lineal/cuadrática/doble): delegar y sincronizar ---
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
        """Deshace el último cambio."""
        if not self.historial:
            return "VACIO"
        self.estructura = self.historial.pop()

        if self.colisiones_controller:
            self.colisiones_controller.estructura = [None] * self.capacidad
            for pos, valor in self.estructura.items():
                if valor and valor != "":
                    idx = pos - 1
                    try:
                        self.colisiones_controller.estructura[idx] = int(valor)
                    except ValueError:
                        self.colisiones_controller.estructura[idx] = valor
        self.guardar()
        return "OK"

    def eliminar_clave(self, clave: str) -> str:
        """Elimina una clave si existe en la estructura."""
        clave = str(clave)
        encontrada = False

        for k, v in list(self.estructura.items()):
            if str(v) == clave:
                encontrada = True
                self._guardar_estado()
                self.estructura[k] = ""

                if self.colisiones_controller:
                    idx = k - 1
                    self.colisiones_controller.estructura[idx] = None

                # También eliminar de estructura anidada si existe
                self.estructura_anidada = [
                    sub for sub in self.estructura_anidada if clave not in sub
                ]

                self.guardar()
                break

        return "OK" if encontrada else "NO_EXISTE"

    def guardar(self):
        """Guarda la estructura en archivo JSON."""
        datos = {
            "capacidad": self.capacidad,
            "digitos": self.digitos,
            "estructura": self.estructura,
            "estructura_anidada": self.estructura_anidada
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
            self.colisiones_controller = ColisionesController(self.capacidad, "mod")

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
