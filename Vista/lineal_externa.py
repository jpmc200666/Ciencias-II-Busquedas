from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel, QFrame,
    QComboBox, QSpinBox, QPushButton, QGridLayout, QScrollArea,
    QMessageBox, QHBoxLayout, QDialog, QFileDialog
)
from PySide6.QtCore import Qt
import os
import json
from Vista.dialogo_clave import DialogoClave

# Si luego agregas un controlador, lo importas aquí:
from Controlador.Externas.LinealController import LinealExternaController
# from Modelo.manejador_archivos import ManejadorArchivos
# from .dialogo_clave import DialogoClave


class LinealExterna(QMainWindow):
    def __init__(self, cambiar_ventana):
        super().__init__()
        self.cambiar_ventana = cambiar_ventana
        self.controller = LinealExternaController()
        # Variables para la estructura
        self.bloques = []  # Lista de bloques, cada bloque es una lista de claves
        self.num_claves = 0
        self.tamanio_bloque = 0

        self.setWindowTitle("Ciencias de la Computación II - Búsqueda Lineal Externa")

        central = QWidget()
        layout = QVBoxLayout(central)
        layout.setSpacing(20)

        # ======= ENCABEZADO =======
        header = QFrame()
        header.setStyleSheet("""
            background: qlineargradient(
                spread:pad, x1:0, y1:0, x2:1, y2:0,
                stop:0 #D8B4FE, stop:1 #A78BFA
            );
            border-radius: 12px;
        """)
        header_layout = QVBoxLayout(header)

        titulo = QLabel("Ciencias de la Computación II - Búsqueda Lineal Externa")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("font-size: 26px; font-weight: bold; color: white; margin: 10px;")
        header_layout.addWidget(titulo)

        # ======= MENÚ SUPERIOR =======
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

        # ======= CONTROLES SUPERIORES =======
        self.num_claves_input = QSpinBox()
        self.num_claves_input.setRange(2, 100)
        self.num_claves_input.setValue(10)
        self.num_claves_input.setFixedWidth(100)

        self.digitos = QSpinBox()
        self.digitos.setRange(1, 10)
        self.digitos.setValue(4)
        self.digitos.setFixedWidth(100)

        lbl_claves = QLabel("Número de claves (N):")
        lbl_digitos = QLabel("Número de dígitos:")
        for lbl in (lbl_claves, lbl_digitos):
            lbl.setStyleSheet("font-size: 16px; font-weight: bold;")

        fila_controles = QHBoxLayout()
        fila_controles.setSpacing(20)
        fila_controles.setAlignment(Qt.AlignCenter)
        fila_controles.addWidget(lbl_claves)
        fila_controles.addWidget(self.num_claves_input)
        fila_controles.addWidget(lbl_digitos)
        fila_controles.addWidget(self.digitos)
        layout.addLayout(fila_controles)

        # ======= BOTONES =======
        self.btn_crear = QPushButton("Crear estructura")
        self.btn_insertar = QPushButton("Insertar claves")
        self.btn_guardar = QPushButton("Guardar estructura")
        self.btn_cargar = QPushButton("Cargar estructura")
        self.btn_eliminar = QPushButton("Eliminar estructura")
        self.btn_deshacer = QPushButton("Deshacer último movimiento")
        self.btn_eliminar_clave = QPushButton("Eliminar clave")
        self.btn_buscar_clave = QPushButton("Buscar clave")

        botones = (
            self.btn_crear, self.btn_insertar, self.btn_guardar,
            self.btn_cargar, self.btn_eliminar, self.btn_deshacer,
            self.btn_eliminar_clave, self.btn_buscar_clave
        )
        for btn in botones:
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

        grid_botones = QGridLayout()
        grid_botones.addWidget(self.btn_crear, 0, 0)
        grid_botones.addWidget(self.btn_insertar, 0, 1)
        grid_botones.addWidget(self.btn_buscar_clave, 0, 2)
        grid_botones.addWidget(self.btn_eliminar_clave, 0, 3)
        grid_botones.addWidget(self.btn_deshacer, 1, 0)
        grid_botones.addWidget(self.btn_guardar, 1, 1)
        grid_botones.addWidget(self.btn_eliminar, 1, 2)
        grid_botones.addWidget(self.btn_cargar, 1, 3)
        layout.addLayout(grid_botones)

        # ======= ÁREA DE VISUALIZACIÓN =======
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.contenedor = QWidget()
        self.contenedor_layout = QVBoxLayout(self.contenedor)
        self.contenedor_layout.setSpacing(10)
        self.contenedor_layout.setContentsMargins(20, 20, 20, 20)
        self.contenedor_layout.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.scroll.setWidget(self.contenedor)
        layout.addWidget(self.scroll)

        self.setCentralWidget(central)

        # ======= CONEXIONES (por ahora vacías) =======
        self.btn_crear.clicked.connect(self.crear_estructura)
        self.btn_insertar.clicked.connect(self.insertar_clave)
        self.btn_guardar.clicked.connect(self.guardar_estructura)
        self.btn_cargar.clicked.connect(self.cargar_estructura)
        self.btn_eliminar.clicked.connect(self.eliminar_estructura)
        self.btn_deshacer.clicked.connect(self.deshacer)
        self.btn_eliminar_clave.clicked.connect(self.eliminar_clave)
        self.btn_buscar_clave.clicked.connect(self.buscar_clave)

    # ======= MÉTODOS BÁSICOS =======
    def crear_estructura(self):
        """Crea la estructura de bloques según N claves"""
        try:
            num_claves = self.num_claves_input.value()
            datos = self.controller.crear_estructura(num_claves)
            self.bloques = datos['bloques']
            self.num_claves = datos['num_claves']
            self.tamanio_bloque = datos['tamanio_bloque']

            self.actualizar_visualizacion()
            QMessageBox.information(
                self,
                "Estructura Creada",
                f"Estructura creada exitosamente:\n\n"
                f"• N (claves totales): {self.num_claves}\n"
                f"• B (tamaño de bloque): {self.tamanio_bloque}\n"
                f"• Número de bloques: {len(self.bloques)}"
            )
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al crear estructura: {str(e)}")

    def actualizar_visualizacion(self):
        """Actualiza la visualización de los bloques"""
        # Limpiar contenedor
        while self.contenedor_layout.count():
            child = self.contenedor_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        if not self.bloques:
            label = QLabel("No hay estructura creada. Presiona 'Crear estructura' para comenzar.")
            label.setStyleSheet("font-size: 16px; color: #6B7280; padding: 40px;")
            label.setAlignment(Qt.AlignCenter)
            self.contenedor_layout.addWidget(label)
            return

        # Título de información
        info_label = QLabel(
            f"Estructura: {self.num_claves} claves | "
            f"Tamaño de bloque: {self.tamanio_bloque} | "
            f"Bloques: {len(self.bloques)}"
        )
        info_label.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #7C3AED;
            padding: 10px;
            background-color: #F3E8FF;
            border-radius: 8px;
            margin-bottom: 20px;
        """)
        info_label.setAlignment(Qt.AlignCenter)
        self.contenedor_layout.addWidget(info_label)

        # Contenedor para los bloques en disposición horizontal
        bloques_container = QWidget()
        bloques_layout = QHBoxLayout(bloques_container)
        bloques_layout.setSpacing(30)
        bloques_layout.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        bloques_layout.setContentsMargins(20, 20, 20, 20)

        # Dibujar cada bloque uno al lado del otro
        for i, bloque in enumerate(self.bloques):
            bloque_widget = self.crear_bloque_visual(i, bloque)
            bloques_layout.addWidget(bloque_widget)

        bloques_layout.addStretch()
        self.contenedor_layout.addWidget(bloques_container)

    def crear_bloque_visual(self, indice, bloque):
        """Crea la representación visual de un bloque horizontal con celdas"""
        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.setSpacing(3)
        container_layout.setContentsMargins(0, 0, 0, 0)

        # Frame que contiene las celdas
        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background-color: transparent;
                border: none;
            }
        """)

        layout = QHBoxLayout(frame)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        # Crear cada celda del bloque
        for i in range(self.tamanio_bloque):
            celda = QFrame()
            celda_layout = QVBoxLayout(celda)
            celda_layout.setContentsMargins(0, 0, 0, 0)
            celda_layout.setSpacing(0)

            # Verificar si hay una clave en esta posición
            if i < len(bloque):
                # Celda ocupada
                celda.setStyleSheet("""
                    QFrame {
                        background-color: #E9D5FF;
                        border: 2px solid #A78BFA;
                        min-width: 50px;
                        max-width: 50px;
                        min-height: 50px;
                        max-height: 50px;
                    }
                """)
                label_clave = QLabel(str(bloque[i]))
                label_clave.setStyleSheet("font-size: 12px; font-weight: bold; color: #5B21B6;")
                label_clave.setAlignment(Qt.AlignCenter)
                celda_layout.addWidget(label_clave)
            else:
                # Celda vacía
                celda.setStyleSheet("""
                    QFrame {
                        background-color: #F3E8FF;
                        border: 2px solid #A78BFA;
                        min-width: 50px;
                        max-width: 50px;
                        min-height: 50px;
                        max-height: 50px;
                    }
                """)

            layout.addWidget(celda)

        container_layout.addWidget(frame)

        # Número del bloque debajo (centrado)
        num_bloque = QLabel(f"Bloque {indice + 1}")
        num_bloque.setStyleSheet("font-size: 11px; font-weight: bold; color: #6B7280;")
        num_bloque.setAlignment(Qt.AlignCenter)
        container_layout.addWidget(num_bloque)

        return container

    def insertar_clave(self):
        """Inserta una nueva clave en la estructura"""
        if not self.bloques:
            QMessageBox.warning(self, "Advertencia", "Primero debes crear la estructura.")
            return

        # Abrir diálogo para ingresar clave
        dlg = DialogoClave(self.digitos.value(), "Insertar clave", "insertar", self)
        if dlg.exec():
            clave = int(dlg.input.text())
            resultado = self.controller.insertar_clave(clave)

            if resultado["exito"]:
                # Actualizar visualización desde el controlador
                self.bloques = self.controller.bloques
                self.actualizar_visualizacion()

            QMessageBox.information(self, "Resultado", resultado["mensaje"])

    def guardar_estructura(self):
        """Guarda la estructura actual en un archivo JSON."""
        if not self.bloques:
            QMessageBox.warning(self, "Advertencia", "No hay estructura para guardar.")
            return

        # Pedir ruta para guardar
        ruta, _ = QFileDialog.getSaveFileName(
            self, "Guardar estructura", os.getcwd(), "Archivos JSON (*.json)"
        )

        if not ruta:
            return  # Cancelado por el usuario

        try:
            datos = self.controller.exportar_estructura()
            with open(ruta, 'w', encoding='utf-8') as f:
                json.dump(datos, f, indent=4)

            QMessageBox.information(self, "Éxito", f"Estructura guardada en:\n{ruta}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo guardar: {str(e)}")

    def cargar_estructura(self):
        """Carga una estructura guardada desde un archivo JSON."""
        ruta, _ = QFileDialog.getOpenFileName(
            self, "Cargar estructura", os.getcwd(), "Archivos JSON (*.json)"
        )

        if not ruta:
            return  # Cancelado por el usuario

        try:
            with open(ruta, 'r', encoding='utf-8') as f:
                datos = json.load(f)

            resultado = self.controller.importar_estructura(datos)

            if resultado["exito"]:
                self.bloques = self.controller.bloques
                self.num_claves = self.controller.num_claves
                self.tamanio_bloque = self.controller.tamanio_bloque
                self.actualizar_visualizacion()
                QMessageBox.information(self, "Éxito", resultado["mensaje"])
            else:
                QMessageBox.warning(self, "Advertencia", resultado["mensaje"])
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo cargar: {str(e)}")
    def eliminar_estructura(self):
        """Elimina la estructura actual"""
        if not self.bloques:
            QMessageBox.warning(self, "Advertencia", "No hay estructura para eliminar.")
            return

        respuesta = QMessageBox.question(
            self,
            "Confirmar eliminación",
            "¿Estás seguro de que deseas eliminar la estructura actual?",
            QMessageBox.Yes | QMessageBox.No
        )

        if respuesta == QMessageBox.Yes:
            self.bloques = []
            self.num_claves = 0
            self.tamanio_bloque = 0
            self.actualizar_visualizacion()
            QMessageBox.information(self, "Éxito", "Estructura eliminada correctamente.")

    def buscar_clave(self):
        """Buscar una clave existente"""
        dlg = DialogoClave(self.digitos.value(), "Buscar clave", "buscar", self)
        if dlg.exec():
            clave = int(dlg.input.text())
            resultado = self.controller.buscar_clave(clave)
            QMessageBox.information(self, "Resultado de búsqueda", resultado["mensaje"])

    def eliminar_clave(self):
        """Elimina una clave solicitándola por diálogo y actualiza la vista."""
        if not self.bloques:
            QMessageBox.warning(self, "Advertencia", "Primero debes crear la estructura.")
            return

        dlg = DialogoClave(self.digitos.value(), "Eliminar clave", "eliminar", self)
        if dlg.exec():
            try:
                clave = int(dlg.input.text())
            except Exception:
                QMessageBox.warning(self, "Error", "Clave inválida.")
                return

            resultado = self.controller.eliminar_clave(clave)

            # Si se eliminó, actualiza los bloques desde el controlador
            if resultado.get("exito"):
                self.bloques = self.controller.bloques
                # Ajustar num_claves/ tamaño_bloque si el controlador lo modificó
                self.num_claves = self.controller.num_claves
                self.tamanio_bloque = self.controller.tamanio_bloque
                self.actualizar_visualizacion()

            QMessageBox.information(self, "Resultado", resultado["mensaje"])

    def deshacer(self):
        """Deshace la última operación"""
        resultado = self.controller.deshacer()
        if resultado["exito"]:
            self.bloques = resultado["bloques"]
            self.actualizar_visualizacion()
        QMessageBox.information(self, "Deshacer", resultado["mensaje"])

    def eliminar_estructura(self):
        """Limpia toda la estructura"""
        respuesta = QMessageBox.question(
            self, "Confirmar", "¿Deseas eliminar la estructura?",
            QMessageBox.Yes | QMessageBox.No
        )
        if respuesta == QMessageBox.Yes:
            resultado = self.controller.limpiar_estructura()
            self.bloques = []
            self.actualizar_visualizacion()
            QMessageBox.information(self, "Estructura", resultado["mensaje"])

    def compactar_bloques(self):
        """Reacomoda las claves en los bloques para eliminar huecos (corrimiento a la izquierda)."""
        # Aplanar todos los valores en una sola lista
        todas = [x for bloque in self.bloques for x in bloque if x is not None]

        # Vaciar todos los bloques
        for bloque in self.bloques:
            bloque.clear()

        # Volver a llenarlos manteniendo el tamaño fijo por bloque
        idx = 0
        for bloque in self.bloques:
            for _ in range(self.tamanio_bloque):
                if idx < len(todas):
                    bloque.append(todas[idx])
                    idx += 1
                else:
                    bloque.append(None)
