from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel, QFrame,
    QComboBox, QSpinBox, QPushButton, QGridLayout, QScrollArea,
    QMessageBox, QHBoxLayout, QDialog, QFileDialog
)
from PySide6.QtCore import Qt
from .dialogo_clave import DialogoClave
from Controlador.Internas.lineal_controller import LinealController
from Modelo.manejador_archivos import ManejadorArchivos
from datetime import datetime
import os


class LinealInterna(QMainWindow):
    def __init__(self, cambiar_ventana):
        super().__init__()
        self.cambiar_ventana = cambiar_ventana
        self.controller = LinealController()

        self.setWindowTitle("Ciencias de la Computación II - Búsqueda Lineal")

        central = QWidget()
        layout = QVBoxLayout(central)
        layout.setSpacing(20)

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

        self.rango = QComboBox()
        # 👉 Mostrar solo los números (exponentes)
        self.rango.addItems([str(i) for i in range(1, 7)])  # 1 hasta 6
        self.rango.setFixedWidth(100)
        self.digitos = QSpinBox()
        self.digitos.setRange(1, 10)
        self.digitos.setValue(4)

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

        # En el constructor (init)
        controles = QVBoxLayout()

        fila_controles = QHBoxLayout()
        fila_controles.setSpacing(20)
        fila_controles.setAlignment(Qt.AlignCenter)

        lbl_rango = QLabel("Rango (10^n):")
        lbl_rango.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.rango.setStyleSheet("font-size: 16px; padding: 5px;")

        lbl_digitos = QLabel("Número de dígitos:")
        lbl_digitos.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.digitos.setFixedWidth(100)
        self.digitos.setStyleSheet("font-size: 16px; padding: 5px;")

        fila_controles.addWidget(lbl_rango)
        fila_controles.addWidget(self.rango)
        fila_controles.addWidget(lbl_digitos)
        fila_controles.addWidget(self.digitos)

        controles.addLayout(fila_controles)

        grid_botones = QGridLayout()
        grid_botones.addWidget(self.btn_crear, 0, 0)
        grid_botones.addWidget(self.btn_insertar, 0, 1)
        grid_botones.addWidget(self.btn_buscar_clave, 0, 2)
        grid_botones.addWidget(self.btn_eliminar_clave, 0, 3)
        grid_botones.addWidget(self.btn_deshacer, 1, 0)
        grid_botones.addWidget(self.btn_guardar, 1, 1)
        grid_botones.addWidget(self.btn_eliminar, 1, 2)
        grid_botones.addWidget(self.btn_cargar, 1, 3)

        controles.addLayout(grid_botones)
        layout.addLayout(controles)

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

        self.btn_crear.clicked.connect(self.crear_estructura)
        self.btn_insertar.clicked.connect(self.adicionar_claves)
        self.btn_guardar.clicked.connect(self.guardar_estructura)
        self.btn_cargar.clicked.connect(self.cargar_estructura)
        self.btn_eliminar.clicked.connect(self.eliminar_estructura)
        self.btn_deshacer.clicked.connect(self.deshacer_movimiento)
        self.btn_eliminar_clave.clicked.connect(self.eliminar_clave)
        self.btn_buscar_clave.clicked.connect(self.buscar_clave)

        self.filas_info = []
        self.labels = []
        self.indices_labels = []
        self.indices_reales = []
        self.capacidad = 0
        self.historial = []

    def crear_estructura(self):
        self._limpiar_vista()

        # 👉 Tomar el exponente seleccionado y calcular 10^n
        n = int(self.rango.currentText())
        capacidad = 10 ** n

        self.controller.crear_estructura(capacidad, self.digitos.value())
        self.controller.guardar()
        self.capacidad = capacidad

        self._reconstruir_vista()

        # 🔒 Bloquear rango y dígitos
        self.rango.setEnabled(False)
        self.digitos.setEnabled(False)

    def _limpiar_vista(self):
        while self.contenedor_layout.count():
            item = self.contenedor_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self.filas_info.clear()
        self.labels.clear()
        self.indices_labels.clear()
        self.indices_reales.clear()

    def _reconstruir_vista(self):
        self._limpiar_vista()

        if self.capacidad <= 10:
            self._crear_fila(0, self.capacidad, completa=True)
            return

        total_ocupadas = sum(
            1 for i in range(self.capacidad)
            if self.controller.estructura.get(i, "") != ""
        )

        if total_ocupadas <= 8:
            self._crear_fila(0, 8, completa=False)
        else:
            self._crear_fila(0, 10, completa=True)

            if total_ocupadas <= 18:
                self._crear_fila(10, 8, completa=False)
            else:
                self._crear_fila(10, 10, completa=True)

                if total_ocupadas <= 28:
                    self._crear_fila(20, 8, completa=False)
                else:
                    fila_actual = 20
                    while fila_actual < self.capacidad:
                        ocupadas_hasta_aqui = sum(
                            1 for i in range(fila_actual + 10)
                            if self.controller.estructura.get(i, "") != ""
                        )
                        if ocupadas_hasta_aqui <= fila_actual + 8:
                            self._crear_fila(fila_actual, 8, completa=False)
                            break
                        else:
                            self._crear_fila(fila_actual, 10, completa=True)
                            fila_actual += 10

    def _crear_fila(self, inicio, cantidad, completa):
        fila_container = QWidget()
        fila_container.setStyleSheet("background: transparent;")
        fila_layout = QHBoxLayout(fila_container)
        fila_layout.setSpacing(0)
        fila_layout.setContentsMargins(0, 0, 0, 0)

        # 📌 Antes estaba AlignLeft → cambiamos a centrado
        fila_layout.setAlignment(Qt.AlignHCenter)

        if completa:
            for i in range(cantidad):
                idx_real = inicio + i
                if idx_real < self.capacidad:
                    self._agregar_bloque(fila_layout, idx_real)
        else:
            for i in range(cantidad):
                idx_real = inicio + i
                if idx_real < self.capacidad:
                    self._agregar_bloque(fila_layout, idx_real)

            self._agregar_bloque_especial(fila_layout, "...", "...")
            self._agregar_bloque(fila_layout, self.capacidad - 1)

        fila_layout.addStretch()

        self.contenedor_layout.addWidget(
            fila_container, 0, Qt.AlignHCenter
        )
        self.filas_info.append({
            'widget': fila_container,
            'inicio': inicio,
            'cantidad': cantidad,
            'completa': completa
        })

    def _agregar_bloque(self, layout, idx_real):
        contenedor = QWidget()
        contenedor.setFixedWidth(80)
        layout_vert = QVBoxLayout(contenedor)
        layout_vert.setSpacing(2)
        layout_vert.setContentsMargins(0, 0, 0, 0)

        cuadro = QLabel("")
        cuadro.setAlignment(Qt.AlignCenter)
        cuadro.setFixedSize(80, 80)
        cuadro.setStyleSheet("""
            QLabel {
                background-color: #EDE9FE;
                border: 2px solid #7C3AED;
                font-size: 16px;
            }
        """)

        numero = QLabel(str(idx_real + 1))
        numero.setAlignment(Qt.AlignCenter)
        numero.setFixedHeight(20)
        numero.setStyleSheet("font-size: 12px; color: gray; background: transparent;")

        layout_vert.addWidget(cuadro)
        layout_vert.addWidget(numero)

        layout.addWidget(contenedor)
        self.labels.append(cuadro)
        self.indices_labels.append(numero)
        self.indices_reales.append(idx_real)

    def _agregar_bloque_especial(self, layout, texto_valor, texto_indice):
        contenedor = QWidget()
        contenedor.setFixedWidth(80)
        layout_vert = QVBoxLayout(contenedor)
        layout_vert.setSpacing(2)
        layout_vert.setContentsMargins(0, 0, 0, 0)

        cuadro = QLabel(texto_valor)
        cuadro.setAlignment(Qt.AlignCenter)
        cuadro.setFixedSize(80, 80)
        cuadro.setStyleSheet("""
            QLabel {
                background-color: #F3F4F6;
                border: 2px solid #9CA3AF;
                font-size: 24px;
                color: #6B7280;
            }
        """)

        numero = QLabel(texto_indice)
        numero.setAlignment(Qt.AlignCenter)
        numero.setFixedHeight(20)
        numero.setStyleSheet("font-size: 12px; color: gray; background: transparent;")

        layout_vert.addWidget(cuadro)
        layout_vert.addWidget(numero)

        layout.addWidget(contenedor)
        self.labels.append(cuadro)
        self.indices_labels.append(numero)
        self.indices_reales.append(-1)

    def adicionar_claves(self):
        if not self.labels:
            self._mostrar_mensaje("Error", "Primero debe crear la estructura.")
            return

        # 👉 Usar el diálogo morado
        dlg = DialogoClave(
            self.digitos.value(),
            titulo="Insertar clave",
            modo="insertar",
            parent=self
        )
        if not dlg.exec():
            return

        clave = dlg.get_clave()
        if not clave.isdigit():
            self._mostrar_mensaje("Error", "La clave debe ser numérica.")
            return

        if len(clave) != self.digitos.value():
            self._mostrar_mensaje("Error", f"La clave debe tener {self.digitos.value()} dígitos.")
            return

        estado = self.controller.adicionar_clave(clave)

        if estado == "OK":
            self.historial.append(("insertar", clave))
            self._reconstruir_vista()
            self._repintar()
            self._mostrar_mensaje("Éxito", f"La clave {clave} fue insertada correctamente.")
        elif estado == "REPETIDA":
            self._mostrar_mensaje("Clave duplicada", f"La clave {clave} ya fue insertada.")
        elif estado == "LLENO":
            self._mostrar_mensaje("Sin espacio", "No hay más espacios disponibles.")
        elif estado == "LONGITUD":
            self._mostrar_mensaje("Error", f"La clave debe tener {self.digitos.value()} dígitos.")

    def _repintar(self):
        for i, idx_real in enumerate(self.indices_reales):
            if idx_real == -1:
                continue

            lbl = self.labels[i]
            idx_lbl = self.indices_labels[i]

            val = str(self.controller.estructura.get(idx_real, ""))

            if val:
                lbl.setText(val)
                lbl.setStyleSheet("""
                    QLabel {
                        background-color: #C4B5FD;
                        border: 2px solid #6D28D9;
                        font-size: 16px;
                        font-weight: bold;
                    }
                """)
            else:
                lbl.setText("")
                lbl.setStyleSheet("""
                    QLabel {
                        background-color: #EDE9FE;
                        border: 2px solid #7C3AED;
                        font-size: 16px;
                    }
                """)

            idx_lbl.setText(str(idx_real + 1))

    def buscar_clave(self):
        if not self.labels:
            self._mostrar_mensaje("Error", "Primero debe crear o cargar la estructura.")
            return

        dlg = DialogoClave(
            self.digitos.value(),
            titulo="Buscar clave",
            modo="buscar",
            parent=self
        )
        if not dlg.exec():
            return

        clave = dlg.clave()
        if not clave:
            return

        idx = self.controller.buscar_clave(clave)
        if idx == -1:
            self._mostrar_mensaje("No encontrada", f"La clave {clave} no existe en la estructura.")
            return

        try:
            pos_label = self.indices_reales.index(idx)
            self._reset_label_styles()
            self.labels[pos_label].setStyleSheet("""
                QLabel {
                    background-color: #D8B4FE;
                    border: 3px solid #7C3AED;
                    font-size: 18px;
                    font-weight: bold;
                }
            """)
            self._mostrar_mensaje("Resultado", f"La clave {clave} está en la posición {idx + 1}.")
        except ValueError:
            self._mostrar_mensaje(
                "Encontrada (no visible)",
                f"La clave {clave} está en la posición {idx + 1}, pero no es visible actualmente."
            )

    def eliminar_clave(self):
        if not self.labels:
            self._mostrar_mensaje("Error", "Primero debe crear la estructura.")
            return

        dlg = DialogoClave(
            self.digitos.value(),
            titulo="Eliminar clave",
            modo="eliminar",
            parent=self
        )
        if not dlg.exec():
            return

        clave = dlg.get_clave()
        if not clave:
            return

        eliminado = self.controller.eliminar_clave(clave)
        if eliminado:
            self.historial.append(("eliminar", clave))  # ✅ registrar eliminación


            # 🔹 Primero mensaje de éxito
            self._mostrar_mensaje("Éxito", f"Clave {clave} eliminada.")

            # 🔹 Luego reconstruir y repintar
            self._reconstruir_vista()
            self._repintar()
        else:
            self._mostrar_mensaje("Error", f"La clave {clave} no existe.")

    def deshacer_movimiento(self):
        if not self.historial:
            self._mostrar_mensaje("Nada que deshacer", "No hay movimientos previos.")
            return

        movimiento = self.historial.pop()

        # 🧩 compatibilidad con versiones viejas
        if isinstance(movimiento, tuple) and len(movimiento) == 2:
            tipo, clave = movimiento
        else:
            tipo, clave = "insertar", movimiento  # asumir que era una inserción

        if tipo == "insertar":
            exito = self.controller.eliminar_clave(clave)
            if exito:
                self.historial.append(("eliminar", clave))
                self._reconstruir_vista()
                self._repintar()
                self._mostrar_mensaje("Deshacer", f"Se eliminó la clave {clave}.")
            else:
                self._mostrar_mensaje("Error", f"No se pudo eliminar la clave {clave} al deshacer.")
        elif tipo == "eliminar":
            resultado = self.controller.agregar_clave(clave)
            if resultado == "OK":
                self.historial.append(("insertar", clave))
                self._reconstruir_vista()
                self._repintar()
                self._mostrar_mensaje("Deshacer", f"Se restauró la clave {clave}.")
            else:
                self._mostrar_mensaje("Error", f"No se pudo restaurar la clave {clave}: {resultado}.")

    def eliminar_estructura(self):
        """Elimina la estructura actual solo en memoria y en la vista (no el archivo)."""
        try:
            # Confirmación opcional
            if not self._mostrar_confirmacion(
                    "Confirmar eliminación",
                    "⚠️ Cuidado: estás a punto de eliminar la estructura visual.\n\n¿Deseas continuar?"
            ):
                return

            # Resetear datos en memoria
            self.controller.estructura = {}
            self.controller.capacidad = 0
            self.controller.digitos = 0

            # Limpiar la vista
            self._limpiar_vista()
            self._repintar()
            self.labels = []
            self.capacidad = 0

            # Reactivar controles si los tenías deshabilitados
            self.rango.setEnabled(True)
            self.digitos.setEnabled(True)

            self._mostrar_mensaje("Éxito", "La estructura visual fue eliminada correctamente.")
        except Exception as e:
            self._mostrar_mensaje("Error", f"No se pudo eliminar la estructura:\n{e}")

    def guardar_estructura(self):
        try:
            capacidad = self.capacidad or 0
            digitos = self.digitos.value()
            tabla = {k: v for k, v in self.controller.estructura.items() if v}
            if capacidad == 0:
                capacidad = len(tabla)
            datos = {
                "rango": self.rango.currentText(),
                "digitos": digitos,
                "capacidad": capacidad,
                "claves": tabla
            }
            default_name = f"busqueda_lineal_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            ruta, _ = QFileDialog.getSaveFileName(
                self, "Guardar estructura como", default_name, "JSON (*.json)"
            )
            if not ruta:
                return
            if not ruta.lower().endswith(".json"):
                ruta += ".json"
            ManejadorArchivos.guardar_json(ruta, datos)
            self._mostrar_mensaje("Éxito", f"Estructura guardada en:\n{ruta}")
        except Exception as e:
            self._mostrar_mensaje("Error", f"No se pudo guardar la estructura:\n{e}")

    def cargar_estructura(self):
        try:
            if self.labels or self.capacidad:
                if not self._mostrar_confirmacion(
                        "Confirmar carga",
                        "Ya existe una estructura cargada.\nSi continúas, será sobreescrita.\n\n¿Deseas continuar?"
                ):
                    return

            archivo, _ = QFileDialog.getOpenFileName(
                self, "Seleccionar archivo JSON", "", "JSON (*.json)"
            )
            if not archivo:
                return

            datos = ManejadorArchivos.leer_json(archivo)
            if not datos:
                self._mostrar_mensaje("Error", "Archivo inválido o vacío.")
                return

            rango = datos.get("rango")
            digitos = datos.get("digitos", self.digitos.value())
            capacidad = datos.get("capacidad", 0)
            claves = datos.get("claves", {})

            self.controller.crear_estructura(capacidad, digitos)

            if isinstance(claves, dict):
                for k, v in claves.items():
                    idx = int(k)
                    if v:
                        self.controller.estructura[idx] = str(v)

            self.controller.guardar()
            self.capacidad = capacidad

            if rango:
                idx_combo = self.rango.findText(rango)
                if idx_combo != -1:
                    self.rango.setCurrentIndex(idx_combo)
            self.digitos.setValue(digitos)

            self._reconstruir_vista()
            self._repintar()

            self._mostrar_mensaje("Éxito", "Estructura cargada correctamente")
        except Exception as e:
            self._mostrar_mensaje("Error", f"No se pudo cargar la estructura:\n{e}")

    def _reset_label_styles(self):
        for i, lbl in enumerate(self.labels):
            if self.indices_reales[i] == -1:
                continue
            text = lbl.text()
            if text:
                lbl.setStyleSheet("""
                    QLabel {
                        background-color: #C4B5FD;
                        border: 2px solid #6D28D9;
                        font-size: 16px;
                        font-weight: bold;
                    }
                """)
            else:
                lbl.setStyleSheet("""
                    QLabel {
                        background-color: #EDE9FE;
                        border: 2px solid #7C3AED;
                        font-size: 16px;
                    }
                """)

    def _mostrar_mensaje(self, titulo, texto):
        dlg = DialogoClave(
            longitud=0,
            titulo=titulo,
            modo="mensaje",
            parent=self,
            mensaje=texto
        )
        dlg.exec()

    def _mostrar_confirmacion(self, titulo, texto):
        dlg = DialogoClave(0, titulo, modo="confirmar", parent=self, mensaje=texto)
        return dlg.exec() == QDialog.Accepted

