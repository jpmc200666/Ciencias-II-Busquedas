from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QComboBox, QSpinBox, QGridLayout, QMessageBox, QScrollArea,
    QFileDialog, QInputDialog, QFrame, QDialog
)
from PySide6.QtCore import Qt
from .dialogo_clave import DialogoClave
from Controlador.Internas.plegamiento_controller import PlegamientoController
from .dialogo_colision import DialogoColisiones
from .vista_arreglo_anidado import VistaArregloAnidado
from .vista_lista_encadenada import VistaListaEncadenada
from Controlador.lista_encadenada_controller import ListaEncadenadaController
from Controlador.arreglo_anidado_controller import ArregloAnidadoController


class PlegamientoInterna(QMainWindow):
    def __init__(self, cambiar_ventana):
        super().__init__()
        self.estrategia_actual = None
        self.cambiar_ventana = cambiar_ventana
        self.controller = PlegamientoController()
        self.setWindowTitle("Ciencias de la Computación II - Función Hash (Plegamiento)")

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

        titulo = QLabel("Ciencias de la Computación II - Función Hash (Plegamiento)")
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

        btn_inicio.clicked.connect(lambda: self.cambiar_ventana("inicio"))
        btn_busqueda.clicked.connect(lambda: self.cambiar_ventana("busqueda"))
        header_layout.addLayout(menu_layout)
        layout.addWidget(header)

        # --- Controles superiores ---
        controles_layout = QHBoxLayout()
        controles_layout.setAlignment(Qt.AlignCenter)

        lbl_rango = QLabel("Rango (10^n):")
        lbl_rango.setStyleSheet("font-weight: bold;")
        self.rango = QComboBox()
        self.rango.addItems([f"10^{i}" for i in range(1, 6)])
        self.rango.setFixedWidth(80)

        lbl_digitos = QLabel("Número de dígitos:")
        lbl_digitos.setStyleSheet("font-weight: bold;")
        self.digitos = QSpinBox()
        self.digitos.setRange(2, 10)
        self.digitos.setValue(4)
        self.digitos.setFixedWidth(60)

        controles_layout.addWidget(lbl_rango)
        controles_layout.addWidget(self.rango)
        controles_layout.addSpacing(20)
        controles_layout.addWidget(lbl_digitos)
        controles_layout.addWidget(self.digitos)
        layout.addLayout(controles_layout)

        # --- Botones (mismo diseño y distribución que CuadradoInterna) ---
        botones_layout = QGridLayout()
        botones_layout.setSpacing(15)

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

        for btn in botones:
            btn.setFixedHeight(50)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #7C3AED;
                    color: white;
                    font-size: 16px;
                    border-radius: 10px;
                }
                QPushButton:hover {
                    background-color: #6D28D9;
                }
            """)

        botones_layout.addWidget(self.btn_crear, 0, 0)
        botones_layout.addWidget(self.btn_agregar, 0, 1)
        botones_layout.addWidget(self.btn_buscar, 0, 2)
        botones_layout.addWidget(self.btn_eliminar_clave, 0, 3)
        botones_layout.addWidget(self.btn_deshacer, 1, 0)
        botones_layout.addWidget(self.btn_guardar, 1, 1)
        botones_layout.addWidget(self.btn_eliminar, 1, 2)
        botones_layout.addWidget(self.btn_cargar, 1, 3)

        layout.addLayout(botones_layout)

        # --- Área de scroll para la estructura ---
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

        self.labels = []
        self.capacidad = 0

    # --- Métodos funcionales ---
    def crear_estructura(self):
        for i in reversed(range(self.grid.count())):
            widget = self.grid.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        self.labels.clear()

        n = int(self.rango.currentText().split("^")[1])
        self.capacidad = 10 ** n
        self.controller.crear_estructura(self.capacidad, self.digitos.value())

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
        # --- Pedir clave con el diálogo personalizado ---
        dlg_clave = DialogoClave(self.controller.digitos, titulo="Adicionar clave", modo="insertar", parent=self)
        if dlg_clave.exec() != QDialog.Accepted:
            return  # usuario canceló

        clave = dlg_clave.get_clave()
        if not clave:
            QMessageBox.warning(self, "Error", "Debe ingresar una clave válida.")
            return

        # --- Validaciones previas ---
        if len(clave) != self.controller.digitos:
            QMessageBox.warning(self, "Error", f"La clave debe tener {self.controller.digitos} dígitos.")
            return

        if self.controller._clave_existe(clave):
            QMessageBox.warning(self, "Error", f"La clave '{clave}' ya existe en la estructura.")
            return

        # --- Intentar insertar ---
        resultado = self.controller.adicionar_clave(clave)

        # ✅ Inserción directa sin colisión
        if resultado == "OK":
            QMessageBox.information(self, "Éxito", f"Clave '{clave}' insertada correctamente.")
            self.actualizar_tabla()
            return

        # ⚠️ Colisión detectada: pedir estrategia de resolución
        if resultado == "COLISION":
            dlg_col = DialogoColisiones(self)
            if dlg_col.exec() == QDialog.Accepted:
                estrategia = dlg_col.get_estrategia()
                if not estrategia:
                    QMessageBox.warning(self, "Error", "Debe seleccionar una estrategia de colisión.")
                    return

                resultado = self.controller.adicionar_clave(clave, estrategia)
                if resultado == "OK":
                    QMessageBox.information(self, "Éxito", f"Clave '{clave}' insertada usando {estrategia}.")
                    self.estrategia_actual = estrategia.lower()
                    self.actualizar_vista_segun_estrategia()
                elif resultado == "REPETIDA":
                    QMessageBox.warning(self, "Error", f"La clave '{clave}' ya está registrada.")
                elif resultado == "LLENO":
                    QMessageBox.warning(self, "Error", "La estructura está llena.")
                else:
                    QMessageBox.warning(self, "Error", f"No se pudo insertar: {resultado}")
            else:
                QMessageBox.information(self, "Cancelado", "Inserción cancelada por el usuario.")
            return

        # ❌ Otros casos de error
        if resultado == "REPETIDA":
            QMessageBox.warning(self, "Error", f"La clave '{clave}' ya está registrada.")
        elif resultado == "LLENO":
            QMessageBox.warning(self, "Error", "La estructura está llena.")
        elif resultado == "LONGITUD":
            QMessageBox.warning(self, "Error", f"La clave debe tener {self.controller.digitos} dígitos.")
        else:
            QMessageBox.warning(self, "Error", f"Error inesperado: {resultado}")

    def buscar_clave(self):
        clave, ok = QInputDialog.getText(self, "Buscar Clave", "Ingrese la clave a buscar:")
        if not ok or not clave:
            return

        encontrado = self.controller.buscar_clave(clave)
        if encontrado != -1:
            QMessageBox.information(self, "Resultado", f"Clave {clave} encontrada en posición {encontrado + 1}")
        else:
            QMessageBox.warning(self, "Resultado", "Clave no encontrada.")

    def eliminar_clave(self):
        clave, ok = QInputDialog.getText(self, "Eliminar Clave", "Ingrese la clave a eliminar:")
        if not ok or not clave:
            return

        resultado = self.controller.eliminar_clave(clave)
        if resultado == "OK":
            QMessageBox.information(self, "Éxito", f"Clave {clave} eliminada correctamente.")
            self.actualizar_tabla()
        elif resultado == "NO_EXISTE":
            QMessageBox.warning(self, "Error", "La clave no existe.")
        else:
            QMessageBox.warning(self, "Error", f"Ocurrió un problema: {resultado}")

    def deshacer(self):
        resultado = self.controller.deshacer()
        if resultado == "OK":
            QMessageBox.information(self, "Éxito", "Se deshizo el último movimiento.")
            self.actualizar_tabla()
        elif resultado == "VACIO":
            QMessageBox.warning(self, "Aviso", "No hay movimientos para deshacer.")

    def guardar_estructura(self):
        ruta, _ = QFileDialog.getSaveFileName(self, "Guardar estructura", "plegamiento_interna.json", "Archivos JSON (*.json)")
        if not ruta:
            return
        try:
            self.controller.ruta_archivo = ruta
            self.controller.guardar()
            QMessageBox.information(self, "Éxito", f"Estructura guardada en:\n{ruta}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo guardar:\n{e}")

    def cargar_estructura(self):
        ruta, _ = QFileDialog.getOpenFileName(self, "Cargar estructura", "", "Archivos JSON (*.json)")
        if ruta:
            self.controller.ruta_archivo = ruta
            if self.controller.cargar():
                self.capacidad = self.controller.capacidad
                if hasattr(self.controller, 'estrategia_fija') and self.controller.estrategia_fija:
                    self.estrategia_actual = self.controller.estrategia_fija.lower()

                if hasattr(self.controller, 'estructura_anidada') and self.controller.estructura_anidada:
                    if not self.estrategia_actual:
                        self.estrategia_actual = "lista encadenada"

                QMessageBox.information(
                    self,
                    "Éxito",
                    f"Estructura cargada correctamente.\nEstrategia: {self.estrategia_actual or 'direccionamiento abierto'}"
                )
                self.actualizar_vista_segun_estrategia()
            else:
                QMessageBox.warning(self, "Error", "No se pudo cargar el archivo.")

    def eliminar_estructura(self):
        self.estrategia_actual = None
        resp = QMessageBox.question(
            self, "Eliminar estructura", "¿Desea eliminar la estructura actual?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if resp == QMessageBox.Yes:
            self.controller.estructura = {}
            self.controller.capacidad = 0
            self.controller.historial.clear()
            self.actualizar_tabla()
            QMessageBox.information(self, "Éxito", "Estructura eliminada correctamente.")

    def actualizar_tabla(self):
        datos = self.controller.obtener_datos_vista()
        estructura = datos.get("estructura", {})
        arreglo_anidado = datos.get("arreglo_anidado", [])
        lista_encadenada = datos.get("lista_encadenada", [])

        for i in reversed(range(self.grid.count())):
            widget = self.grid.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        for i in range(self.controller.capacidad):
            fila = (i // 10) * 3
            col = i % 10

            celda = QLabel(str(estructura.get(i + 1, "")) or "")
            celda.setAlignment(Qt.AlignCenter)
            celda.setFixedSize(60, 60)
            celda.setStyleSheet("""
                QLabel {
                    background-color: #EDE9FE;
                    border: 2px solid #7C3AED;
                    border-radius: 12px;
                    font-size: 16px;
                }
            """)
            self.grid.addWidget(celda, fila, col, alignment=Qt.AlignCenter)

            numero = QLabel(str(i + 1))
            numero.setAlignment(Qt.AlignCenter)
            numero.setStyleSheet("font-size: 14px; color: gray; margin-top: 5px;")
            self.grid.addWidget(numero, fila + 1, col, alignment=Qt.AlignCenter)

            # --- Mostrar colisiones debajo ---
            colisiones = []
            if arreglo_anidado[i]:
                colisiones = arreglo_anidado[i]
            elif lista_encadenada[i]:
                colisiones = lista_encadenada[i]

            if colisiones:
                col_label = QLabel(" → ".join(colisiones))
                col_label.setAlignment(Qt.AlignCenter)
                col_label.setStyleSheet("""
                    color: #5B21B6;
                    font-size: 13px;
                    background-color: #DDD6FE;
                    border-radius: 8px;
                    padding: 3px;
                """)
                self.grid.addWidget(col_label, fila + 2, col, alignment=Qt.AlignCenter)

        self.labels = [self.grid.itemAt(j).widget() for j in range(0, self.grid.count(), 3)]

    def actualizar_vista_segun_estrategia(self):
        if self.estrategia_actual == "arreglo anidado":
            anidado_ctrl = ArregloAnidadoController(self.controller)
            vista_anidada = VistaArregloAnidado(self.grid, anidado_ctrl)
            vista_anidada.dibujar()
        elif self.estrategia_actual == "lista encadenada":
            encadenada_ctrl = ListaEncadenadaController(self.controller)
            vista_encadenada = VistaListaEncadenada(self.grid, encadenada_ctrl)
            vista_encadenada.dibujar()
        else:
            self.actualizar_tabla()
