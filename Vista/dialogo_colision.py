from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QComboBox, QPushButton
from PySide6.QtCore import Qt


class DialogoColisiones(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Resolución de colisiones")
        self.setFixedSize(450, 250)
        self.setModal(True)

        # Layout principal
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setAlignment(Qt.AlignCenter)

        # Etiqueta
        etiqueta = QLabel("Se ha detectado una colisión.\nSeleccione el método de resolución:")
        etiqueta.setAlignment(Qt.AlignCenter)
        etiqueta.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #4C1D95;
            margin-bottom: 10px;
        """)
        layout.addWidget(etiqueta)

        # ComboBox con las estrategias
        self.combo = QComboBox()
        self.combo.addItems([
            "Lineal",
            "Cuadrática",
            "Doble función hash",
            "Arreglo anidado",
            "Lista encadenada"
        ])
        self.combo.setStyleSheet("""
            QComboBox {
                border: 2px solid #7C3AED;
                border-radius: 10px;
                padding: 10px;
                font-size: 16px;
                background-color: #F3E8FF;
                color: #4C1D95;
                min-height: 40px;
            }
            QComboBox:hover {
                border: 2px solid #6D28D9;
                background-color: #EDE9FE;
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 8px solid #7C3AED;
                margin-right: 10px;
            }
            QComboBox QAbstractItemView {
                border: 2px solid #7C3AED;
                border-radius: 8px;
                background-color: #F3E8FF;
                selection-background-color: #7C3AED;
                selection-color: white;
                padding: 5px;
            }
        """)
        layout.addWidget(self.combo)

        # Botón de aceptar
        btn_aceptar = QPushButton("Aceptar")
        btn_aceptar.setStyleSheet("""
            QPushButton {
                background-color: #7C3AED;
                color: white;
                padding: 10px 30px;
                font-size: 16px;
                border-radius: 10px;
                font-weight: bold;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #6D28D9;
            }
            QPushButton:pressed {
                background-color: #5B21B6;
            }
        """)
        btn_aceptar.clicked.connect(self.accept)
        layout.addWidget(btn_aceptar, alignment=Qt.AlignCenter)

        # Espaciado al final
        layout.addStretch()

    def get_estrategia(self) -> str:
        """Devuelve el texto de la estrategia seleccionada."""
        return self.combo.currentText()
