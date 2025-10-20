import os
from Modelo.manejador_archivos import ManejadorArchivos


class TruncamientoController:
    def __init__(self, ruta_archivo="data/truncamiento.json"):
        self.ruta_archivo = ruta_archivo
        self.estructura = {}
        self.capacidad = 0
        self.digitos = 0
        self.posiciones = []  # posiciones elegidas por el usuario (1-based)
        self.historial = []

        os.makedirs(os.path.dirname(self.ruta_archivo), exist_ok=True)

    # -------------------------------
    # ESTADO / HISTORIAL
    # -------------------------------
    def _guardar_estado(self):
        """Guarda una copia del estado actual para poder deshacer."""
        self.historial.append(self.estructura.copy())

    # -------------------------------
    # CREACIÓN / CONFIGURACIÓN
    # -------------------------------
    def crear_estructura(self, capacidad: int, digitos: int, posiciones: list[int]):
        """Crea una nueva estructura vacía de truncamiento."""
        self.capacidad = int(capacidad)
        self.digitos = int(digitos)
        self.posiciones = list(posiciones)
        self.estructura = {i: "" for i in range(1, self.capacidad + 1)}
        self.historial.clear()
        self.guardar()
        return "OK"

    def _digitos_necesarios(self) -> int:
        """Determina cuántos dígitos se necesitan según la capacidad (mínimo 2)."""
        if self.capacidad <= 1:
            return 2
        return max(2, len(str(self.capacidad - 1)))

    # -------------------------------
    # FUNCIÓN HASH (TRUNCAMIENTO)
    # -------------------------------
    def funcion_hash(self, clave: str) -> int:
        """Calcula la posición hash usando truncamiento en las posiciones elegidas."""
        if not self.posiciones:
            raise ValueError("No se han definido posiciones para truncamiento.")
        if not clave.isdigit():
            raise ValueError("La clave debe ser numérica.")
        if len(clave) < max(self.posiciones):
            raise ValueError("Las posiciones elegidas superan la longitud de la clave.")

        seleccionados = [clave[p - 1] for p in self.posiciones[:self._digitos_necesarios()]]
        valor = int("".join(seleccionados))
        return (valor % self.capacidad) + 1 if self.capacidad > 0 else 1

    # -------------------------------
    # INSERCIÓN / ELIMINACIÓN / DESHACER
    # -------------------------------
    def agregar_clave(self, clave: str) -> str:
        """Inserta una clave."""
        if not clave.isdigit():
            return "NO_NUMERICA"
        if len(clave) != self.digitos:
            return "LONGITUD"
        if clave in self.estructura.values():
            return "REPETIDA"

        try:
            pos = self.funcion_hash(clave)
        except Exception as e:
            return f"ERROR: {e}"

        if pos not in self.estructura:
            return "FUERA_RANGO"

        if self.estructura[pos] != "":
            return "LLENO"

        self._guardar_estado()
        self.estructura[pos] = clave
        self.guardar()
        return "OK"

    def eliminar_clave(self, clave: str) -> str:
        """Elimina una clave existente."""
        if not clave.isdigit():
            return "NO_NUMERICA"
        for pos, valor in list(self.estructura.items()):
            if valor == clave:
                self._guardar_estado()
                self.estructura[pos] = ""
                self.guardar()
                return "OK"
        return "NO_EXISTE"

    def deshacer(self) -> str:
        """Revierte al último estado guardado."""
        if not self.historial:
            return "VACIO"
        self.estructura = self.historial.pop()
        self.guardar()
        return "OK"

    # -------------------------------
    # PERSISTENCIA
    # -------------------------------
    def guardar(self):
        datos = {
            "capacidad": self.capacidad,
            "digitos": self.digitos,
            "posiciones": self.posiciones,
            "estructura": self.estructura
        }
        try:
            ManejadorArchivos.guardar_json(self.ruta_archivo, datos)
        except Exception as e:
            print("Error guardando truncamiento:", e)

    def cargar(self) -> bool:
        datos = ManejadorArchivos.leer_json(self.ruta_archivo)
        if not datos:
            return False
        self.capacidad = int(datos.get("capacidad", 0))
        self.digitos = int(datos.get("digitos", 0))
        self.posiciones = list(datos.get("posiciones", []))
        self.estructura = {int(k): v for k, v in datos.get("estructura", {}).items()}
        return True

    # -------------------------------
    # UTILIDADES
    # -------------------------------
    def obtener_datos_vista(self):
        return {
            "capacidad": self.capacidad,
            "digitos": self.digitos,
            "posiciones": self.posiciones,
            "estructura": self.estructura
        }

    def get_claves(self):
        return [v for v in self.estructura.values() if v != ""]
