from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QSpinBox, QComboBox, QGridLayout, QLineEdit, QMessageBox, QScrollArea
)
from PySide6.QtCore import Qt
import math


class Cubetas(QMainWindow):
    def __init__(self, cambiar_ventana):
        super().__init__()
        self.cambiar_ventana = cambiar_ventana
        self.setWindowTitle("Cubetas")
        self.setGeometry(300, 200, 900, 600)

        # Datos / contadores de expansión
        self.cubetas_data = []
        self.n_inicial = 0
        self.n = 0
        self.registros = 0
        self.tam_clave = 0
        self.tipo_exp = "Parcial"
        self.expansiones = 0        # total de expansiones (parciales + totales) usadas para cálculo de totales previos
        self.partial_steps = 0      # cuenta exclusivas de expansiones parciales aplicadas

        # --- Scroll principal ---
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        central = QWidget()
        scroll.setWidget(central)
        self.setCentralWidget(scroll)

        self.main_layout = QVBoxLayout(central)
        self.main_layout.setAlignment(Qt.AlignTop)

        # --- Header ---
        header = QFrame()
        header.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #C084FC, stop:1 #7C3AED);
            padding: 20px;
        """)
        titulo = QLabel("🪣 Cubetas (Hash con expansión dinámica)")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("font-size: 26px; font-weight: bold; color: white;")
        header_layout = QVBoxLayout(header)
        header_layout.addWidget(titulo)
        self.main_layout.addWidget(header)

        # --- Controles principales ---
        form_layout = QHBoxLayout()

        lbl_cubetas = QLabel("N° de cubetas:")
        self.spin_cubetas = QSpinBox(); self.spin_cubetas.setRange(1, 50); self.spin_cubetas.setValue(2)

        lbl_registros = QLabel("Registros por cubeta:")
        self.spin_registros = QSpinBox(); self.spin_registros.setRange(1, 10); self.spin_registros.setValue(2)

        lbl_tam_clave = QLabel("Tamaño de clave:")
        self.spin_tam_clave = QSpinBox(); self.spin_tam_clave.setRange(1, 10); self.spin_tam_clave.setValue(4)

        lbl_exp = QLabel("Expansión:")
        self.combo_exp = QComboBox(); self.combo_exp.addItems(["Parcial", "Total"])

        btn_crear = QPushButton("⚙ Crear estructura")
        btn_crear.clicked.connect(self.crear_estructura)

        for w in [lbl_cubetas, self.spin_cubetas, lbl_registros, self.spin_registros,
                  lbl_tam_clave, self.spin_tam_clave, lbl_exp, self.combo_exp, btn_crear]:
            form_layout.addWidget(w)

        self.main_layout.addLayout(form_layout)

        # --- Sección insertar clave ---
        insertar_layout = QHBoxLayout()
        self.input_clave = QLineEdit()
        self.input_clave.setPlaceholderText("Ingrese clave...")
        self.btn_insertar = QPushButton("➕ Insertar clave")
        self.btn_insertar.clicked.connect(self.insertar_clave)
        insertar_layout.addWidget(self.input_clave)
        insertar_layout.addWidget(self.btn_insertar)
        self.main_layout.addLayout(insertar_layout)

        # --- Cuadrícula ---
        self.grid_frame = QFrame()
        self.grid_layout = QGridLayout(self.grid_frame)
        self.grid_layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        self.main_layout.addWidget(self.grid_frame)

        # --- Botones navegación (inicio y búsqueda) ---
        nav_layout = QHBoxLayout()
        btn_inicio = QPushButton("🏠 Volver al inicio"); btn_inicio.clicked.connect(lambda: self.cambiar_ventana("inicio"))
        btn_busqueda = QPushButton("🔍 Volver a búsqueda"); btn_busqueda.clicked.connect(lambda: self.cambiar_ventana("busqueda"))
        for b in (btn_inicio, btn_busqueda):
            b.setStyleSheet("""
                QPushButton {
                    background-color: #DDD6FE; border-radius: 10px; padding: 10px 20px;
                    font-weight: bold; color: #4C1D95;
                }
                QPushButton:hover { background-color: #C4B5FD; }
            """)
            nav_layout.addWidget(b)
        self.main_layout.addLayout(nav_layout)

    # ------------------------
    # Crear estructura inicial
    # ------------------------
    def crear_estructura(self):
        self.n = self.spin_cubetas.value()
        self.n_inicial = self.n
        self.registros = self.spin_registros.value()
        self.tam_clave = self.spin_tam_clave.value()
        self.tipo_exp = self.combo_exp.currentText()
        self.expansiones = 0
        self.partial_steps = 0

        self.cubetas_data = [["" for _ in range(self.registros)] for _ in range(self.n)]
        self.dibujar_cuadricula()

    # ------------------------
    # Dibujar estructura visual
    # ------------------------
    def dibujar_cuadricula(self):
        for i in reversed(range(self.grid_layout.count())):
            w = self.grid_layout.itemAt(i).widget()
            if w:
                w.setParent(None)

        for i, cubeta in enumerate(self.cubetas_data):
            lbl = QLabel(f"Cubeta {i+1}")
            lbl.setAlignment(Qt.AlignCenter)
            lbl.setStyleSheet("font-weight: bold; color: #4C1D95;")
            self.grid_layout.addWidget(lbl, i, 0)
            for j, valor in enumerate(cubeta):
                campo = QLineEdit()
                campo.setText(valor)
                campo.setReadOnly(True)
                campo.setFixedWidth(100)
                campo.setStyleSheet("background-color: #EDE9FE; border-radius: 6px; padding: 3px;")
                self.grid_layout.addWidget(campo, i, j + 1)

    # ------------------------
    # Insertar clave
    # ------------------------
    def insertar_clave(self):
        clave = self.input_clave.text().strip()
        if not clave:
            QMessageBox.warning(self, "Error", "Ingrese una clave válida.")
            return

        # validar numérico y tamaño exacto
        if not clave.isdigit():
            QMessageBox.warning(self, "Error", "La clave debe ser numérica.")
            return
        if len(clave) != self.tam_clave:
            QMessageBox.warning(self, "Error", f"La clave debe tener exactamente {self.tam_clave} dígitos.")
            return

        # Buscar primera posición libre e insertar primero
        insertado = False
        for cubeta in self.cubetas_data:
            for idx in range(len(cubeta)):
                if cubeta[idx] == "":
                    cubeta[idx] = clave
                    insertado = True
                    break
            if insertado:
                break

        if not insertado:
            QMessageBox.warning(self, "Estructura llena", "No hay espacio disponible.")
            return

        # Limpiar entrada y redibujar estructura actual
        self.input_clave.clear()
        self.dibujar_cuadricula()

        # 🔹 Ahora que ya se insertó la clave, verificar si se debe expandir
        self.verificar_expansion(pre_insert=False)

    # ------------------------
    # Verificar expansión
    # ------------------------
    def verificar_expansion(self, pre_insert=False):
        ocupados = sum(1 for cub in self.cubetas_data for r in cub if r != "")
        total = self.n * self.registros
        ocupacion = (ocupados / total) * 100 if total > 0 else 0.0
        if pre_insert:
            ocupacion = ((ocupados + 1) / total) * 100 if total > 0 else 0.0

        # --- Expansión parcial dinámica (con incrementos 1,1,2,2,4,4...) ---
        if self.tipo_exp == "Parcial" and ocupacion >= 75:
            # calcular add = ceil((n_inicial/2) * 2^{floor(partial_steps/2)})
            base = self.n_inicial / 2.0
            factor = 2 ** (self.partial_steps // 2)
            add = math.ceil(base * factor)
            if add < 1:
                add = 1

            nuevo_n = self.n + add

            # Si por alguna razón nuevo_n no aumenta, forzamos mínimo +1
            if nuevo_n <= self.n:
                nuevo_n = self.n + 1

            # Comprobación para no reexpandir si ya hay suficientes cubetas
            if nuevo_n > len(self.cubetas_data):
                # añadir las nuevas cubetas vacías
                for _ in range(nuevo_n - len(self.cubetas_data)):
                    self.cubetas_data.append(["" for _ in range(self.registros)])
                self.n = nuevo_n
                self.partial_steps += 1
                self.expansiones += 1

                QMessageBox.information(
                    self, "Expansión parcial",
                    f"Ocupación: {ocupacion:.1f}%\n"
                    f"Expandiendo parcialmente a {nuevo_n} cubetas."
                )
                self.dibujar_cuadricula()

            # después de aplicar parcial, si la cantidad resultante es un múltiplo entero del inicial
            # (ej. 2×, 3×, ...) y queremos considerar eso como 'total', no es necesario hacer nada extra
            # porque la secuencia ya se comporta como pediste (2,3,4,6,8,12,...)

        # --- Expansión total (usuario eligió "Total") ---
        elif self.tipo_exp == "Total" and ocupacion >= 75:
            # duplicar respecto a la n actual (o respecto a n_inicial según tu política)
            nuevo_n = self.n * 2
            if nuevo_n <= len(self.cubetas_data):
                return
            for _ in range(len(self.cubetas_data), nuevo_n):
                self.cubetas_data.append(["" for _ in range(self.registros)])
            self.n = nuevo_n
            self.expansiones += 1

            QMessageBox.information(
                self, "Expansión total",
                f"Ocupación: {ocupacion:.1f}%\n"
                f"Expandiendo totalmente a {nuevo_n} cubetas."
            )
            self.dibujar_cuadricula()
