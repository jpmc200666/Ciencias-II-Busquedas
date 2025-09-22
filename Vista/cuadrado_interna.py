from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel, QFrame,
    QComboBox, QSpinBox, QPushButton, QGridLayout, QScrollArea,
    QMessageBox, QHBoxLayout
)
from PySide6.QtCore import Qt
from .dialogo_clave import DialogoClave
from Controlador.Internas.cuadrado_controller import CuadradoController


class CuadradoInterna(QMainWindow):
    def __init__(self, cambiar_ventana):
        super().__init__()
        self.cambiar_ventana = cambiar_ventana
        self.controller = CuadradoController()

        self.setWindowTitle("Ciencias de la Computación II - Búsqueda por Cuadrado")

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

        titulo = QLabel("Ciencias de la Computación II - Búsqueda por Cuadrado")
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

        # --- Controles ---
        self.rango = QComboBox()
        self.rango.addItems([f"10^{i}" for i in range(1, 6)])
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
        for i in reversed(range(self.grid.count())):
            widget = self.grid.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        self.labels.clear()

        n = int(self.rango.currentText().split("^")[1])
        self.capacidad = 10 ** n
        self.controller.crear_estructura(self.capacidad, self.digitos.value())

        for i in range(self.capacidad if self.capacidad <= 100 else 100):
            self._agregar_cuadro(i)

    def _agregar_cuadro(self, i):
        fila = (i // 10) * 2
        col = i % 10

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

        numero = QLabel(str(i + 1))
        numero.setAlignment(Qt.AlignCenter)
        numero.setStyleSheet("font-size: 14px; color: gray; margin-top: 5px;")
        self.grid.addWidget(numero, fila + 1, col, alignment=Qt.AlignCenter)

        self.labels.append(cuadro)

    def adicionar_claves(self):
        if not self.labels:
            QMessageBox.warning(self, "Error", "Primero cree la estructura.")
            return

        dlg = DialogoClave(self.digitos.value(), self)
        if dlg.exec():
            clave = dlg.get_clave()
            estado = self.controller.adicionar_clave(clave)

            if estado == "OK":
                estructura = self.controller.estructura
                for i, lbl in enumerate(self.labels, start=1):  # labels empieza en 1..capacidad
                    valor = estructura.get(i, "")
                    if valor != "":
                        lbl.setText(valor)
                        lbl.setStyleSheet("""
                            QLabel {
                                background-color: #C4B5FD;
                                border: 2px solid #6D28D9;
                                border-radius: 12px;
                                font-size: 18px;
                                font-weight: bold;
                            }
                        """)
                    else:
                        lbl.setText("")
                        lbl.setStyleSheet("""
                            QLabel {
                                background-color: #EDE9FE;
                                border: 2px solid #A78BFA;
                                border-radius: 12px;
                                font-size: 18px;
                            }
                        """)


            elif estado == "REPETIDA":
                QMessageBox.warning(self, "Error", f"La clave {clave} ya fue insertada.")
            elif estado == "LLENO":
                QMessageBox.warning(self, "Error", "La estructura está llena.")
            elif estado == "LONGITUD":
                QMessageBox.warning(self, "Error", "Longitud incorrecta.")

    def cargar_estructura(self):
        QMessageBox.information(self, "Pendiente", "Lógica de cargar estructura aún no implementada.")

    def eliminar_estructura(self):
        QMessageBox.information(self, "Pendiente", "Lógica de eliminar estructura aún no implementada.")
