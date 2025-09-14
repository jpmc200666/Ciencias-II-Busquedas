from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QHBoxLayout
)
from PySide6.QtCore import Qt


class DialogoClave(QDialog):
    def __init__(self, longitud, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Adicionar clave")
        self.setFixedSize(400, 200)

        # --- Layout principal ---
        layout = QVBoxLayout(self)
        layout.setSpacing(15)

        # --- Texto de instrucción ---
        lbl = QLabel(f"Ingrese una clave de {longitud} dígitos:")
        lbl.setAlignment(Qt.AlignCenter)
        lbl.setStyleSheet("font-size: 18px; font-weight: bold; color: #4C1D95;")
        layout.addWidget(lbl)

        # --- Campo de texto ---
        self.input = QLineEdit()
        self.input.setPlaceholderText("Ej: " + "0" * longitud)
        self.input.setMaxLength(longitud)
        self.input.setAlignment(Qt.AlignCenter)
        self.input.setStyleSheet("""
            QLineEdit {
                border: 2px solid #7C3AED;
                border-radius: 10px;
                padding: 8px;
                font-size: 18px;
                background-color: #F3E8FF;
                color: #4C1D95;
            }
        """)
        layout.addWidget(self.input)

        # --- Botones ---
        botones = QHBoxLayout()
        self.btn_ok = QPushButton("Aceptar")
        self.btn_cancel = QPushButton("Cancelar")

        for btn, color in [(self.btn_ok, "#7C3AED"), (self.btn_cancel, "#A78BFA")]:
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {color};
                    color: white;
                    padding: 8px 16px;
                    font-size: 16px;
                    border-radius: 8px;
                }}
                QPushButton:hover {{
                    background-color: #6D28D9;
                }}
            """)
            botones.addWidget(btn)

        layout.addLayout(botones)

        # Conexiones
        self.btn_ok.clicked.connect(self.accept)
        self.btn_cancel.clicked.connect(self.reject)

    def get_clave(self):
        return self.input.text()
