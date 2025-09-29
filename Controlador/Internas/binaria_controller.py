import json
import os

class BinariaController:
    def __init__(self):
        self.capacidad = 0
        self.digitos = 0
        self.estructura = {}
        self.historial = []  # pila de estados previos

    def _guardar_estado(self):
        """Guarda el estado actual en el historial (para deshacer)."""
        copia = self.estructura.copy()
        self.historial.append(copia)

    def crear_estructura(self, capacidad, digitos):
        """Inicializa estructura vacía."""
        self.capacidad = capacidad
        self.digitos = digitos
        self.estructura = {}
        self.historial.clear()
        return True

    def adicionar_clave(self, clave: str):
        if len(clave) != self.digitos:
            return "LONGITUD"
        if clave in self.estructura.values():
            return "REPETIDA"
        if len(self.estructura) >= self.capacidad:
            return "LLENO"

        # Guardamos estado antes de modificar
        self._guardar_estado()

        lista = list(self.estructura.values())
        lista.append(clave)
        lista.sort()
        self.estructura = {i: lista[i] for i in range(len(lista))}
        return "OK"

    def eliminar_clave(self, clave: str):
        lista = list(self.estructura.values())
        if clave in lista:
            self._guardar_estado()
            lista.remove(clave)
            self.estructura = {i: lista[i] for i in range(len(lista))}
            return "OK"
        return "NO_EXISTE"

    def deshacer(self):
        """Revierte al último estado guardado."""
        if not self.historial:
            return "VACIO"
        self.estructura = self.historial.pop()
        return "OK"

    def buscar(self, clave: str):
        """Búsqueda binaria en lista ordenada."""
        lista = list(self.estructura.values())
        low, high = 0, len(lista) - 1
        while low <= high:
            mid = (low + high) // 2
            if lista[mid] == clave:
                return mid
            elif lista[mid] < clave:
                low = mid + 1
            else:
                high = mid - 1
        return -1

    def obtener_datos_vista(self):
        return {
            "capacidad": self.capacidad,
            "estructura": self.estructura,
            "digitos": self.digitos
        }

    def eliminar_estructura(self):
        """Borra toda la estructura y resetea el controlador."""
        self.capacidad = 0
        self.digitos = 0
        self.estructura = {}
        self.historial.clear()
        return True

    def guardar(self, ruta: str):
        try:
            datos = {
                "capacidad": self.capacidad,
                "digitos": self.digitos,
                "estructura": self.estructura
            }
            with open(ruta, "w", encoding="utf-8") as f:
                json.dump(datos, f, indent=4, ensure_ascii=False)
            return "OK"
        except Exception as e:
            return str(e)

    def cargar(self, ruta: str):
        if not os.path.exists(ruta):
            return "NO_ARCHIVO"
        try:
            with open(ruta, "r", encoding="utf-8") as f:
                datos = json.load(f)

            self.capacidad = datos.get("capacidad", 0)
            self.digitos = datos.get("digitos", 0)
            self.estructura = datos.get("estructura", {})
            self.historial.clear()
            return "OK"
        except Exception as e:
            return str(e)