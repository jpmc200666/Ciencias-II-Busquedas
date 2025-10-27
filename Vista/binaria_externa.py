from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel, QFrame,
    QComboBox, QSpinBox, QPushButton, QGridLayout, QScrollArea,
    QMessageBox, QHBoxLayout, QFileDialog
)
from PySide6.QtCore import Qt
import os, json
from Vista.dialogo_clave import DialogoClave
from Controlador.Externas.BinariaController import BinariaController


class BinariaExterna(QMainWindow):
    def __init__(self, cambiar_ventana):
        super().__init__()
        self.cambiar_ventana = cambiar_ventana
        self.controller = BinariaController()

        self.bloques = []
        self.num_claves = 0
        self.tamanio_bloque = 0

        self.setWindowTitle("Ciencias de la Computación II - Búsqueda Binaria Externa")

        # ================== LAYOUT PRINCIPAL ==================
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

        titulo = QLabel("Ciencias de la Computación II - Búsqueda Binaria Externa")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("font-size: 26px; font-weight: bold; color: white; margin: 10px;")
        header_layout.addWidget(titulo)

        menu_layout = QHBoxLayout()
        menu_layout.setSpacing(40)
        menu_layout.setAlignment(Qt.AlignCenter)

        btn_inicio = QPushButton("Inicio")
        btn_busqueda = QPushButton("Menú de Búsqueda")

        for btn in (btn_inicio, btn_busqueda):
            btn.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    color: white;
                    font-size: 16px;
                    font-weight: bold;
                    border: none;
                }
                QPushButton:hover {
                    color: #E0E7FF;
                    text-decoration: underline;
                }
            """)
            menu_layout.addWidget(btn)

        btn_inicio.clicked.connect(lambda: self.cambiar_ventana("inicio"))
        btn_busqueda.clicked.connect(lambda: self.cambiar_ventana("busqueda"))
        header_layout.addLayout(menu_layout)
        layout.addWidget(header)

        # ======= CONTROLES SUPERIORES =======
        fila_controles = QHBoxLayout()
        fila_controles.setSpacing(20)
        fila_controles.setAlignment(Qt.AlignCenter)

        lbl_claves = QLabel("Número de claves (N):")
        lbl_digitos = QLabel("Número de dígitos:")

        for lbl in (lbl_claves, lbl_digitos):
            lbl.setStyleSheet("font-size: 16px; font-weight: bold;")

        self.num_claves_input = QSpinBox()
        self.num_claves_input.setRange(2, 100)
        self.num_claves_input.setValue(10)
        self.num_claves_input.setFixedWidth(100)

        self.digitos = QSpinBox()
        self.digitos.setRange(1, 10)
        self.digitos.setValue(4)
        self.digitos.setFixedWidth(100)

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

        # ======= VISUALIZACIÓN =======
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

        # ======= CONEXIONES =======
        self.btn_crear.clicked.connect(self.crear_estructura)
        self.btn_insertar.clicked.connect(self.insertar_clave)
        self.btn_guardar.clicked.connect(self.guardar_estructura)
        self.btn_cargar.clicked.connect(self.cargar_estructura)
        self.btn_eliminar.clicked.connect(self.eliminar_estructura)
        self.btn_deshacer.clicked.connect(self.deshacer)
        self.btn_eliminar_clave.clicked.connect(self.eliminar_clave)
        self.btn_buscar_clave.clicked.connect(self.buscar_clave)

    # ================== FUNCIONALIDAD ==================

    def crear_estructura(self):
        """Crea la estructura inicial desde el controlador."""
        try:
            num_claves = self.num_claves_input.value()
            datos = self.controller.crear_estructura(num_claves)
            self.bloques = datos['bloques']
            self.num_claves = datos['num_claves']
            self.tamanio_bloque = datos['tamanio_bloque']
            self.actualizar_visualizacion()

            QMessageBox.information(self, "Estructura Creada",
                                    f"Estructura creada exitosamente:\n\n"
                                    f"• N (claves totales): {self.num_claves}\n"
                                    f"• B (tamaño de bloque): {self.tamanio_bloque}\n"
                                    f"• Bloques: {len(self.bloques)}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo crear la estructura:\n{str(e)}")

    def actualizar_visualizacion(self):
        """Dibuja los bloques igual que en la versión lineal."""
        while self.contenedor_layout.count():
            child = self.contenedor_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        if not self.bloques:
            label = QLabel("No hay estructura creada.")
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet("font-size: 16px; color: #6B7280; padding: 40px;")
            self.contenedor_layout.addWidget(label)
            return

        info_label = QLabel(
            f"Estructura binaria externa | Claves: {self.num_claves} | "
            f"Tamaño de bloque: {self.tamanio_bloque} | Bloques: {len(self.bloques)}"
        )
        info_label.setAlignment(Qt.AlignCenter)
        info_label.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #7C3AED;
            background-color: #F3E8FF;
            padding: 10px;
            border-radius: 8px;
            margin-bottom: 20px;
        """)
        self.contenedor_layout.addWidget(info_label)

        bloques_container = QWidget()
        bloques_layout = QHBoxLayout(bloques_container)
        bloques_layout.setSpacing(30)
        bloques_layout.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        bloques_layout.setContentsMargins(20, 20, 20, 20)

        for i, bloque in enumerate(self.bloques):
            bloque_widget = self.crear_bloque_visual(i, bloque)
            bloques_layout.addWidget(bloque_widget)

        bloques_layout.addStretch()
        self.contenedor_layout.addWidget(bloques_container)

    def crear_bloque_visual(self, indice, bloque):
        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.setSpacing(3)
        container_layout.setContentsMargins(0, 0, 0, 0)

        frame = QFrame()
        layout = QHBoxLayout(frame)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        for i in range(self.tamanio_bloque):
            celda = QFrame()
            celda_layout = QVBoxLayout(celda)
            celda_layout.setContentsMargins(0, 0, 0, 0)

            if i < len(bloque):
                celda.setStyleSheet("""
                    QFrame {
                        background-color: #E9D5FF;
                        border: 2px solid #A78BFA;
                        min-width: 50px; max-width: 50px;
                        min-height: 50px; max-height: 50px;
                    }
                """)
                label_clave = QLabel(str(bloque[i]))
                label_clave.setAlignment(Qt.AlignCenter)
                label_clave.setStyleSheet("font-size: 12px; font-weight: bold; color: #5B21B6;")
                celda_layout.addWidget(label_clave)
            else:
                celda.setStyleSheet("""
                    QFrame {
                        background-color: #F3E8FF;
                        border: 2px solid #A78BFA;
                        min-width: 50px; max-width: 50px;
                        min-height: 50px; max-height: 50px;
                    }
                """)

            layout.addWidget(celda)

        container_layout.addWidget(frame)

        num_bloque = QLabel(f"Bloque {indice + 1}")
        num_bloque.setAlignment(Qt.AlignCenter)
        num_bloque.setStyleSheet("font-size: 11px; font-weight: bold; color: #6B7280;")
        container_layout.addWidget(num_bloque)

        return container

    def insertar_clave(self):
        """Inserta una nueva clave"""
        dlg = DialogoClave(self.digitos.value(), "Insertar clave", "insertar", self)
        if dlg.exec():
            clave = dlg.input.text().zfill(self.digitos.value())
            resultado = self.controller.insertar_clave(clave)
            self.bloques = self.controller.bloques
            self.actualizar_visualizacion()
            QMessageBox.information(self, "Resultado", resultado["mensaje"])
    def eliminar_clave(self):
        """Elimina una clave y reacomoda los bloques"""
        dlg = DialogoClave(self.digitos.value(), "Eliminar clave", "eliminar", self)
        if dlg.exec():
            clave = dlg.input.text().zfill(self.digitos.value())
            resultado = self.controller.eliminar_clave(clave)
            self.bloques = self.controller.bloques
            self.actualizar_visualizacion()
            QMessageBox.information(self, "Resultado", resultado["mensaje"])

    def buscar_clave(self):
        """Busca una clave en la estructura"""
        dlg = DialogoClave(self.digitos.value(), "Buscar clave", "buscar", self)
        if dlg.exec():
            clave = dlg.input.text().zfill(self.digitos.value())
            bloques = self.controller.obtener_bloques()
            encontrado = False
            for i, bloque in enumerate(bloques):
                if clave in bloque:
                    QMessageBox.information(self, "Resultado",
                                            f"Clave {clave} encontrada en el bloque {i + 1}.")
                    encontrado = True
                    break
            if not encontrado:
                QMessageBox.warning(self, "Resultado",
                                    f"La clave {clave} no se encuentra en la estructura.")

    def guardar_estructura(self):
        """Guarda la estructura actual en un archivo JSON"""
        archivo, _ = QFileDialog.getSaveFileName(self, "Guardar estructura", "", "Archivos JSON (*.json)")
        if not archivo:
            return
        try:
            datos = {
                "bloques": self.bloques,
                "num_claves": self.num_claves,
                "tamanio_bloque": self.tamanio_bloque
            }
            with open(archivo, "w", encoding="utf-8") as f:
                json.dump(datos, f, indent=4)
            QMessageBox.information(self, "Guardado exitoso", "Estructura guardada correctamente.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo guardar la estructura:\n{str(e)}")

    def cargar_estructura(self):
        """Carga una estructura desde un archivo JSON"""
        archivo, _ = QFileDialog.getOpenFileName(self, "Cargar estructura", "", "Archivos JSON (*.json)")
        if not archivo:
            return
        try:
            with open(archivo, "r", encoding="utf-8") as f:
                datos = json.load(f)
            self.bloques = datos["bloques"]
            self.num_claves = datos["num_claves"]
            self.tamanio_bloque = datos["tamanio_bloque"]
            self.actualizar_visualizacion()
            QMessageBox.information(self, "Carga exitosa", "Estructura cargada correctamente.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo cargar la estructura:\n{str(e)}")

    def eliminar_estructura(self):
        """Elimina toda la estructura actual"""
        respuesta = QMessageBox.question(
            self, "Confirmar eliminación",
            "¿Deseas eliminar toda la estructura?",
            QMessageBox.Yes | QMessageBox.No
        )
        if respuesta == QMessageBox.Yes:
            self.controller.bloques = []
            self.bloques = []
            self.num_claves = 0
            self.tamanio_bloque = 0
            self.actualizar_visualizacion()
            QMessageBox.information(self, "Estructura eliminada", "La estructura fue eliminada correctamente.")

    def deshacer(self):
        """Deshace el último movimiento si el controlador lo soporta"""
        if hasattr(self.controller, "historial") and self.controller.historial:
            self.controller.bloques = self.controller.historial.pop()
            self.bloques = self.controller.bloques
            self.actualizar_visualizacion()
            QMessageBox.information(self, "Deshacer", "Último movimiento revertido.")
        else:
            QMessageBox.warning(self, "Deshacer", "No hay acciones para deshacer.")
