from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout
from PySide6.QtCore import Qt
from PySide6.QtGui import QIntValidator


class DialogoClave(QDialog):
    def __init__(self, longitud, titulo="Clave", modo="insertar", parent=None, mensaje=""):
        """
        :param longitud: cantidad de dígitos de la clave
        :param titulo: título de la ventana
        :param modo: "insertar", "buscar", "mensaje" o "confirmar"
        :param mensaje: texto a mostrar si el modo es 'mensaje' o 'confirmar'
        """
        super().__init__(parent)

        self.setWindowTitle(titulo)
        self.setFixedSize(420, 220)
        self.setModal(True)

        layout = QVBoxLayout(self)
        layout.setSpacing(12)

        # --- Modo insertar / buscar: label + QLineEdit + botones ---
        if modo in ("insertar", "buscar", "eliminar"):
            if modo == "insertar":
                texto = f"Ingrese una clave de {longitud} dígitos:"
            elif modo == "buscar":
                texto = f"Ingrese la clave de {longitud} dígitos a buscar:"
            elif modo == "eliminar":
                texto = f"Ingrese la clave de {longitud} dígitos a eliminar:"

            lbl = QLabel(texto)
            lbl.setAlignment(Qt.AlignCenter)
            lbl.setStyleSheet("font-size: 18px; font-weight: bold; color: #4C1D95;")
            layout.addWidget(lbl)

            # Input (estética morada)
            self.input = QLineEdit()
            self.input.setMaxLength(longitud)
            self.input.setAlignment(Qt.AlignCenter)
            self.input.setPlaceholderText("Ej: " + "0" * longitud)
            # Validador numérico (acepta ceros a la izquierda si el usuario los escribe)
            try:
                max_val = 10 ** longitud - 1
                self.input.setValidator(QIntValidator(0, max_val, self))
            except Exception:
                pass
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
                }
            """)
            layout.addWidget(self.input)

            # Botones (estética morada)
            btn_layout = QHBoxLayout()
            btn_ok = QPushButton("Aceptar")
            btn_cancel = QPushButton("Cancelar")

            btn_ok.setStyleSheet("""
                QPushButton {
                    background-color: #7C3AED;
                    color: white;
                    padding: 8px 18px;
                    font-size: 16px;
                    border-radius: 10px;
                }
                QPushButton:hover {
                    background-color: #6D28D9;
                }
            """)
            btn_cancel.setStyleSheet("""
                QPushButton {
                    background-color: #A78BFA;
                    color: white;
                    padding: 8px 18px;
                    font-size: 16px;
                    border-radius: 10px;
                }
                QPushButton:hover {
                    background-color: #9F7AEA;
                }
            """)

            btn_ok.clicked.connect(self.accept)
            btn_cancel.clicked.connect(self.reject)

            btn_layout.addStretch()
            btn_layout.addWidget(btn_ok)
            btn_layout.addWidget(btn_cancel)
            btn_layout.addStretch()
            layout.addLayout(btn_layout)

        # --- Modo mensaje: solo mostrar texto + OK ---
        elif modo == "mensaje":
            lbl = QLabel(mensaje)
            lbl.setAlignment(Qt.AlignCenter)
            lbl.setWordWrap(True)
            lbl.setStyleSheet("font-size: 16px; font-weight: bold; color: #4C1D95;")
            layout.addWidget(lbl)

            btn_ok = QPushButton("Aceptar")
            btn_ok.setStyleSheet("""
                QPushButton {
                    background-color: #7C3AED;
                    color: white;
                    padding: 8px 20px;
                    font-size: 16px;
                    border-radius: 10px;
                }
                QPushButton:hover {
                    background-color: #6D28D9;
                }
            """)
            btn_ok.clicked.connect(self.accept)
            layout.addWidget(btn_ok, alignment=Qt.AlignCenter)

            # no hay input en modo mensaje
            self.input = None

        # --- Modo confirmar: texto + botones Sí / No ---
        elif modo == "confirmar":
            lbl = QLabel(mensaje)
            lbl.setAlignment(Qt.AlignCenter)
            lbl.setWordWrap(True)
            lbl.setStyleSheet("font-size: 16px; color: #4C1D95;")
            layout.addWidget(lbl)

            botones = QHBoxLayout()
            btn_si = QPushButton("Sí")
            btn_no = QPushButton("No")

            btn_si.setStyleSheet("""
                QPushButton {
                    background-color: #7C3AED;
                    color: white;
                    padding: 8px 18px;
                    font-size: 16px;
                    border-radius: 10px;
                }
                QPushButton:hover {
                    background-color: #6D28D9;
                }
            """)
            btn_no.setStyleSheet("""
                QPushButton {
                    background-color: #A78BFA;
                    color: white;
                    padding: 8px 18px;
                    font-size: 16px;
                    border-radius: 10px;
                }
                QPushButton:hover {
                    background-color: #9F7AEA;
                }
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
            # modo desconocido -> solo mensaje de fallback
            lbl = QLabel(mensaje or "")
            lbl.setAlignment(Qt.AlignCenter)
            layout.addWidget(lbl)
            self.input = None

    def clave(self):
        """Compatibilidad antigua: devuelve la clave ingresada (si aplica)."""
        return self.get_clave()

    def get_clave(self):
        """Devuelve la clave ingresada, o None si no corresponde."""
        return self.input.text() if self.input is not None else None
