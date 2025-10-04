import os
from Modelo.manejador_archivos import ManejadorArchivos


class CuadradoController:
    def __init__(self, ruta_archivo="data/cuadrado.json"):
        self.ruta_archivo = ruta_archivo
        self.estructura = {}
        self.capacidad = 0
        self.digitos = 0

        os.makedirs(os.path.dirname(self.ruta_archivo), exist_ok=True)

    def crear_estructura(self, capacidad: int, digitos: int):
        self.capacidad = capacidad
        self.digitos = digitos
        self.estructura = {i: "" for i in range(1, capacidad + 1)}
        self.guardar()

    def funcion_hash(self, clave: str) -> int:
        """
        Función hash por el método del cuadrado:
        - Se eleva la clave al cuadrado.
        - Se extraen los dígitos centrales según la regla:
            * Si el cuadrado tiene impar de dígitos → se toma el central + uno a la izquierda.
            * Si tiene par de dígitos → se toman los 2 centrales.
        - Finalmente se suma 1 para obtener la posición (1-based).
        """
        n = int(clave)
        cuadrado = str(n * n)
        longitud = len(cuadrado)

        if longitud % 2 == 1:  # impar
            mid = longitud // 2
            extraidos = cuadrado[mid - 1: mid + 1]  # central + uno a la izquierda
        else:  # par
            mid = longitud // 2
            extraidos = cuadrado[mid - 1: mid + 1]  # dos centrales

        pos = int(extraidos) + 1  # se suma 1 según tu regla

        # 🔹 Ajustar al rango con índices 1..capacidad
        if self.capacidad > 0:
            pos = ((pos - 1) % self.capacidad) + 1

        return pos

    def agregar_clave(self, clave: str) -> str:
        if len(clave) != self.digitos:
            return "LONGITUD"

        if clave in self.estructura.values():
            return "REPETIDA"

        pos = self.funcion_hash(clave)

        if self.estructura[pos] == "":
            self.estructura[pos] = clave
        else:
            return "LLENO"  # no maneja colisiones todavía

        self.guardar()
        return "OK"

    def adicionar_clave(self, clave: str) -> str:
        return self.agregar_clave(clave)

    def guardar(self):
        datos = {
            "capacidad": self.capacidad,
            "digitos": self.digitos,
            "estructura": self.estructura,
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
            "estructura": self.estructura,
        }

    def get_claves(self):
        return [v for v in self.estructura.values() if v != ""]
