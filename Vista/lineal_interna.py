from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel, QFrame,
    QComboBox, QSpinBox, QPushButton, QGridLayout, QScrollArea,
    QMessageBox, QHBoxLayout, QInputDialog, QFileDialog
)
from PySide6.QtCore import Qt
from .dialogo_clave import DialogoClave  # diálogo para ingresar clave
from Controlador.Internas.lineal_controller import LinealController
from Modelo.manejador_archivos import ManejadorArchivos
from datetime import datetime


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

        controles = QVBoxLayout()
        controles.addWidget(QLabel("Rango (10^n):"))
        controles.addWidget(self.rango)
        controles.addWidget(QLabel("Número de dígitos de la clave:"))
        controles.addWidget(self.digitos)

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
        self.btn_insertar.clicked.connect(self.adicionar_claves)
        self.btn_guardar.clicked.connect(self.guardar_estructura)
        self.btn_cargar.clicked.connect(self.cargar_estructura)
        self.btn_eliminar.clicked.connect(self.eliminar_estructura)
        self.btn_deshacer.clicked.connect(self.deshacer_movimiento)
        self.btn_eliminar_clave.clicked.connect(self.eliminar_clave)
        self.btn_buscar_clave.clicked.connect(self.buscar_clave)

        # Estado
        self.labels = []
        self.capacidad = 0
        self.historial = []

    # ========================
    # Métodos de funcionalidad
    # ========================

    def cargar_estructura(self):
        """Abrir un JSON guardado y reconstruir la vista."""
        try:
            if self.labels or self.capacidad:
                respuesta = QMessageBox.question(
                    self, "Confirmar carga",
                    "Ya existe una estructura cargada.\n"
                    "Si continúas, será sobreescrita.\n\n¿Deseas continuar?",
                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No
                )
                if respuesta == QMessageBox.No:
                    return

            archivo, _ = QFileDialog.getOpenFileName(
                self, "Seleccionar archivo JSON", "", "JSON (*.json)"
            )
            if not archivo:
                return

            datos = ManejadorArchivos.leer_json(archivo)
            if not datos:
                QMessageBox.warning(self, "Error", "Archivo inválido o vacío.")
                return

            rango = datos.get("rango")
            digitos = datos.get("digitos", self.digitos.value())
            capacidad = datos.get("capacidad", len(datos.get("claves", [])))
            claves = datos.get("claves", [])

            # ----------------------------
            # SINCRONIZAR controller con lo cargado
            # ----------------------------
            # Asegurarnos de que el controller tenga la misma capacidad y digitos
            self.controller.crear_estructura(capacidad, digitos)

            # Normalizar 'claves' a una lista de longitud 'capacidad'
            if isinstance(claves, dict):
                # si viene como dict 1-based -> convertir a lista 0-based
                max_idx = max((int(k) for k in claves.keys()), default=0)
                capacidad = max(capacidad, max_idx)
                lista = [""] * capacidad
                for k, v in claves.items():
                    idx = int(k) - 1
                    if 0 <= idx < capacidad:
                        lista[idx] = str(v) if v is not None else ""
                claves = lista
            else:
                # aseguramos longitud mínima
                claves = [str(x) if x is not None else "" for x in claves]
                if len(claves) < capacidad:
                    claves += [""] * (capacidad - len(claves))

            # Cargar valores en el controller (índices 0..capacidad-1)
            nueva = {i: (claves[i] if i < len(claves) else "") for i in range(capacidad)}
            self.controller.estructura = nueva
            self.controller.capacidad = capacidad
            self.controller.digitos = digitos
            # opcional: guardar estado en archivo del controller
            self.controller.guardar()
            # ----------------------------

            # limpiar grilla
            for i in reversed(range(self.grid.count())):
                widget = self.grid.itemAt(i).widget()
                if widget:
                    widget.setParent(None)
            self.labels.clear()

            self.capacidad = capacidad
            if rango:
                idx = self.rango.findText(rango)
                if idx != -1:
                    self.rango.setCurrentIndex(idx)
            self.digitos.setValue(digitos)

            if capacidad > 1000:
                # Guardamos como atributos para que otros helpers los usen
                self.mostrar_inicio = 50
                self.mostrar_final = 50

                # Mostrar primeros cuadros (visual indices 0..mostrar_inicio-1)
                for i in range(self.mostrar_inicio):
                    self._agregar_cuadro(i, i)

                # Puntos suspensivos en la rejilla
                puntos = QLabel("...")
                puntos.setStyleSheet("font-size: 18px; color: gray;")
                self.grid.addWidget(
                    puntos,
                    (self.mostrar_inicio // 10) * 2,
                    self.mostrar_inicio % 10,
                    2, 1,
                    alignment=Qt.AlignCenter
                )

                # Mostrar últimos cuadros (visual indices self.mostrar_inicio .. self.mostrar_inicio+mostrar_final-1)
                for i in range(self.mostrar_final):
                    idx_real = capacidad - self.mostrar_final + i
                    self._agregar_cuadro(self.mostrar_inicio + i, idx_real)

            else:
                for i in range(capacidad):
                    self._agregar_cuadro(i, i)

            for i, lbl in enumerate(self.labels):
                if i < len(claves) and claves[i]:
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
            QMessageBox.information(self, "Éxito", "Estructura cargada correctamente")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo cargar la estructura:\n{e}")

    def crear_estructura(self):
        # limpiar
        for i in reversed(range(self.grid.count())):
            widget = self.grid.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        self.labels.clear()

        n = int(self.rango.currentText().split("^")[1])
        capacidad = 10 ** n
        self.controller.crear_estructura(capacidad, self.digitos.value())
        self.controller.guardar()
        self.capacidad = capacidad

        if capacidad > 1000:
            QMessageBox.information(
                self, "Vista representativa",
                f"La capacidad real es {capacidad}, pero se muestra parcial."
            )
            mostrar_inicio, mostrar_final = 50, 50
            for i in range(mostrar_inicio):
                self._agregar_cuadro(i, i)
            puntos = QLabel("...")
            puntos.setStyleSheet("font-size: 18px; color: gray;")
            self.grid.addWidget(puntos, (mostrar_inicio // 10) * 2,
                                mostrar_inicio % 10, 2, 1, alignment=Qt.AlignCenter)
            for i in range(mostrar_final):
                idx_real = capacidad - mostrar_final + i
                self._agregar_cuadro(mostrar_inicio + i + 1, idx_real)
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
        if not self.labels:
            QMessageBox.warning(self, "Error", "Primero debe crear la estructura.")
            return

        dlg = DialogoClave(self.digitos.value(), self)
        if dlg.exec():
            clave = dlg.get_clave()
            if not clave.isdigit():
                QMessageBox.warning(self, "Error", "La clave debe ser numérica.")
                return
            if len(clave) != self.digitos.value():
                QMessageBox.warning(self, "Error", f"La clave debe tener {self.digitos.value()} dígitos.")
                return

            estado = self.controller.adicionar_clave(clave)
            if estado == "OK":
                self.historial.append(clave)
                self._repintar()
            elif estado == "REPETIDA":
                QMessageBox.warning(self, "Clave duplicada", f"La clave {clave} ya fue insertada.")
            elif estado == "LLENO":
                QMessageBox.information(self, "Sin espacio", "No hay más espacios disponibles.")
            elif estado == "LONGITUD":
                QMessageBox.warning(self, "Error", f"La clave debe tener {self.digitos.value()} dígitos.")

    def eliminar_estructura(self):
        try:
            if not self.labels:
                QMessageBox.information(self, "Sin estructura", "No hay estructura para eliminar.")
                return
            respuesta = QMessageBox.question(
                self, "Confirmar eliminación",
                "¿Estás seguro de eliminar la estructura?",
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No
            )
            if respuesta == QMessageBox.No:
                return
            for i in reversed(range(self.grid.count())):
                widget = self.grid.itemAt(i).widget()
                if widget:
                    widget.setParent(None)
            self.labels.clear()
            self.capacidad = 0
            self.rango.setCurrentIndex(0)
            self.digitos.setValue(4)
            QMessageBox.information(self, "Estructura eliminada", "Estructura eliminada con éxito.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo eliminar la estructura:\n{e}")

    def guardar_estructura(self):
        try:
            capacidad = self.capacidad or 0
            digitos = self.digitos.value()
            tabla = [lbl.text() if lbl.text() else "" for lbl in self.labels]
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
            QMessageBox.information(self, "Éxito", f"Estructura guardada en:\n{ruta}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo guardar la estructura:\n{e}")

    def deshacer_movimiento(self):
        if not self.historial:
            QMessageBox.information(self, "Nada que deshacer", "No hay movimientos previos.")
            return
        ultima_clave = self.historial.pop()
        eliminado = self.controller.eliminar_clave(ultima_clave)
        if not eliminado:
            QMessageBox.warning(self, "Error", f"No se pudo deshacer la clave {ultima_clave}.")
            return
        self._repintar()
        QMessageBox.information(self, "Deshacer", f"Se eliminó la clave {ultima_clave}.")

    def eliminar_clave(self):
        if not self.labels:
            QMessageBox.warning(self, "Error", "Primero debe crear la estructura.")
            return

        clave, ok = QInputDialog.getText(self, "Eliminar clave", "Ingrese la clave a eliminar:")
        if not ok or not clave:
            return

        eliminado = self.controller.eliminar_clave(clave)
        if eliminado:
            # si existía, actualizar vista y también historial si corresponde
            try:
                # quitar de historial si estaba
                self.historial.remove(clave)
            except ValueError:
                pass

            self._repintar()
            QMessageBox.information(self, "Éxito", f"Clave {clave} eliminada.")
        else:
            QMessageBox.warning(self, "Error", f"La clave {clave} no existe.")

    def buscar_clave(self):
        if not self.labels:
            QMessageBox.warning(self, "Error", "Primero debe crear o cargar la estructura.")
            return

        clave, ok = QInputDialog.getText(self, "Buscar clave", "Ingrese la clave a buscar:")
        if not ok or not clave:
            return

        # pedir índice real (0-based) al controller
        idx = self.controller.buscar_clave(clave)  # debe devolver 0-based o -1

        if idx == -1:
            QMessageBox.warning(self, "No encontrada", f"La clave {clave} no existe en la estructura.")
            return

        # mapear ese índice real a la posición en labels (si está visible)
        label_pos = self._map_index_to_label(idx)
        if label_pos is None:
            # existe en la estructura pero no está en la porción visible
            QMessageBox.information(
                self, "Encontrada (no visible)",
                f"La clave {clave} está en la posición {idx + 1}, pero no es visible en la representación actual."
            )
            return

        # limpiar resaltados previos y luego resaltar en morado
        self._reset_label_styles()
        highlight_style = """
            QLabel {
                background-color: #D8B4FE;  /* morado claro */
                border: 3px solid #7C3AED;  /* morado oscuro */
                border-radius: 12px;
                font-size: 18px;
                font-weight: bold;
            }
        """
        self.labels[label_pos].setStyleSheet(highlight_style)

        # mostrar posición 1-based al usuario
        QMessageBox.information(self, "Resultado", f"La clave {clave} está en la posición {idx + 1}.")

    def _repintar(self):
        """
        Pinta la vista *según la estructura real* del controller.
        Esto evita inconsistencias entre lo que busca el controller y lo que muestra la UI.
        """
        # indices reales que corresponden a cada label visible
        visibles = self._get_visible_indices()

        for pos_label, idx_real in enumerate(visibles):
            lbl = self.labels[pos_label]
            val = str(self.controller.estructura.get(idx_real, "") if self.controller.estructura is not None else "")
            if val:
                lbl.setText(val)
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

    def _get_visible_indices(self):
        """
        Devuelve la lista de índices reales (0-based) de la estructura que están
        representados por self.labels (en orden). Useful para repintar.
        """
        if self.capacidad <= 1000:
            return list(range(self.capacidad))
        # misma lógica que usas para mostrar: primeros mostrar_inicio y últimos mostrar_final
        mostrar_inicio = getattr(self, "mostrar_inicio", 50)
        mostrar_final = getattr(self, "mostrar_final", 50)
        primeros = list(range(0, min(mostrar_inicio, self.capacidad)))
        ultimos = list(range(max(0, self.capacidad - mostrar_final), self.capacidad))
        return primeros + ultimos

    def _map_index_to_label(self, idx):
        """
        Mapear un índice real (0-based) de la estructura a la posición en self.labels.
        Devuelve None si ese índice no está en la porción visible.
        """
        visibles = self._get_visible_indices()
        try:
            return visibles.index(idx)
        except ValueError:
            return None

    def _reset_label_styles(self):
        """Restaura estilos por defecto de todos los labels sin cambiar su texto."""
        for lbl in self.labels:
            text = lbl.text()
            if text:
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
                lbl.setStyleSheet("""
                    QLabel {
                        background-color: #EDE9FE;
                        border: 2px solid #A78BFA;
                        border-radius: 12px;
                        font-size: 18px;
                    }
                """)


