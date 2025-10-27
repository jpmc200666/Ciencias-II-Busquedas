# Controlador/Externas/ZonaColisionesController.py
import copy
import json
import os

class ZonaColisionesController:
    def __init__(self):
        self.zona = []
        self.historial = []  # 🔹 se inicializa el historial

    # ---------------------------
    # Inserción con historial
    # ---------------------------
    def insertar(self, clave):
        if clave in self.zona:
            return False, f"La clave {clave} ya está en la zona de colisiones."
        self._guardar_estado()
        self.zona.append(clave)
        return True, f"Clave {clave} insertada en la zona de colisiones."

    # ---------------------------
    # Búsqueda
    # ---------------------------
    def buscar(self, clave):
        try:
            return self.zona.index(clave)
        except ValueError:
            return None

    # ---------------------------
    # Eliminación con historial
    # ---------------------------
    def eliminar(self, clave):
        if clave not in self.zona:
            return False, f"La clave {clave} no se encuentra en la zona de colisiones."
        self._guardar_estado()
        self.zona.remove(clave)
        return True, f"Clave {clave} eliminada de la zona de colisiones."

    # ---------------------------
    # Deshacer última acción
    # ---------------------------
    def deshacer(self):
        if self.historial:
            self.zona = self.historial.pop()
            return True
        return False

    # ---------------------------
    # Guardar estado actual a archivo JSON
    # ---------------------------
    def guardar(self, ruta):
        datos = {'zona': self.zona}
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(datos, f, ensure_ascii=False, indent=4)

    # ---------------------------
    # Cargar estado desde archivo JSON
    # ---------------------------
    def cargar(self, ruta):
        if not os.path.exists(ruta):
            self.zona = []
            self.historial.clear()
            return False, "Archivo no encontrado. Se inicializó zona vacía."
        with open(ruta, "r", encoding="utf-8") as f:
            datos = json.load(f)
        self.zona = datos.get('zona', [])
        self.historial.clear()
        return True, "Zona de colisiones cargada correctamente."

    # ---------------------------
    # Interno: guarda una copia del estado actual
    # ---------------------------
    def _guardar_estado(self):
        self.historial.append(copy.deepcopy(self.zona))
