import sys
from PySide6.QtWidgets import QMainWindow, QStackedWidget
from Vista.inicio import Inicio
from Vista.busqueda import Busqueda
from Vista.grafos import Grafos
from Vista.lineal_interna import LinealInterna
from Vista.binaria_interna import BinariaInterna
from Vista.mod_interna import ModInterna   # 👈 importa la clase

class MainWindow(QMainWindow):
    def __init__(self, cambiar_pagina_callback):
        super().__init__()
        self.setWindowTitle("Ciencias de la Computación II")
        self.setGeometry(300, 200, 900, 600)

        self.stacked = QStackedWidget()
        self.setCentralWidget(self.stacked)

        # Páginas
        self.inicio = Inicio(cambiar_pagina_callback)
        self.busqueda = Busqueda(cambiar_pagina_callback)
        self.grafos = Grafos(cambiar_pagina_callback)
        self.lineal_interna = LinealInterna(cambiar_pagina_callback)
        self.binaria_interna = BinariaInterna(cambiar_pagina_callback)
        self.mod_interna = ModInterna(cambiar_pagina_callback)   # 👈 agrega esta

        # Añadir al stack
        self.stacked.addWidget(self.inicio)          # 0
        self.stacked.addWidget(self.busqueda)        # 1
        self.stacked.addWidget(self.grafos)          # 2
        self.stacked.addWidget(self.lineal_interna)  # 3
        self.stacked.addWidget(self.binaria_interna) # 4
        self.stacked.addWidget(self.mod_interna)     # 5  👈 aquí entra mod_interna

        # Página inicial
        self.stacked.setCurrentIndex(0)

    def cambiar_pagina(self, nombre):
        paginas = {
            "inicio": 0,
            "busqueda": 1,
            "grafos": 2,
            "lineal_interna": 3,
            "binaria_interna": 4,
            "mod_interna": 5   # 👈 registra la clave para que Busqueda.abrir_mod() funcione
        }

        if nombre in paginas:
            self.stacked.setCurrentIndex(paginas[nombre])
