from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QDialogButtonBox, QCheckBox

class DialogoPosiciones(QDialog):
    def __init__(self, digitos_totales: int, digitos_necesarios: int, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Seleccionar posiciones")
        self.setMinimumWidth(300)
        self.seleccion = []

        layout = QVBoxLayout(self)

        layout.addWidget(QLabel(
            f"Selecciona {digitos_necesarios} posición(es) "
            f"de la clave de {digitos_totales} dígitos:"
        ))

        # checkboxes para cada posición
        self.checkboxes = []
        for i in range(1, digitos_totales + 1):
            chk = QCheckBox(f"Posición {i}")
            layout.addWidget(chk)
            self.checkboxes.append(chk)

        # botones OK / Cancelar
        botones = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        botones.accepted.connect(self.accept)
        botones.rejected.connect(self.reject)
        layout.addWidget(botones)

    def get_posiciones(self, digitos_necesarios: int):
        """Devuelve las posiciones seleccionadas si son válidas."""
        seleccionadas = [i+1 for i, chk in enumerate(self.checkboxes) if chk.isChecked()]
        if len(seleccionadas) == digitos_necesarios:
            return seleccionadas
        return None
