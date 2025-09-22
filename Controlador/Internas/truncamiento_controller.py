import os
from Modelo.manejador_archivos import ManejadorArchivos


class TruncamientoController:
    def __init__(self, ruta_archivo="data/truncamiento.json"):
        self.ruta_archivo = ruta_archivo
        self.estructura = {}
        self.capacidad = 0
        self.digitos = 0
        self.posiciones = []  # 👈 posiciones que elige el usuario (1-based)

        os.makedirs(os.path.dirname(self.ruta_archivo), exist_ok=True)

    def crear_estructura(self, capacidad: int, digitos: int, posiciones: list[int]):
        self.capacidad = capacidad
        self.digitos = digitos
        self.posiciones = posiciones
        self.estructura = {i: "" for i in range(1, self.capacidad + 1)}
        self.guardar()

    def _digitos_necesarios(self):
        """Determina cuántos dígitos se requieren según la capacidad."""
        return len(str(self.capacidad - 1))

    def funcion_hash(self, clave: str) -> int:
        """
        Función hash usando truncamiento en posiciones elegidas.
        Ejemplo:
            clave = "2835", posiciones = [2, 3], capacidad = 100
            -> tomamos clave[1] y clave[2] = "83"
            -> int("83") + 1 = 84
        """
        digitos_requeridos = self._digitos_necesarios()

        # Tomar solo las posiciones necesarias
        seleccionados = [clave[p - 1] for p in self.posiciones[:digitos_requeridos]]
        valor = int("".join(seleccionados))

        return valor + 1  # siempre +1 para que sea 1-based

    def agregar_clave(self, clave: str) -> str:
        """
        Inserta una clave en la estructura usando truncamiento.
        Devuelve:
            - "OK" si se insertó
            - "REPETIDA" si ya existe
            - "LLENO" si no hay espacio en esa posición
            - "LONGITUD" si no cumple los dígitos
        """
        # Validar longitud
        if len(clave) != self.digitos:
            return "LONGITUD"

        # Validar repetida
        if str(clave) in map(str, self.estructura.values()):
            return "REPETIDA"

        # Calcular índice hash
        pos = self.funcion_hash(clave)

        # Insertar si está vacío
        if self.estructura.get(pos, "") == "":
            self.estructura[pos] = str(clave)
        else:
            return "LLENO"  # por ahora sin manejo de colisiones

        self.guardar()
        return "OK"

    def guardar(self):
        datos = {
            "capacidad": self.capacidad,
            "digitos": self.digitos,
            "posiciones": self.posiciones,
            "estructura": self.estructura
        }
        ManejadorArchivos.guardar_json(self.ruta_archivo, datos)

    def cargar(self):
        datos = ManejadorArchivos.leer_json(self.ruta_archivo)
        if datos:
            self.capacidad = datos.get("capacidad", 0)
            self.digitos = datos.get("digitos", 0)
            self.posiciones = datos.get("posiciones", [])
            self.estructura = {int(k): v for k, v in datos.get("estructura", {}).items()}
            return True
        return False

    def obtener_datos_vista(self):
        return {
            "capacidad": self.capacidad,
            "digitos": self.digitos,
            "posiciones": self.posiciones,
            "estructura": self.estructura
        }

    def get_claves(self):
        return [v for v in self.estructura.values() if v != ""]
