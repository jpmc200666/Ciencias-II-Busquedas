from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QComboBox, QPushButton
from PySide6.QtCore import Qt


class DialogoColisiones(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Resolución de colisiones")
        self.setFixedSize(400, 200)

        # Layout principal
        layout = QVBoxLayout(self)

        # Etiqueta
        etiqueta = QLabel("Se ha detectado una colisión.\n"
                          "Seleccione el método de resolución:")
        etiqueta.setAlignment(Qt.AlignCenter)
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
        layout.addWidget(self.combo)

        # Botón de aceptar
        btn_aceptar = QPushButton("Aceptar")
        btn_aceptar.clicked.connect(self.accept)
        layout.addWidget(btn_aceptar)

    def get_estrategia(self) -> str:
        """Devuelve la estrategia seleccionada por el usuario."""
        return self.combo.currentText()
