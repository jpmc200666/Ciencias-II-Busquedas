from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel, QFrame,
    QComboBox, QSpinBox, QPushButton, QGridLayout, QScrollArea,
    QInputDialog, QHBoxLayout, QDialog, QMessageBox, QFileDialog, QTableWidgetItem
)
from PySide6.QtCore import Qt
from .dialogo_clave import DialogoClave
from Controlador.Internas.mod_controller import ModController
from .dialogo_colision import DialogoColisiones


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
        self.btn_buscar = QPushButton("Buscar clave")
        self.btn_eliminar_clave = QPushButton("Eliminar clave")
        self.btn_deshacer = QPushButton("Deshacer último movimiento")
        self.btn_guardar = QPushButton("Guardar estructura")

        for btn in ( self.btn_crear, self.btn_agregar, self.btn_buscar, self.btn_cargar,self.btn_eliminar,
                     self.btn_eliminar_clave, self.btn_deshacer, self.btn_guardar):

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
        grid_botones.addWidget(self.btn_buscar, 2, 0)
        grid_botones.addWidget(self.btn_eliminar_clave, 2, 1)
        grid_botones.addWidget(self.btn_deshacer, 3, 0)
        grid_botones.addWidget(self.btn_guardar, 3, 1)

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
        self.btn_buscar.clicked.connect(self.buscar_clave)
        self.btn_eliminar_clave.clicked.connect(self.eliminar_clave)
        self.btn_deshacer.clicked.connect(self.deshacer)
        self.btn_guardar.clicked.connect(self.guardar_estructura)
        # Estado
        self.labels = []
        self.capacidad = 0

    # --- Métodos básicos ---
    def crear_estructura(self):
        # Limpia
        for i in reversed(range(self.grid.count())):
            widget = self.grid.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        self.labels.clear()

        # Capacidad depende del rango
        n = int(self.rango.currentText().split("^")[1])
        self.capacidad = 10 ** n

        # Crear estructura en el controlador
        self.controller.crear_estructura(self.capacidad, self.digitos.value())

        if self.capacidad > 1000:
            QMessageBox.information(
                self, "Vista representativa",
                f"La capacidad real es {self.capacidad}, "
                "pero solo se muestra parcialmente."
            )
            mostrar = 50
            for i in range(mostrar):
                self._agregar_cuadro(i + 1, i + 1)

            puntos = QLabel("...")
            puntos.setStyleSheet("font-size: 18px; color: gray;")
            self.grid.addWidget(
                puntos, (mostrar // 10) * 2, mostrar % 10, 2, 1, alignment=Qt.AlignCenter
            )

            for i in range(mostrar):
                idx_real = self.capacidad - mostrar + i + 1
                self._agregar_cuadro(mostrar + i + 1, idx_real)
        else:
            for i in range(self.capacidad):
                self._agregar_cuadro(i + 1, i + 1)

        self.controller.ultima_estrategia = None

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
        """Adiciona una clave y maneja correctamente las colisiones y la vista."""
        if self.capacidad == 0 or self.controller is None:
            QMessageBox.warning(self, "Error", "Primero cree la estructura.")
            return

        # Obtener clave del usuario
        dialogo = DialogoClave(
            longitud=self.digitos.value(),
            titulo=f"Clave de {self.digitos.value()} dígitos",
            modo="insertar",
            parent=self
        )
        if dialogo.exec() != QDialog.Accepted:
            return

        clave = dialogo.get_clave()

        # Intentar insertar (sin estrategia inicial)
        resultado = self.controller.adicionar_clave(clave)

        # Si hubo colisión
        if resultado == "COLISION":
            dlg_col = DialogoColisiones(self)
            if dlg_col.exec() == QDialog.Accepted:
                estrategia = dlg_col.get_estrategia()

                # Registrar estrategia usada en el controlador
                self.controller.ultima_estrategia = estrategia

                # Reintentar la inserción con la estrategia seleccionada
                resultado = self.controller.adicionar_clave(clave, estrategia)
            else:
                QMessageBox.information(self, "Cancelado", "Inserción cancelada por el usuario.")
                return

        # Manejar resultados
        if resultado == "OK":
            QMessageBox.information(self, "Éxito", f"Clave {clave} insertada correctamente.")

            # 🔹 Actualizar la vista según la estrategia usada
            if getattr(self.controller, "ultima_estrategia", "") == "Arreglo anidado":
                self.actualizar_vista_anidada(modo="vertical")
            else:
                # Modo normal (horizontal u otra vista)
                self.actualizar_tabla()

        elif resultado == "LONGITUD":
            QMessageBox.warning(self, "Error",
                                f"La clave debe tener exactamente {self.digitos.value()} dígitos.")

        elif resultado == "REPETIDA":
            QMessageBox.warning(self, "Error", "La clave ya existe en la estructura.")

        elif isinstance(resultado, str) and resultado.startswith("ERROR:"):
            QMessageBox.critical(self, "Error", resultado)

        else:
            QMessageBox.warning(self, "Error", f"Resultado inesperado: {resultado}")

    def cargar_estructura(self):
        # ⚠️ Advertencia si ya hay datos en memoria
        if self.controller.capacidad > 0 and any(self.controller.estructura.values()):
            resp = QMessageBox.warning(
                self,
                "Advertencia",
                "La estructura actual será sobreescrita. ¿Desea continuar?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            if resp == QMessageBox.No:
                return

        # Seleccionar archivo
        ruta, _ = QFileDialog.getOpenFileName(self, "Cargar estructura", "", "Archivos JSON (*.json)")
        if ruta:
            self.controller.ruta_archivo = ruta
            if self.controller.cargar():
                QMessageBox.information(self, "Éxito", "Estructura cargada correctamente.")
                self.actualizar_tabla()
            else:
                QMessageBox.warning(self, "Error", "No se pudo cargar la estructura.")

    def eliminar_estructura(self):
        resp = QMessageBox.question(
            self,
            "Eliminar estructura",
            "¿Está seguro de que desea eliminar la estructura actual?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if resp == QMessageBox.Yes:
            self.controller.estructura = {}
            self.controller.capacidad = 0
            self.controller.digitos = 0
            self.controller.historial.clear()
            self.actualizar_tabla()
            QMessageBox.information(self, "Éxito", "Estructura eliminada correctamente.")

    def buscar_clave(self):
        clave, ok = QInputDialog.getText(self, "Buscar Clave", "Ingrese la clave a buscar:")
        if ok and clave:
            datos = self.controller.obtener_datos_vista()
            encontrado = None
            for pos, valor in datos["estructura"].items():
                if str(valor) == clave:
                    encontrado = pos
                    break

            if encontrado:
                QMessageBox.information(self, "Resultado", f"Clave {clave} encontrada en posición {encontrado}")
            else:
                QMessageBox.warning(self, "Resultado", f"Clave {clave} no encontrada")

    def eliminar_clave(self):
        clave, ok = QInputDialog.getText(self, "Eliminar clave", "Ingrese la clave a eliminar:")
        if not ok or not clave.strip():
            return

        resultado = self.controller.eliminar_clave(clave.strip())

        if resultado == "OK":
            QMessageBox.information(self, "Éxito", f"La clave {clave} fue eliminada correctamente.")
            self.actualizar_tabla()  # 👈 REFRESCAR TABLA
        elif resultado == "NO_EXISTE":
            QMessageBox.warning(self, "Error", f"La clave {clave} no existe en la estructura.")
        else:
            QMessageBox.critical(self, "Error", f"Ocurrió un problema: {resultado}")

    def deshacer(self):
        resultado = self.controller.deshacer()
        if resultado == "OK":
            QMessageBox.information(self, "Éxito", "Se deshizo el último movimiento.")
            self.actualizar_tabla()
        elif resultado == "VACIO":
            QMessageBox.warning(self, "Aviso", "No hay movimientos para deshacer.")
        else:
            QMessageBox.critical(self, "Error", f"Ocurrió un error: {resultado}")

    def guardar_estructura(self):
        # sugerimos nombre por defecto
        nombre_defecto = "interna_binaria.json"
        ruta, _ = QFileDialog.getSaveFileName(
            self,
            "Guardar estructura",
            nombre_defecto,
            "Archivos JSON (*.json)"
        )
        if not ruta:
            return  # usuario canceló

        try:
            self.controller.ruta_archivo = ruta
            self.controller.guardar()
            QMessageBox.information(self, "Éxito", f"Estructura guardada en:\n{ruta}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo guardar la estructura:\n{e}")

    def actualizar_vista_anidada(self, modo="vertical"):
        """Dibuja el arreglo principal completo y muestra colisiones a la derecha."""
        # Limpiar grid
        for i in reversed(range(self.grid.count())):
            widget = self.grid.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        estructura = self.controller.estructura or {}
        anidados = getattr(self.controller, "estructura_anidada", [])

        # 🔹 Garantizar longitud igual a la capacidad
        if not isinstance(anidados, list):
            anidados = []
        if len(anidados) != self.controller.capacidad:
            anidados = (anidados + [[]] * self.controller.capacidad)[:self.controller.capacidad]

        # 🔹 Calcular el número máximo de columnas anidadas existentes
        max_colisiones = max((len(sublista) for sublista in anidados), default=0)

        # --- Títulos ---
        # --- Título combinado ---
        titulo = QLabel("Arreglo principal  |  Arreglos anidados (colisiones)")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("font-size: 18px; font-weight: bold; color: #4C1D95;")
        self.grid.addWidget(titulo, 0, 0, 1, max_colisiones + 2, alignment=Qt.AlignCenter)

        # --- Estructura principal + anidados ---
        for fila in range(1, self.controller.capacidad + 1):
            val = estructura.get(fila, "")
            texto = str(val).zfill(self.controller.digitos) if val else ""
            celda = QLabel(texto)
            celda.setAlignment(Qt.AlignCenter)
            celda.setFixedSize(70, 70)
            celda.setStyleSheet("""
                background-color: #EDE9FE;
                border: 2px solid #7C3AED;
                border-radius: 10px;
                font-size: 16px;
            """)
            self.grid.addWidget(celda, fila, 0, alignment=Qt.AlignCenter)

            # índice
            idx = QLabel(str(fila))
            idx.setAlignment(Qt.AlignCenter)
            idx.setStyleSheet("color: gray; font-size: 12px;")
            self.grid.addWidget(idx, fila + 1, 0, alignment=Qt.AlignTop | Qt.AlignCenter)

            # --- Colisiones (relleno completo por columnas) ---
            sublista = anidados[fila - 1] if fila - 1 < len(anidados) else []
            for j in range(1, max_colisiones + 1):
                if j <= len(sublista):
                    # Celda con valor real
                    texto = str(sublista[j - 1]).zfill(self.controller.digitos)
                    estilo = """
                        background-color: #DDD6FE;
                        border: 2px solid #7C3AED;
                        border-radius: 10px;
                        font-size: 16px;
                    """
                else:
                    # Celda vacía (guía)
                    texto = ""
                    estilo = """
                        border: 2px dashed #C4B5FD;
                        background-color:#F5F3FF;
                        border-radius:10px;
                    """

                lbl = QLabel(texto)
                lbl.setAlignment(Qt.AlignCenter)
                lbl.setFixedSize(70, 70)
                lbl.setStyleSheet(estilo)
                self.grid.addWidget(lbl, fila, j + 1, alignment=Qt.AlignCenter)

    def actualizar_tabla(self):
        """Actualiza la vista para arreglos anidados (colisiones)."""
        # limpiar grid principal
        for i in reversed(range(self.grid.count())):
            widget = self.grid.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        self.labels = []
        estructura = self.controller.estructura

        # caso: arreglo anidado (colisiones)
        if isinstance(estructura, dict) and all(isinstance(v, list) for v in estructura.values()):
            titulo = QLabel("Arreglo principal     Arreglo anidado (colisiones)")
            titulo.setStyleSheet("font-weight: bold; font-size: 16px; color: #4B0082;")
            self.grid.addWidget(titulo, 0, 0, 1, 10, alignment=Qt.AlignCenter)

            # columnas separadas para el principal y cada subarreglo
            col_principal = 0
            col_sub = 1
            tam_sub = 5  # cantidad de cuadros por subarreglo

            for idx in range(1, self.capacidad + 1):
                # cuadro del arreglo principal
                cuadro = QLabel()
                cuadro.setAlignment(Qt.AlignCenter)
                cuadro.setFixedSize(70, 70)
                cuadro.setStyleSheet("background-color: #f3e8ff; border: 2px solid #7c3aed; border-radius: 10px;")
                val = ""
                if isinstance(estructura.get(idx, None), list) and estructura[idx]:
                    val = estructura[idx][0] if estructura[idx] else ""
                elif isinstance(estructura.get(idx, None), str):
                    val = estructura[idx]
                cuadro.setText(val)
                self.grid.addWidget(cuadro, idx, col_principal, alignment=Qt.AlignCenter)

                # etiqueta con número de posición debajo
                etiqueta = QLabel(str(idx))
                etiqueta.setStyleSheet("color: #7c3aed; font-size: 12px;")
                self.grid.addWidget(etiqueta, idx + 1, col_principal, alignment=Qt.AlignCenter)

                # ahora el subarreglo completo
                sublista = estructura.get(idx, [])
                for j in range(tam_sub):
                    valor = sublista[j] if j < len(sublista) else ""
                    sub_label = QLabel(valor)
                    sub_label.setAlignment(Qt.AlignCenter)
                    sub_label.setFixedSize(70, 70)

                    if valor:
                        sub_label.setStyleSheet(
                            "background-color: #ddd6fe; border: 2px solid #7c3aed; border-radius: 10px;")
                    else:
                        sub_label.setStyleSheet(
                            "border: 2px dashed #c084fc; background-color: #faf5ff; border-radius: 10px;")

                    # dibujar el subarreglo en la misma fila del principal, pero más a la derecha
                    self.grid.addWidget(sub_label, j, col_sub, alignment=Qt.AlignCenter)

            return

        # ---- CASO NORMAL (sin colisiones anidadas) ----
        if self.capacidad > 1000:
            mostrar = 50
            for i in range(mostrar):
                self._agregar_cuadro(i + 1, i + 1)
            puntos = QLabel("...")
            puntos.setStyleSheet("font-size: 18px; color: gray;")
            self.grid.addWidget(puntos, (mostrar // 10) * 2, mostrar % 10, 2, 1, alignment=Qt.AlignCenter)
            for i in range(mostrar):
                idx_real = self.capacidad - mostrar + i + 1
                self._agregar_cuadro(mostrar + i + 1, idx_real)
        else:
            for i in range(self.capacidad):
                self._agregar_cuadro(i + 1, i + 1)

        # rellenar valores normales
        for idx, cuadro in enumerate(self.labels):
            pos = idx + 1
            val = estructura.get(pos, "")
            cuadro.setText(val if val else "")
