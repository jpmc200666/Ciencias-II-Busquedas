from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIntValidator


class DialogoClave(QDialog):
    def __init__(self, longitud, titulo="Clave", modo="insertar", parent=None, mensaje=""):
        super().__init__(parent)
        self.longitud = longitud
        self.modo = modo
        self.mensaje = mensaje

        self.setWindowTitle(str(titulo))
        self.setFixedSize(420, 230)
        self.setModal(True)

        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setAlignment(Qt.AlignCenter)

        # --- Modo insertar/buscar/eliminar ---
        if modo in ("insertar", "buscar", "eliminar"):
            textos = {
                "insertar": f"Ingrese una clave de {longitud} dígitos:",
                "buscar": f"Ingrese la clave de {longitud} dígitos a buscar:",
                "eliminar": f"Ingrese la clave de {longitud} dígitos a eliminar:"
            }
            lbl = QLabel(textos[modo])
            lbl.setAlignment(Qt.AlignCenter)
            lbl.setStyleSheet("font-size: 18px; font-weight: bold; color: #4C1D95;")
            layout.addWidget(lbl)

            self.input = QLineEdit()
            self.input.setMaxLength(longitud)
            self.input.setAlignment(Qt.AlignCenter)
            self.input.setPlaceholderText("Ej: " + "0" * longitud)
            self.input.setValidator(QIntValidator(0, 10**longitud - 1, self))
            self.input.setStyleSheet("""
                QLineEdit {
                    border: 2px solid #7C3AED;
                    border-radius: 10px;
                    padding: 10px;
                    font-size: 18px;
                    background-color: #F3E8FF;
                    color: #4C1D95;
                }
                QLineEdit:focus {
                    border: 2px solid #6D28D9;
                    background-color: #EDE9FE;
                }
            """)
            layout.addWidget(self.input)

            btn_layout = QHBoxLayout()
            btn_ok = QPushButton("Aceptar")
            btn_cancel = QPushButton("Cancelar")

            for b, color in [(btn_ok, "#7C3AED"), (btn_cancel, "#A78BFA")]:
                b.setStyleSheet(f"""
                    QPushButton {{
                        background-color: {color};
                        color: white;
                        padding: 8px 20px;
                        font-size: 16px;
                        border-radius: 10px;
                    }}
                    QPushButton:hover {{ background-color: #6D28D9; }}
                """)

            btn_ok.clicked.connect(self.validar_y_aceptar)
            btn_cancel.clicked.connect(self.reject)

            btn_layout.addStretch()
            btn_layout.addWidget(btn_ok)
            btn_layout.addWidget(btn_cancel)
            btn_layout.addStretch()
            layout.addLayout(btn_layout)

        # --- Modo mensaje simple ---
        elif modo == "mensaje":
            lbl = QLabel(mensaje)
            lbl.setAlignment(Qt.AlignCenter)
            lbl.setWordWrap(True)
            lbl.setStyleSheet("font-size: 16px; color: #4C1D95;")
            layout.addWidget(lbl)

            btn_ok = QPushButton("Aceptar")
            btn_ok.setStyleSheet("""
                QPushButton {
                    background-color: #7C3AED;
                    color: white;
                    padding: 8px 22px;
                    font-size: 16px;
                    border-radius: 10px;
                }
                QPushButton:hover { background-color: #6D28D9; }
            """)
            btn_ok.clicked.connect(self.accept)
            layout.addWidget(btn_ok, alignment=Qt.AlignCenter)
            self.input = None

        # --- Modo confirmar ---
        elif modo == "confirmar":
            lbl = QLabel(mensaje)
            lbl.setAlignment(Qt.AlignCenter)
            lbl.setWordWrap(True)
            lbl.setStyleSheet("font-size: 16px; color: #4C1D95;")
            layout.addWidget(lbl)

            botones = QHBoxLayout()
            btn_si = QPushButton("Sí")
            btn_no = QPushButton("No")

            for b, color in [(btn_si, "#7C3AED"), (btn_no, "#A78BFA")]:
                b.setStyleSheet(f"""
                    QPushButton {{
                        background-color: {color};
                        color: white;
                        padding: 8px 18px;
                        font-size: 16px;
                        border-radius: 10px;
                    }}
                    QPushButton:hover {{ background-color: #6D28D9; }}
                """)

            btn_si.clicked.connect(self.accept)
            btn_no.clicked.connect(self.reject)
            botones.addStretch()
            botones.addWidget(btn_si)
            botones.addWidget(btn_no)
            botones.addStretch()
            layout.addLayout(botones)

            self.input = None

        else:
            lbl = QLabel("Modo no reconocido.")
            lbl.setAlignment(Qt.AlignCenter)
            layout.addWidget(lbl)
            self.input = None

    # --- Métodos auxiliares ---
    def validar_y_aceptar(self):
        if self.input:
            texto = self.input.text().strip()
            if len(texto) != self.longitud:
                QMessageBox.warning(self, "Error", f"La clave debe tener {self.longitud} dígitos.")
                return
            if not texto.isdigit():
                QMessageBox.warning(self, "Error", "La clave debe ser numérica.")
                return
        self.accept()

    def get_clave(self):
        return self.input.text().strip() if self.input else None

    def clave(self):
        return self.get_clave()
