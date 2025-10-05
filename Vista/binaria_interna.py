from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel, QFrame,
    QComboBox, QSpinBox, QPushButton, QGridLayout, QScrollArea,
    QMessageBox, QHBoxLayout, QDialog, QFileDialog, QMessageBox
)
from PySide6.QtCore import Qt
from .dialogo_clave import DialogoClave
from Controlador.Internas.binaria_controller import BinariaController


class BinariaInterna(QMainWindow):
    def __init__(self, cambiar_ventana):
        super().__init__()
        self.cambiar_ventana = cambiar_ventana
        self.controller = BinariaController()

        self.setWindowTitle("Ciencias de la Computación II - Búsqueda Binaria")

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

        titulo = QLabel("Ciencias de la Computación II - Búsqueda Binaria")
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
        self.rango.addItems([f"10^{i}" for i in range(1, 6)])
        self.digitos = QSpinBox()
        self.digitos.setRange(1, 10)
        self.digitos.setValue(4)

        # Botones principales
        self.btn_crear = QPushButton("Crear estructura")
        self.btn_agregar = QPushButton("Insertar claves")
        self.btn_buscar = QPushButton("Buscar clave")
        self.btn_eliminar_clave = QPushButton("Eliminar clave")
        self.btn_deshacer = QPushButton("Deshacer último movimiento")
        self.btn_guardar = QPushButton("Guardar estructura")
        self.btn_eliminar = QPushButton("Eliminar estructura")
        self.btn_cargar = QPushButton("Cargar estructura")

        for btn in (self.btn_crear, self.btn_agregar, self.btn_buscar, self.btn_eliminar_clave,
                    self.btn_deshacer, self.btn_guardar, self.btn_eliminar, self.btn_cargar):
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

        # Layout de controles
        self.controles = QVBoxLayout()
        self.controles.addWidget(QLabel("Rango (10^n):"))
        self.controles.addWidget(self.rango)
        self.controles.addWidget(QLabel("Número de dígitos de la clave:"))
        self.controles.addWidget(self.digitos)

        grid_botones = QGridLayout()
        grid_botones.addWidget(self.btn_crear,          0, 0)
        grid_botones.addWidget(self.btn_agregar,        0, 1)
        grid_botones.addWidget(self.btn_buscar,         0, 2)
        grid_botones.addWidget(self.btn_eliminar_clave, 0, 3)
        grid_botones.addWidget(self.btn_deshacer,       1, 0)
        grid_botones.addWidget(self.btn_guardar,        1, 1)
        grid_botones.addWidget(self.btn_eliminar,       1, 2)
        grid_botones.addWidget(self.btn_cargar,         1, 3)

        self.controles.addLayout(grid_botones)
        layout.addLayout(self.controles)

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
        self.btn_buscar.clicked.connect(self.buscar_clave)
        self.btn_eliminar_clave.clicked.connect(self.eliminar_clave)
        self.btn_deshacer.clicked.connect(self.deshacer)
        self.btn_guardar.clicked.connect(self.guardar_estructura)
        self.btn_eliminar.clicked.connect(self.eliminar_estructura)
        self.btn_cargar.clicked.connect(self.cargar_estructura)

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

        self.controller.crear_estructura(capacidad, self.digitos.value())

        if capacidad > 1000:
            QMessageBox.information(
                self, "Vista representativa",
                f"La capacidad real es {capacidad}, "
                "pero solo se muestra parcialmente."
            )
            mostrar = 50
            for i in range(mostrar):
                self._agregar_cuadro(i, i)

            puntos = QLabel("...")
            puntos.setStyleSheet("font-size: 18px; color: gray;")
            self.grid.addWidget(
                puntos, (mostrar // 10) * 2, mostrar % 10, 2, 1, alignment=Qt.AlignCenter
            )

            for i in range(mostrar):
                idx_real = capacidad - mostrar + i
                self._agregar_cuadro(mostrar + i + 1, idx_real)
        else:
            for i in range(capacidad):
                self._agregar_cuadro(i, i)

    def _agregar_cuadro(self, i, idx_real):
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

        numero = QLabel(str(idx_real + 1))
        numero.setAlignment(Qt.AlignCenter)
        numero.setStyleSheet("font-size: 14px; color: gray; margin-top: 5px;")
        self.grid.addWidget(numero, fila + 1, col, alignment=Qt.AlignCenter)

        self.labels.append(cuadro)

    def adicionar_claves(self):
        if self.capacidad == 0:
            QMessageBox.warning(self, "Error", "Primero cree la estructura.")
            return

        dialogo = DialogoClave(self.digitos.value(), "Insertar clave", parent=self)
        if dialogo.exec() == QDialog.Accepted:
            clave = dialogo.get_clave()
            resultado = self.controller.adicionar_clave(clave)

            if resultado == "OK":
                datos = self.controller.obtener_datos_vista()
                lista = list(datos["estructura"].values())

                for i, clave in enumerate(lista):
                    if i < len(self.labels):
                        self.labels[i].setText(clave)

            elif resultado == "LONGITUD":
                QMessageBox.warning(self, "Error", "La clave no cumple con la longitud definida.")
            elif resultado == "REPETIDA":
                QMessageBox.warning(self, "Error", "La clave ya existe en la estructura.")
            elif resultado == "LLENO":
                QMessageBox.warning(self, "Error", "La estructura ya está llena.")

    def buscar_clave(self):
        if self.capacidad == 0:
            QMessageBox.warning(self, "Error", "Primero cree la estructura.")
            return

        dialogo = DialogoClave(self.digitos.value(), self)
        if dialogo.exec() == QDialog.Accepted:
            clave = dialogo.get_clave()
            pos = self.controller.buscar(clave)

            for lbl in self.labels:
                lbl.setStyleSheet("""
                    QLabel {
                        background-color: #EDE9FE;
                        border: 2px solid #7C3AED;
                        border-radius: 12px;
                        font-size: 16px;
                    }
                """)

            if pos != -1 and pos < len(self.labels):
                self.labels[pos].setStyleSheet("""
                    QLabel {
                        background-color: #C084FC;
                        border: 2px solid #6D28D9;
                        border-radius: 12px;
                        font-size: 18px;
                        font-weight: bold;
                    }
                """)
                QMessageBox.information(self, "Éxito", f"Clave encontrada en posición {pos + 1}")
            else:
                QMessageBox.warning(self, "No encontrado", "La clave no está en la estructura.")

    def eliminar_clave(self):
        if self.capacidad == 0:
            QMessageBox.warning(self, "Error", "Primero cree la estructura.")
            return

        dialogo = DialogoClave(self.digitos.value(), self)
        if dialogo.exec() == QDialog.Accepted:
            clave = dialogo.get_clave()
            resultado = self.controller.eliminar_clave(clave)

            if resultado == "OK":
                datos = self.controller.obtener_datos_vista()
                lista = list(datos["estructura"].values())

                for i, lbl in enumerate(self.labels):
                    if i < len(lista):
                        lbl.setText(lista[i])
                    else:
                        lbl.setText("")
                QMessageBox.information(self, "Éxito", "Clave eliminada correctamente.")
            else:
                QMessageBox.warning(self, "Error", "La clave no existe en la estructura.")

    def eliminar_estructura(self):
        self.controller = BinariaController()
        self.capacidad = 0

        for i in reversed(range(self.grid.count())):
            widget = self.grid.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        self.labels.clear()
        QMessageBox.information(self, "Éxito", "La estructura ha sido eliminada.")

    # --- Métodos extra ---
    def deshacer(self):
        """Revierte la última acción realizada (insertar/eliminar clave)."""
        resultado = self.controller.deshacer()
        if resultado == "OK":
            datos = self.controller.obtener_datos_vista()
            lista = list(datos["estructura"].values())

            # Refrescar visual
            for i, lbl in enumerate(self.labels):
                if i < len(lista):
                    lbl.setText(lista[i])
                else:
                    lbl.setText("")

            QMessageBox.information(self, "Éxito", "Se deshizo el último movimiento.")
        else:
            QMessageBox.warning(self, "Error", "No hay movimientos para deshacer.")

    def guardar_estructura(self):
        """Abre explorador de archivos para guardar la estructura en JSON con nombre por defecto."""
        ruta, _ = QFileDialog.getSaveFileName(
            self,
            "Guardar estructura",
            "interna_binaria.json",   # <<-- nombre sugerido
            "Archivos JSON (*.json)"
        )
        if not ruta:
            return

        resultado = self.controller.guardar(ruta)
        if resultado == "OK":
            QMessageBox.information(self, "Éxito", f"Estructura guardada en:\n{ruta}")
        else:
            QMessageBox.critical(self, "Error", f"No se pudo guardar la estructura:\n{resultado}")

    def cargar_estructura(self):
        """Abre explorador de archivos para cargar la estructura en JSON."""
        # advertencia antes de sobrescribir
        if self.controller.estructura:
            resp = QMessageBox.warning(
                self,
                "Advertencia",
                "Se sobrescribirá la estructura actual.\n\n"
                "¿Desea continuar?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            if resp != QMessageBox.Yes:
                return  # cancelar

        ruta, _ = QFileDialog.getOpenFileName(
            self,
            "Cargar estructura",
            "",
            "Archivos JSON (*.json)"
        )
        if not ruta:
            return

        resultado = self.controller.cargar(ruta)
        if resultado == "OK":
            datos = self.controller.obtener_datos_vista()
            lista = list(datos["estructura"].values())
            self.capacidad = datos["capacidad"]

            # limpiar grilla previa
            for i in reversed(range(self.grid.count())):
                widget = self.grid.itemAt(i).widget()
                if widget:
                    widget.setParent(None)
            self.labels.clear()

            # volver a crear cuadros según capacidad
            capacidad = self.capacidad
            if capacidad > 1000:
                mostrar = 50
                for i in range(mostrar):
                    self._agregar_cuadro(i, i)

                puntos = QLabel("...")
                puntos.setStyleSheet("font-size: 18px; color: gray;")
                self.grid.addWidget(
                    puntos, (mostrar // 10) * 2, mostrar % 10, 2, 1, alignment=Qt.AlignCenter
                )

                for i in range(mostrar):
                    idx_real = capacidad - mostrar + i
                    self._agregar_cuadro(mostrar + i + 1, idx_real)

            else:
                for i in range(capacidad):
                    self._agregar_cuadro(i, i)

            # poner las claves cargadas
            for i, clave in enumerate(lista):
                if i < len(self.labels):
                    self.labels[i].setText(clave)

            QMessageBox.information(self, "Éxito", "Estructura cargada correctamente.")
        else:
            QMessageBox.critical(self, "Error", f"No se pudo cargar la estructura:\n{resultado}")