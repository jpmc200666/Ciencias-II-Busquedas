import os
from Modelo.manejador_archivos import ManejadorArchivos


class ModController:
    def __init__(self, ruta_archivo="data/mod.json"):
        self.ruta_archivo = ruta_archivo
        self.estructura = {}   # Diccionario {posicion: clave}
        self.capacidad = 0
        self.digitos = 0

        os.makedirs(os.path.dirname(self.ruta_archivo), exist_ok=True)

    def crear_estructura(self, digitos: int):
        self.digitos = digitos
        self.capacidad = 10 ** digitos
        self.estructura = {i: "" for i in range(1, self.capacidad + 1)}
        self.guardar()

    def funcion_hash(self, clave: str) -> int:
        """
        Función hash usando el método módulo.
        Devuelve la posición calculada (1-based).
        """
        return (int(clave) % self.capacidad) + 1  # ✅ +1 porque empieza desde 1

    def agregar_clave(self, clave: str) -> str:
        """
        Inserta una clave en la estructura usando la función hash mod.
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
        if self.estructura[pos] == "":
            self.estructura[pos] = str(clave)
        else:
            return "LLENO"  # (por ahora sin manejo de colisiones)

        self.guardar()
        return "OK"

    def adicionar_clave(self, clave: str) -> str:
        """Alias para compatibilidad con la vista."""
        return self.agregar_clave(clave)

    def guardar(self):
        datos = {
            "capacidad": self.capacidad,
            "digitos": self.digitos,
            "estructura": self.estructura
        }
        ManejadorArchivos.guardar_json(self.ruta_archivo, datos)

    def cargar(self):
        datos = ManejadorArchivos.leer_json(self.ruta_archivo)
        if datos:
            self.capacidad = datos.get("capacidad", 0)
            self.digitos = datos.get("digitos", 0)
            self.estructura = {int(k): v for k, v in datos.get("estructura", {}).items()}
            return True
        return False

    def obtener_datos_vista(self):
        return {
            "capacidad": self.capacidad,
            "digitos": self.digitos,
            "estructura": self.estructura
        }

    def get_claves(self):
        return [v for v in self.estructura.values() if v != ""]
