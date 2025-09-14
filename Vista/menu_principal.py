import sys
from PySide6.QtWidgets import QMainWindow, QStackedWidget
from Vista.inicio import Inicio
from Vista.busqueda import Busqueda
from Vista.grafos import Grafos
from Vista.lineal_interna import LinealInterna


class MainWindow(QMainWindow):
    def __init__(self, cambiar_pagina_callback):
        super().__init__()
        self.setWindowTitle("Ciencias de la Computación II")
        self.setGeometry(300, 200, 900, 600)

        # Contenedor de páginas
        self.stacked = QStackedWidget()
        self.setCentralWidget(self.stacked)

        # Páginas
        self.inicio = Inicio(cambiar_pagina_callback)
        self.busqueda = Busqueda(cambiar_pagina_callback)
        self.grafos = Grafos(cambiar_pagina_callback)
        self.lineal_externa = LinealInterna(cambiar_pagina_callback)

        # Añadir al stack
        self.stacked.addWidget(self.inicio)         # index 0
        self.stacked.addWidget(self.busqueda)       # index 1
        self.stacked.addWidget(self.grafos)         # index 2
        self.stacked.addWidget(self.lineal_externa) # index 3

        # Mostrar la página inicial
        self.stacked.setCurrentIndex(0)

    def cambiar_pagina(self, nombre):
        """Metodo que se puede invocar desde el controlador"""
        paginas = {
            "inicio": 0,
            "busqueda": 1,
            "grafos": 2,
            "lineal_externa": 3
        }
        if nombre in paginas:
            self.stacked.setCurrentIndex(paginas[nombre])
