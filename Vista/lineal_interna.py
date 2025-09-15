from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel, QFrame,
    QComboBox, QSpinBox, QPushButton, QGridLayout, QScrollArea,
    QMessageBox, QHBoxLayout
)
from PySide6.QtCore import Qt
from .dialogo_clave import DialogoClave  # 👈 importamos el diálogo
from Controlador.Internas.lineal_controller import LinealController


class LinealInterna(QMainWindow):
    def __init__(self, cambiar_ventana):
        super().__init__()
        self.cambiar_ventana = cambiar_ventana
        self.controller = LinealController()

        self.setWindowTitle("Ciencias de la Computación II - Búsqueda Lineal")

        # --- Layout principal ---
        central = QWidget()
        layout = QVBoxLayout(central)
        layout.setSpacing(20)

        # --- Encabezado ---
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

        titulo = QLabel("Ciencias de la Computación II - Búsqueda Lineal")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("font-size: 26px; font-weight: bold; color: white; margin: 10px;")
        header_layout.addWidget(titulo)

        # --- Menú debajo del título ---
        menu_layout = QHBoxLayout()
        menu_layout.setSpacing(40)  # separación entre botones
        menu_layout.setAlignment(Qt.AlignCenter)  # 👈 asegura que queden al centro

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

        # 👇 agrega el layout al header (debajo del título)
        header_layout.addLayout(menu_layout)

        # Conexiones del menú
        btn_inicio.clicked.connect(lambda: self.cambiar_ventana("inicio"))
        btn_busqueda.clicked.connect(lambda: self.cambiar_ventana("busqueda"))

        layout.addWidget(header)

        # --- Controles superiores ---
        self.rango = QComboBox()
        self.rango.addItems([f"10^{i}" for i in range(1, 6)])
        self.digitos = QSpinBox()
        self.digitos.setRange(1, 10)
        self.digitos.setValue(4)

        self.btn_crear = QPushButton("Crear estructura")
        self.btn_agregar = QPushButton("Adicionar claves")
        self.btn_cargar = QPushButton("Cargar estructura")
        self.btn_salir = QPushButton("Eliminar estructura")

        for btn in (self.btn_crear, self.btn_agregar, self.btn_cargar, self.btn_salir):
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

        # Layout de controles (VBox + botones en 2x2)
        controles = QVBoxLayout()
        controles.addWidget(QLabel("Rango (10^n):"))
        controles.addWidget(self.rango)
        controles.addWidget(QLabel("Número de dígitos de la clave:"))
        controles.addWidget(self.digitos)

        grid_botones = QGridLayout()
        grid_botones.addWidget(self.btn_crear, 0, 0)
        grid_botones.addWidget(self.btn_agregar, 0, 1)
        grid_botones.addWidget(self.btn_cargar, 1, 0)
        grid_botones.addWidget(self.btn_salir, 1, 1)

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
        self.btn_salir.clicked.connect(self.eliminar_estructura)  # 👉 ahora usa método

        # Estado
        self.labels = []
        self.capacidad = 0

    def cargar_estructura(self):
        """Carga la estructura guardada desde el controller y actualiza la vista."""
        if self.controller.cargar():
            datos = self.controller.obtener_datos_vista()
            self.capacidad = datos["capacidad"]
            self.digitos.setValue(datos["digitos"])

            # limpiar la grilla
            for i in reversed(range(self.grid.count())):
                widget = self.grid.itemAt(i).widget()
                if widget:
                    widget.setParent(None)
            self.labels.clear()

            # reconstruir cuadros
            if self.capacidad <= 1000:
                for i in range(self.capacidad):
                    self._agregar_cuadro(i, i)
            else:
                for i in range(50):
                    self._agregar_cuadro(i, i)

                puntos = QLabel("...")
                puntos.setStyleSheet("font-size: 18px; color: gray;")
                self.grid.addWidget(
                    puntos, (50 // 10) * 2, 50 % 10, 2, 1, alignment=Qt.AlignCenter
                )

                for i in range(50):
                    idx_real = self.capacidad - 50 + i
                    self._agregar_cuadro(50 + i + 1, idx_real)

            # pintar claves guardadas
            for idx, clave in datos["estructura"].items():
                if clave and idx < len(self.labels):
                    self.labels[idx].setText(clave)
                    self.labels[idx].setStyleSheet("""
                        QLabel {
                            background-color: #C4B5FD;
                            border: 2px solid #6D28D9;
                            border-radius: 12px;
                            font-size: 18px;
                            font-weight: bold;
                        }
                    """)
        else:
            QMessageBox.warning(self, "Error", "No hay estructura guardada para cargar.")

    def crear_estructura(self):
        # Vaciar lo anterior en la interfaz
        for i in reversed(range(self.grid.count())):
            widget = self.grid.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        self.labels.clear()

        # Capacidad a partir del combo
        n = int(self.rango.currentText().split("^")[1])
        capacidad = 10 ** n

        # Crear estructura en el controlador
        self.controller.crear_estructura(capacidad, self.digitos.value())
        self.controller.guardar()
        self.capacidad = capacidad  # mantener sincronizado con la vista

        # Aviso si excede el límite
        if capacidad > 1000:
            QMessageBox.information(
                self,
                "Vista representativa",
                f"La capacidad real es {capacidad}, "
                "pero se muestra una representación parcial para no sobrecargar el programa."
            )

            mostrar_inicio = 50
            mostrar_final = 50

            # Mostrar primeros cuadros
            for i in range(mostrar_inicio):
                self._agregar_cuadro(i, i)

            # Puntos suspensivos
            puntos = QLabel("...")
            puntos.setStyleSheet("font-size: 18px; color: gray;")
            self.grid.addWidget(
                puntos,
                (mostrar_inicio // 10) * 2,
                mostrar_inicio % 10,
                2,
                1,
                alignment=Qt.AlignCenter
            )

            # Mostrar últimos cuadros
            for i in range(mostrar_final):
                idx_real = capacidad - mostrar_final + i
                self._agregar_cuadro(mostrar_inicio + i + 1, idx_real)

        else:
            # Crear todos los cuadros (10 por fila)
            for i in range(capacidad):
                self._agregar_cuadro(i, i)

    def _agregar_cuadro(self, i, idx_real):
        """Agrega un cuadro y su número en la grilla.
        i = posición visual, idx_real = índice verdadero.
        """
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
        if not self.labels:
            QMessageBox.warning(self, "Error", "Primero debe crear la estructura.")
            return

        dlg = DialogoClave(self.digitos.value(), self)
        if dlg.exec():  # Si dio aceptar
            clave = dlg.get_clave()

            # Validaciones
            if not clave.isdigit():
                QMessageBox.warning(self, "Error", "La clave debe ser numérica.")
                return

            if len(clave) != self.digitos.value():
                QMessageBox.warning(
                    self, "Error",
                    f"La clave debe tener exactamente {self.digitos.value()} dígitos."
                )
                return

            # 👉 Guardar en el controlador y revisar estado
            estado = self.controller.adicionar_clave(clave)

            if estado == "OK":
                # 👉 Repintar todos los labels con la lista ORDENADA
                claves = self.controller.get_claves()
                for i, lbl in enumerate(self.labels):
                    if i < len(claves):
                        lbl.setText(claves[i])
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
                QMessageBox.warning(self, "Clave duplicada", f"La clave {clave} ya fue insertada.")

            elif estado == "LLENO":
                QMessageBox.information(self, "Sin espacio", "No hay más espacios disponibles para agregar claves.")

            elif estado == "LONGITUD":
                QMessageBox.warning(self, "Error", f"La clave debe tener exactamente {self.digitos.value()} dígitos.")

    def eliminar_estructura(self):
        QMessageBox.information(self, "Pendiente", "Lógica de eliminar estructura aún no implementada.")
