from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel, QFrame,
    QComboBox, QSpinBox, QPushButton, QGridLayout, QScrollArea,
    QInputDialog, QHBoxLayout, QDialog, QFileDialog, QMessageBox
)
from PySide6.QtCore import Qt

from Controlador.Internas.truncamiento_controller import TruncamientoController
from Vista.dialogo_clave import DialogoClave
from Vista.dialogo_posiciones import DialogoPosiciones


class TruncamientoInterna(QMainWindow):
    def __init__(self, cambiar_ventana):
        super().__init__()
        self.cambiar_ventana = cambiar_ventana
        self.controller = TruncamientoController()
        self.setWindowTitle("Ciencias de la Computación II - Función Hash (Truncamiento)")

        # --- Layout principal ---
        central = QWidget()
        layout = QVBoxLayout(central)
        layout.setSpacing(15)

        # --- Encabezado ---
        header = QFrame()
        header.setStyleSheet("""
            background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0,
            stop:0 #D8B4FE, stop:1 #A78BFA);
            border-radius: 12px;
        """)
        header_layout = QVBoxLayout(header)
        header_layout.setSpacing(5)

        titulo = QLabel("Ciencias de la Computación II - Función Hash (Truncamiento)")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("""
            font-size: 26px;
            font-weight: bold;
            color: white;
            margin-top: 10px;
        """)
        header_layout.addWidget(titulo)

        # --- Menú superior ---
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
        layout.addWidget(header)

        btn_inicio.clicked.connect(lambda: self.cambiar_ventana("inicio"))
        btn_busqueda.clicked.connect(lambda: self.cambiar_ventana("busqueda"))

        # --- Controles superiores ---
        controles_superiores = QHBoxLayout()
        controles_superiores.setSpacing(15)
        controles_superiores.setAlignment(Qt.AlignCenter)

        lbl_rango = QLabel("Rango (10^n):")
        lbl_rango.setStyleSheet("font-weight: bold; font-size: 14px;")
        self.rango = QComboBox()
        self.rango.addItems([f"10^{i}" for i in range(1, 6)])
        self.rango.setFixedWidth(100)

        lbl_digitos = QLabel("Número de dígitos:")
        lbl_digitos.setStyleSheet("font-weight: bold; font-size: 14px;")
        self.digitos = QSpinBox()
        self.digitos.setRange(1, 10)
        self.digitos.setValue(4)
        self.digitos.setFixedWidth(60)

        controles_superiores.addWidget(lbl_rango)
        controles_superiores.addWidget(self.rango)
        controles_superiores.addWidget(lbl_digitos)
        controles_superiores.addWidget(self.digitos)
        layout.addLayout(controles_superiores)

        # --- Botones principales ---
        botones_layout = QGridLayout()
        botones_layout.setSpacing(12)
        botones_layout.setAlignment(Qt.AlignCenter)

        self.btn_crear = QPushButton("Crear estructura")
        self.btn_agregar = QPushButton("Adicionar claves")
        self.btn_buscar = QPushButton("Buscar clave")
        self.btn_eliminar_clave = QPushButton("Eliminar clave")
        self.btn_deshacer = QPushButton("Deshacer último movimiento")
        self.btn_guardar = QPushButton("Guardar estructura")
        self.btn_eliminar = QPushButton("Eliminar estructura")
        self.btn_cargar = QPushButton("Cargar estructura")

        botones = [
            self.btn_crear, self.btn_agregar, self.btn_buscar, self.btn_eliminar_clave,
            self.btn_deshacer, self.btn_guardar, self.btn_eliminar, self.btn_cargar
        ]

        for i, btn in enumerate(botones):
            btn.setFixedHeight(45)
            btn.setFixedWidth(240)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #7C3AED;
                    color: white;
                    font-size: 15px;
                    border-radius: 10px;
                    padding: 8px 20px;
                }
                QPushButton:hover {
                    background-color: #6D28D9;
                }
            """)
            fila = i // 4
            col = i % 4
            botones_layout.addWidget(btn, fila, col, alignment=Qt.AlignCenter)

        layout.addLayout(botones_layout)

        # --- Contenedor con scroll ---
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.contenedor = QWidget()
        self.grid = QGridLayout(self.contenedor)
        self.grid.setAlignment(Qt.AlignCenter)
        self.scroll.setWidget(self.contenedor)
        layout.addWidget(self.scroll)

        self.setCentralWidget(central)

        # Conexiones
        self.btn_crear.clicked.connect(self.crear_estructura)
        self.btn_agregar.clicked.connect(self.adicionar_claves)
        self.btn_cargar.clicked.connect(self.cargar_estructura)
        self.btn_eliminar.clicked.connect(self.eliminar_estructura)
        self.btn_buscar.clicked.connect(self.buscar_clave)
        self.btn_eliminar_clave.clicked.connect(self.eliminar_clave)
        self.btn_deshacer.clicked.connect(self.deshacer)
        self.btn_guardar.clicked.connect(self.guardar_estructura)

        # Estado
        self.labels = []
        self.capacidad = 0

    # ==============================================================
    # MÉTODOS FUNCIONALES
    # ==============================================================

    def crear_estructura(self):
        # Limpia la vista
        for i in reversed(range(self.grid.count())):
            w = self.grid.itemAt(i).widget()
            if w:
                w.setParent(None)
        self.labels.clear()

        n = int(self.rango.currentText().split("^")[1])
        self.capacidad = 10 ** n
        dig = self.digitos.value()
        self.controller.crear_estructura(self.capacidad, dig, [])

        try:
            digitos_req = self.controller._digitos_necesarios()
        except AttributeError:
            QMessageBox.warning(self, "Error", "El controlador no tiene el método '_digitos_necesarios'.")
            return

        dlg = DialogoPosiciones(dig, digitos_req, parent=self)
        if dlg.exec() == QDialog.Accepted:
            posiciones = dlg.get_posiciones(digitos_req)
            if posiciones and len(posiciones) == digitos_req:
                self.controller.posiciones = posiciones
                QMessageBox.information(self, "OK", f"Posiciones seleccionadas: {posiciones}")
            else:
                QMessageBox.warning(self, "Error", "Número incorrecto de posiciones.")
        else:
            QMessageBox.warning(self, "Cancelado", "Debes seleccionar posiciones.")

        # Dibujar estructura visual
        for i in range(min(self.capacidad, 100)):
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

        numero = QLabel(str(idx_real))
        numero.setAlignment(Qt.AlignCenter)
        numero.setStyleSheet("font-size: 14px; color: gray; margin-top: 5px;")
        self.grid.addWidget(numero, fila + 1, col, alignment=Qt.AlignCenter)
        self.labels.append(cuadro)

    def adicionar_claves(self):
        if self.capacidad == 0:
            QMessageBox.warning(self, "Error", "Primero cree la estructura.")
            return

        if not self.controller.posiciones:
            QMessageBox.warning(self, "Error", "Seleccione las posiciones primero.")
            return

        dialogo = DialogoClave(
            longitud=self.digitos.value(),
            titulo=f"Clave de {self.digitos.value()} dígitos",
            modo="insertar",
            parent=self
        )
        if dialogo.exec() != QDialog.Accepted:
            return

        clave = dialogo.get_clave()
        resultado = self.controller.agregar_clave(clave)

        if resultado == "OK":
            QMessageBox.information(self, "Éxito", f"Clave {clave} insertada correctamente.")
            self.actualizar_tabla()
        else:
            QMessageBox.warning(self, "Error", f"Resultado: {resultado}")

    def eliminar_clave(self):
        clave, ok = QInputDialog.getText(self, "Eliminar Clave", "Ingrese la clave a eliminar:")
        if not ok or not clave.strip():
            return

        resultado = self.controller.eliminar_clave(clave.strip())
        QMessageBox.information(self, "Resultado", resultado)
        self.actualizar_tabla()

    def buscar_clave(self):
        clave, ok = QInputDialog.getText(self, "Buscar Clave", "Ingrese la clave:")
        if not ok or not clave.strip():
            return

        encontrado = None
        for pos, valor in self.controller.estructura.items():
            if str(valor) == clave:
                encontrado = pos
                break

        if encontrado:
            QMessageBox.information(self, "Resultado", f"Clave {clave} encontrada en posición {encontrado}")
        else:
            QMessageBox.warning(self, "Resultado", "Clave no encontrada.")

    def deshacer(self):
        res = self.controller.deshacer()
        QMessageBox.information(self, "Deshacer", res)
        self.actualizar_tabla()

    def eliminar_estructura(self):
        resp = QMessageBox.question(
            self, "Eliminar estructura", "¿Desea eliminar la estructura actual?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if resp == QMessageBox.Yes:
            self.controller.estructura = {}
            self.controller.posiciones = []
            self.actualizar_tabla()
            QMessageBox.information(self, "Éxito", "Estructura eliminada correctamente.")

    def guardar_estructura(self):
        ruta, _ = QFileDialog.getSaveFileName(self, "Guardar estructura", "truncamiento_interna.json", "Archivos JSON (*.json)")
        if ruta:
            self.controller.ruta_archivo = ruta
            self.controller.guardar()
            QMessageBox.information(self, "Éxito", f"Estructura guardada en:\n{ruta}")

    def cargar_estructura(self):
        ruta, _ = QFileDialog.getOpenFileName(self, "Cargar estructura", "", "Archivos JSON (*.json)")
        if ruta:
            self.controller.ruta_archivo = ruta
            if self.controller.cargar():
                QMessageBox.information(self, "Éxito", "Estructura cargada correctamente.")
                self.actualizar_tabla()
            else:
                QMessageBox.warning(self, "Error", "No se pudo cargar el archivo.")

    def actualizar_tabla(self):
        for i, lbl in enumerate(self.labels, start=1):
            valor = self.controller.estructura.get(i, "")
            lbl.setText(str(valor) if valor else "")
