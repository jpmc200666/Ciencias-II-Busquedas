from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QDialogButtonBox, QCheckBox, QMessageBox, QFrame
)
from PySide6.QtCore import Qt


class DialogoPosiciones(QDialog):
    def __init__(self, digitos_totales: int, digitos_necesarios: int, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Seleccionar posiciones")
        self.setMinimumWidth(380)
        self.digitos_necesarios = digitos_necesarios

        # --- Fondo con estilo ---
        self.setStyleSheet("""
            QDialog {
                background-color: #F5F3FF;
                border-radius: 12px;
            }
            QLabel {
                color: #2E1065;
                font-size: 16px;
                font-weight: bold;
                margin-bottom: 8px;
            }
            QCheckBox {
                font-size: 15px;
                color: #4C1D95;
                padding: 6px;
            }
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
                border-radius: 6px;
                border: 2px solid #7C3AED;
                background-color: white;
            }
            QCheckBox::indicator:checked {
                background-color: #7C3AED;
                border: 2px solid #5B21B6;
            }
            QDialogButtonBox QPushButton {
                background-color: #7C3AED;
                color: white;
                font-weight: bold;
                border-radius: 10px;
                padding: 8px 16px;
                font-size: 14px;
            }
            QDialogButtonBox QPushButton:hover {
                background-color: #6D28D9;
            }
            QDialogButtonBox QPushButton:disabled {
                background-color: #C4B5FD;
                color: #F5F3FF;
            }
        """)

        # --- Layout principal ---
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setAlignment(Qt.AlignTop)

        label = QLabel(
            f"Selecciona exactamente {digitos_necesarios} posición(es) "
            f"de la clave de {digitos_totales} dígitos:"
        )
        layout.addWidget(label)

        # --- Marco visual para las opciones ---
        frame = QFrame()
        frame_layout = QVBoxLayout(frame)
        frame_layout.setSpacing(5)
        frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 2px solid #C4B5FD;
                border-radius: 10px;
                padding: 8px;
            }
        """)

        # Checkboxes
        self.checkboxes = []
        for i in range(1, digitos_totales + 1):
            chk = QCheckBox(f"Posición {i}")
            chk.stateChanged.connect(self.actualizar_estado)
            frame_layout.addWidget(chk)
            self.checkboxes.append(chk)

        layout.addWidget(frame)

        # Botones OK / Cancelar
        self.botones = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.btn_ok = self.botones.button(QDialogButtonBox.Ok)
        self.btn_ok.setEnabled(False)
        self.botones.accepted.connect(self.validar_y_aceptar)
        self.botones.rejected.connect(self.reject)
        layout.addWidget(self.botones, alignment=Qt.AlignRight)

        self.setLayout(layout)

    # -------------------------------
    # Lógica de control
    # -------------------------------
    def actualizar_estado(self):
        """Controla la cantidad de checkboxes activas."""
        seleccionadas = [chk for chk in self.checkboxes if chk.isChecked()]

        # Si ya alcanzó el máximo, deshabilita las demás no seleccionadas
        if len(seleccionadas) >= self.digitos_necesarios:
            for chk in self.checkboxes:
                if not chk.isChecked():
                    chk.setEnabled(False)
        else:
            for chk in self.checkboxes:
                chk.setEnabled(True)

        # Solo habilita el botón OK cuando se cumplen las seleccionadas necesarias
        self.btn_ok.setEnabled(len(seleccionadas) == self.digitos_necesarios)

    def validar_y_aceptar(self):
        """Evita cerrar el diálogo hasta que haya la cantidad exacta."""
        seleccionadas = [i + 1 for i, chk in enumerate(self.checkboxes) if chk.isChecked()]
        if len(seleccionadas) != self.digitos_necesarios:
            QMessageBox.warning(
                self,
                "Selección inválida",
                f"Debes seleccionar exactamente {self.digitos_necesarios} posiciones."
            )
        else:
            self.accept()

    def get_posiciones(self, digitos_necesarios: int):
        """Devuelve las posiciones seleccionadas si son válidas."""
        seleccionadas = [i + 1 for i, chk in enumerate(self.checkboxes) if chk.isChecked()]
        if len(seleccionadas) == digitos_necesarios:
            return seleccionadas
        return None
