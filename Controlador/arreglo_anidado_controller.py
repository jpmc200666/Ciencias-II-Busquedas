from PySide6.QtWidgets import QLabel, QWidget, QHBoxLayout
from PySide6.QtCore import Qt

class ArregloAnidadoController:
    def __init__(self, controller):
        self.controller = controller

    def obtener_datos(self):
        estructura = self.controller.estructura
        anidados = self.controller.arreglo_anidado or []  # CAMBIO AQUÍ
        if len(anidados) != self.controller.capacidad:
            anidados = (anidados + [[]] * self.controller.capacidad)[:self.controller.capacidad]
        max_colisiones = max((len(sub) for sub in anidados), default=0)
        return estructura, anidados, max_colisiones
