from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QFrame
from PySide6.QtCore import Qt

class BusquedaResiduos(QWidget):
    def __init__(self, cambiar_pagina_callback):
        super().__init__()
        self.cambiar_pagina_callback = cambiar_pagina_callback

        layout = QVBoxLayout(self)
        layout.setSpacing(20)

        # --- Encabezado ---
        header = QFrame()
        header.setStyleSheet("""
            background: qlineargradient(
                spread:pad, x1:0, y1:0, x2:1, y2:0,
                stop:0 #D8B4FE, stop:1 #A78BFA
            );
            border-radius: 12px;
        """)
        header_layout = QVBoxLayout(header)

        titulo = QLabel("Ciencias de la Computación II - Búsqueda por Residuos")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("font-size: 26px; font-weight: bold; color: white; margin: 10px;")
        header_layout.addWidget(titulo)

        # --- Menú debajo del título ---
        menu_layout = QHBoxLayout()
        menu_layout.setSpacing(40)
        menu_layout.setAlignment(Qt.AlignCenter)

        btn_inicio = QPushButton("Inicio")
        btn_busqueda = QPushButton("Menú de Búsqueda")

        for btn in (btn_inicio, btn_busqueda):
            btn.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    color: #2E1065;
                    font-size: 16px;
                    font-weight: bold;
                    border: none;
                }
                QPushButton:hover {
                    color: #6D28D9;
                    text-decoration: underline;
                }
            """)
            menu_layout.addWidget(btn)

        header_layout.addLayout(menu_layout)

        btn_inicio.clicked.connect(lambda: self.cambiar_pagina_callback("inicio"))
        btn_busqueda.clicked.connect(lambda: self.cambiar_pagina_callback("busqueda"))

        layout.addWidget(header)

        # --- Contenido central ---
        label = QLabel("Página: Búsqueda por Residuos")
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("font-size: 20px; color: #4B5563; margin-top: 30px;")
        layout.addWidget(label)
