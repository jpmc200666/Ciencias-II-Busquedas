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

        os.makedirs(os.path.dirname(self.ruta_archivo), exist_ok=True)

    def _guardar_estado(self):
        """Guarda el estado actual en el historial para poder deshacer."""
        self.historial.append(self.estructura.copy())

    def crear_estructura(self, capacidad: int, digitos: int, metodo_hash="mod"):
        """Crea una nueva estructura hash."""
        self.capacidad = capacidad
        self.digitos = digitos
        self.estructura = {i: "" for i in range(1, capacidad + 1)}
        self.historial.clear()
        self.colisiones_controller = ColisionesController(capacidad, metodo_hash)
        self.guardar()

    def adicionar_clave(self, clave: str, estrategia=None) -> str:
        """
        Intenta adicionar una clave a la estructura.
        Retorna:
        - "OK": si se insertó correctamente
        - "LONGITUD": si la clave no tiene la longitud correcta
        - "REPETIDA": si la clave ya existe
        - "COLISION": si hay colisión y no se especificó estrategia
        - "ERROR: ...": si ocurrió un error
        """
        # Validaciones
        if len(clave) != self.digitos:
            return "LONGITUD"

        # Verificar si la clave ya existe
        if clave in [v for v in self.estructura.values() if v]:
            return "REPETIDA"

        try:
            # ⚠️ Usa la conversión solo para calcular la posición hash
            clave_int = int(clave)

            # Guardar estado antes de insertar
            self._guardar_estado()

            # Calcular posición base
            pos_base = self.colisiones_controller.calcular_posicion(clave_int)

            # Verificar si hay colisión
            if self.colisiones_controller.estructura[pos_base] is None:
                # No hay colisión, insertar directamente
                self.colisiones_controller.estructura[pos_base] = clave_int  # versión numérica interna
                self.estructura[pos_base + 1] = clave  # 👈 guarda el texto original con ceros
                self.guardar()
                return "OK"
            else:
                # HAY COLISIÓN
                if estrategia is None:
                    self.historial.pop()
                    return "COLISION"

                # Resolver colisión con estrategia
                pos_final, hubo_colision = self.colisiones_controller.insertar(clave_int, estrategia)
                self._sincronizar_estructura()

                # 🔧 Corrige visualmente para mostrar siempre los ceros originales
                for i in range(1, self.capacidad + 1):
                    valor = self.estructura[i]
                    if str(valor).isdigit():
                        self.estructura[i] = str(valor).zfill(self.digitos)

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
                # Manejar listas (encadenamiento)
                if isinstance(valor, list):
                    self.estructura[i + 1] = ", ".join(map(str, valor))
                else:
                    self.estructura[i + 1] = str(valor)
            else:
                self.estructura[i + 1] = ""

    def deshacer(self):
        """Deshace el último cambio."""
        if not self.historial:
            return "VACIO"
        self.estructura = self.historial.pop()

        # Reconstruir colisiones_controller desde estructura
        if self.colisiones_controller:
            self.colisiones_controller.estructura = [None] * self.capacidad
            for pos, valor in self.estructura.items():
                if valor and valor != "":
                    idx = pos - 1  # ajustar índice
                    try:
                        self.colisiones_controller.estructura[idx] = int(valor)
                    except ValueError:
                        # puede ser lista encadenada con formato "1234, 5678"
                        self.colisiones_controller.estructura[idx] = valor

        self.guardar()
        return "OK"

    def eliminar_clave(self, clave: str) -> str:
        """Elimina una clave si existe en la estructura."""
        clave = str(clave)

        # Buscar la clave
        encontrada = False
        for k, v in list(self.estructura.items()):
            if str(v) == clave:
                encontrada = True
                self._guardar_estado()

                # Eliminar de estructura visible
                self.estructura[k] = ""

                # Eliminar de colisiones_controller
                if self.colisiones_controller:
                    idx = k - 1
                    self.colisiones_controller.estructura[idx] = None

                self.guardar()
                break

        return "OK" if encontrada else "NO_EXISTE"

    def guardar(self):
        """Guarda la estructura en archivo JSON."""
        datos = {
            "capacidad": self.capacidad,
            "digitos": self.digitos,
            "estructura": self.estructura
        }
        ManejadorArchivos.guardar_json(self.ruta_archivo, datos)

    def cargar(self):
        """Carga la estructura desde archivo JSON."""
        datos = ManejadorArchivos.leer_json(self.ruta_archivo)
        if datos:
            self.capacidad = datos.get("capacidad", 0)
            self.digitos = datos.get("digitos", 0)
            self.estructura = {int(k): v for k, v in datos.get("estructura", {}).items()}

            # Reconstruir colisiones_controller
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
            "estructura": self.estructura
        }