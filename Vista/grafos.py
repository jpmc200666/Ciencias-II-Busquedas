from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt

class Grafos(QMainWindow):
    def __init__(self, cambiar_ventana):
        super().__init__()
        self.cambiar_ventana = cambiar_ventana
        self.setWindowTitle("Ciencias de la Computación II - Grafos")
        self.setGeometry(300, 200, 800, 500)

        central = QWidget()
        layout = QVBoxLayout(central)

        titulo = QLabel("Sección de Grafos")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("font-size: 24px; font-weight: bold; color: #2c3e50;")

        boton_inicio = QPushButton("Volver al Inicio")
        boton_inicio.setStyleSheet("font-size: 16px; padding: 8px;")
        boton_inicio.clicked.connect(lambda: self.cambiar_ventana("inicio"))

        layout.addStretch()
        layout.addWidget(titulo)
        layout.addWidget(boton_inicio, alignment=Qt.AlignCenter)
        layout.addStretch()

        self.setCentralWidget(central)
