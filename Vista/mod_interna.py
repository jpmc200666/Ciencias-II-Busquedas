from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel, QFrame,
    QComboBox, QSpinBox, QPushButton, QGridLayout, QScrollArea,
    QMessageBox, QHBoxLayout, QDialog,
)
from PySide6.QtCore import Qt
from .dialogo_clave import DialogoClave
from Controlador.Internas.mod_controller import ModController


class ModInterna(QMainWindow):
    def __init__(self, cambiar_ventana):
        super().__init__()
        self.cambiar_ventana = cambiar_ventana
        self.controller = ModController()

        self.setWindowTitle("Ciencias de la Computación II - Función Hash (Módulo)")

        # --- Layout principal ---
        central = QWidget()
        layout = QVBoxLayout(central)
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

        titulo = QLabel("Ciencias de la Computación II - Función Hash (Módulo)")
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
        btn_inicio.clicked.connect(lambda: self.cambiar_ventana("inicio"))
        btn_busqueda.clicked.connect(lambda: self.cambiar_ventana("busqueda"))

        layout.addWidget(header)

        # --- Controles superiores ---
        self.rango = QComboBox()
        self.rango.addItems([f"10^{i}" for i in range(1, 6)])  # igual que en binaria_interna
        self.digitos = QSpinBox()
        self.digitos.setRange(1, 10)
        self.digitos.setValue(4)

        self.btn_crear = QPushButton("Crear estructura")
        self.btn_agregar = QPushButton("Adicionar claves")
        self.btn_cargar = QPushButton("Cargar estructura")
        self.btn_eliminar = QPushButton("Eliminar estructura")

        for btn in (self.btn_crear, self.btn_agregar, self.btn_cargar, self.btn_eliminar):
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #7C3AED;
                    color: white;
                    padding: 10px 20px;
                    font-size: 16px;
                    border-radius: 10px;
                }
                QPushButton:hover {
                    background-color: #6D28D9;
                }
            """)

        controles = QVBoxLayout()
        controles.addWidget(QLabel("Rango (10^n):"))
        controles.addWidget(self.rango)
        controles.addWidget(QLabel("Número de dígitos de la clave:"))
        controles.addWidget(self.digitos)

        grid_botones = QGridLayout()
        grid_botones.addWidget(self.btn_crear, 0, 0)
        grid_botones.addWidget(self.btn_agregar, 0, 1)
        grid_botones.addWidget(self.btn_cargar, 1, 0)
        grid_botones.addWidget(self.btn_eliminar, 1, 1)

        controles.addLayout(grid_botones)
        layout.addLayout(controles)

        # --- Contenedor con scroll ---
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.contenedor = QWidget()
        self.grid = QGridLayout(self.contenedor)
        self.grid.setAlignment(Qt.AlignCenter)
        self.scroll.setWidget(self.contenedor)
        layout.addWidget(self.scroll)

        self.setCentralWidget(central)

        # --- Conexiones ---
        self.btn_crear.clicked.connect(self.crear_estructura)
        self.btn_agregar.clicked.connect(self.adicionar_claves)
        self.btn_cargar.clicked.connect(self.cargar_estructura)
        self.btn_eliminar.clicked.connect(self.eliminar_estructura)

        # Estado
        self.labels = []
        self.capacidad = 0

    # --- Métodos básicos ---
    def crear_estructura(self):
        # Limpia y crea la estructura vacía
        for i in reversed(range(self.grid.count())):
            widget = self.grid.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        self.labels.clear()

        n = int(self.rango.currentText().split("^")[1])
        capacidad = 10 ** n
        self.capacidad = capacidad

        # ✅ Solo pasas los dígitos
        self.controller.crear_estructura(self.digitos.value())
        self.capacidad = self.controller.capacidad

        if capacidad > 1000:
            QMessageBox.information(
                self, "Vista representativa",
                f"La capacidad real es {capacidad}, "
                "pero solo se muestra parcialmente."
            )
            mostrar = 50
            for i in range(mostrar):
                self._agregar_cuadro(i + 1, i + 1)  # visual 1..50, real 1..50

            puntos = QLabel("...")
            puntos.setStyleSheet("font-size: 18px; color: gray;")
            self.grid.addWidget(
                puntos, (mostrar // 10) * 2, mostrar % 10, 2, 1, alignment=Qt.AlignCenter
            )

            for i in range(mostrar):
                idx_real = capacidad - mostrar + i + 1
                self._agregar_cuadro(mostrar + i + 1, idx_real)
            else:
                for i in range(capacidad):
                    self._agregar_cuadro(i + 1, i + 1)

    def _agregar_cuadro(self, idx_visual, idx_real):
        fila = ((idx_visual - 1) // 10) * 2
        col = (idx_visual - 1) % 10

        cuadro = QLabel("")
        cuadro.setAlignment(Qt.AlignCenter)
        cuadro.setFixedSize(60, 60)
        cuadro.setStyleSheet("""
            QLabel {
                background-color: #EDE9FE;
                border: 2px solid #7C3AED;
                border-radius: 12px;
                font-size: 16px;
            }
        """)
        self.grid.addWidget(cuadro, fila, col, alignment=Qt.AlignCenter)

        # debajo se muestra el índice real
        numero = QLabel(str(idx_real))
        numero.setAlignment(Qt.AlignCenter)
        numero.setStyleSheet("font-size: 14px; color: gray; margin-top: 5px;")
        self.grid.addWidget(numero, fila + 1, col, alignment=Qt.AlignCenter)

        self.labels.append(cuadro)

    def adicionar_claves(self):
        if self.capacidad == 0 or self.controller is None:
            QMessageBox.warning(self, "Error", "Primero cree la estructura.")
            return

        dialogo = DialogoClave(self.digitos.value(), self)
        if dialogo.exec() == QDialog.Accepted:
            clave = dialogo.get_clave()
            resultado = self.controller.adicionar_clave(clave)

            if resultado == "OK":
                datos = self.controller.obtener_datos_vista()
                for i, val in datos["estructura"].items():
                    if i < len(self.labels):
                        self.labels[i].setText(val)
            elif resultado == "LONGITUD":
                QMessageBox.warning(self, "Error", "La clave no cumple con la longitud definida.")
            elif resultado == "REPETIDA":
                QMessageBox.warning(self, "Error", "La clave ya existe en la estructura.")
            elif resultado == "LLENO":
                QMessageBox.warning(self, "Error", "La estructura está llena.")

    def cargar_estructura(self):
        QMessageBox.information(self, "Pendiente", "Lógica de cargar estructura aún no implementada.")

    def eliminar_estructura(self):
        if self.controller:
            self.controller = ModController(self.capacidad, self.digitos.value())
        for lbl in self.labels:
            lbl.setText("")
        QMessageBox.information(self, "Éxito", "La estructura fue eliminada correctamente.")

