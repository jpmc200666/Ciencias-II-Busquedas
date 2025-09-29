import os
from Modelo.manejador_archivos import ManejadorArchivos
from Controlador.ColisionesController import ColisionesController
from Vista.dialogo_colision import DialogoColisiones
from PySide6.QtWidgets import QDialog


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
        self.historial.append(self.estructura.copy())

    def crear_estructura(self, capacidad: int, digitos: int, metodo_hash="mod"):
        self.capacidad = capacidad
        self.digitos = digitos
        self.estructura = {i: "" for i in range(1, capacidad + 1)}
        self.historial.clear()
        self.colisiones_controller = ColisionesController(capacidad, metodo_hash)
        self.guardar()

    def agregar_clave(self, clave: str, parent=None) -> str:
        if len(clave) != self.digitos:
            return "LONGITUD"
        if str(clave) in map(str, self.estructura.values()):
            return "REPETIDA"

        try:
            self._guardar_estado()
            clave_int = int(clave)

            # calcular posición inicial
            pos = self.colisiones_controller.calcular_posicion(clave_int)

            if self.colisiones_controller.estructura[pos] is None:
                # sin colisión → insertar directo
                self.colisiones_controller.estructura[pos] = clave_int
            else:
                # hay colisión → abrir cuadro
                dialogo = DialogoColisiones(parent)
                if dialogo.exec() == QDialog.Accepted:
                    estrategia = dialogo.get_estrategia()
                    pos = self.colisiones_controller.insertar(clave_int, estrategia)
                else:
                    return "CANCELADO"

            # actualizar estructura visible (+1 porque tu diccionario empieza en 1)
            self.estructura[pos + 1] = str(clave)
            self.guardar()
            return "OK"
        except Exception as e:
            return f"ERROR: {e}"

    def adicionar_clave(self, clave: str, estrategia="Lineal") -> str:
        return self.agregar_clave(clave, estrategia)

    def deshacer(self):
        if not self.historial:
            return "VACIO"
        self.estructura = self.historial.pop()
        return "OK"

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

    def eliminar_clave(self, clave: str) -> str:
        """Elimina una clave si existe en la estructura."""
        clave = str(clave)
        if clave not in map(str, self.estructura.values()):
            return "NO_EXISTE"

        # Guardar estado para deshacer
        self._guardar_estado()

        # Eliminar la clave
        for k, v in list(self.estructura.items()):
            if str(v) == clave:
                self.estructura[k] = ""
                break

        self.guardar()
        return "OK"

