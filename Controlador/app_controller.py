import sys
from PySide6.QtWidgets import QApplication
from Vista.menu_principal import MainWindow


class AppController:
    def __init__(self):
        # Crear la aplicación
        self.app = QApplication(sys.argv)

        # Crear la ventana principal y pasarle el callback para cambiar páginas
        self.ventana = MainWindow(self.cambiar_pagina)

    def salir(self):
        """Cerrar la aplicación"""
        self.app.quit()

    def cambiar_pagina(self, nombre: str):
        """Cambiar entre las diferentes páginas de la aplicación"""
        self.ventana.cambiar_pagina(nombre)

    def run(self):
        """Ejecutar la aplicación"""
        self.ventana.show()
        sys.exit(self.app.exec())
