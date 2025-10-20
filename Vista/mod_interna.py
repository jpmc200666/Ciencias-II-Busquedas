from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel, QFrame,
    QComboBox, QSpinBox, QPushButton, QGridLayout, QScrollArea,
    QInputDialog, QHBoxLayout, QDialog, QFileDialog
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
        layout.setSpacing(15)

        # --- Encabezado idéntico al de búsqueda lineal ---
        header = QFrame()
        header.setStyleSheet("""
            background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0,
            stop:0 #D8B4FE, stop:1 #A78BFA);
            border-radius: 12px;
        """)
        header_layout = QVBoxLayout(header)
        header_layout.setSpacing(5)

        titulo = QLabel("Ciencias de la Computación II - Función Hash (Módulo)")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("""
            font-size: 26px;
            font-weight: bold;
            color: white;
            margin-top: 10px;
        """)
        header_layout.addWidget(titulo)

        # Menú igual al de búsqueda lineal
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

        # Conexiones del menú
        btn_inicio.clicked.connect(lambda: self.cambiar_ventana("inicio"))
        btn_busqueda.clicked.connect(lambda: self.cambiar_ventana("busqueda"))

        # --- Controles superiores alineados horizontalmente ---
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

        # --- Botones principales (misma distribución visual que búsqueda lineal) ---
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

        # --- Contenedor con scroll para la estructura ---
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

        # 🔒 BLOQUEAR controles de rango y dígitos después de crear la estructura
        self.rango.setEnabled(False)
        self.digitos.setEnabled(False)

        if self.capacidad > 1000:
            dialogo = DialogoClave(
                longitud=0,
                titulo="Vista representativa",
                modo="mensaje",
                parent=self,
                mensaje=f"La capacidad real es {self.capacidad}, pero solo se muestra parcialmente."
            )
            dialogo.exec()

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
        # Obtener cantidad total actual de claves (principales + anidadas)
        total_actual = len([v for v in self.controller.estructura.values() if v])
        anidados = getattr(self.controller, "estructura_anidada", [])
        if isinstance(anidados, list):
            total_actual += sum(len(sublista) for sublista in anidados if sublista)

        # Si ya se alcanzó el límite (capacidad total)
        if total_actual >= self.controller.capacidad:
            dialogo = DialogoClave(
                longitud=0,
                titulo="Capacidad alcanzada",
                modo="mensaje",
                parent=self,
                mensaje=f"No se pueden agregar más claves.\nLa estructura ya contiene {total_actual} claves de un máximo de {self.controller.capacidad}."
            )
            dialogo.exec()
            return

        """Adiciona una clave y maneja correctamente las colisiones y la vista."""
        if self.capacidad == 0 or self.controller is None:
            dialogo = DialogoClave(
                longitud=0,
                titulo="Error",
                modo="mensaje",
                parent=self,
                mensaje="Primero cree la estructura."
            )
            dialogo.exec()
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
            # Si ya hay una estrategia global definida, usarla directamente
            if getattr(self.controller, "ultima_estrategia", None):
                estrategia = self.controller.ultima_estrategia
                resultado = self.controller.adicionar_clave(clave, estrategia)
            else:
                # Si aún no hay estrategia, mostrar el diálogo por primera vez
                dlg_col = DialogoColisiones(self)
                if dlg_col.exec() == QDialog.Accepted:
                    estrategia = dlg_col.get_estrategia()
                    self.controller.ultima_estrategia = estrategia  # Guardar globalmente
                    resultado = self.controller.adicionar_clave(clave, estrategia)
                else:
                    dialogo = DialogoClave(
                        longitud=0,
                        titulo="Cancelado",
                        modo="mensaje",
                        parent=self,
                        mensaje="Inserción cancelada por el usuario."
                    )
                    dialogo.exec()
                    return

        # Manejar resultados
        if resultado == "OK":
            dialogo = DialogoClave(
                longitud=0,
                titulo="Éxito",
                modo="mensaje",
                parent=self,
                mensaje=f"Clave {clave} insertada correctamente."
            )
            dialogo.exec()

            # --- Actualizar vista según estrategia ---
            estrategia_actual = getattr(self.controller, "ultima_estrategia", "")

            if estrategia_actual == "Arreglo anidado":
                self.actualizar_vista_anidada()
            elif estrategia_actual == "Lista encadenada":
                self.actualizar_vista_encadenada()
            else:
                self.actualizar_tabla()

        elif resultado == "LONGITUD":
            dialogo = DialogoClave(
                longitud=0,
                titulo="Error",
                modo="mensaje",
                parent=self,
                mensaje=f"La clave debe tener exactamente {self.digitos.value()} dígitos."
            )
            dialogo.exec()

        elif resultado == "REPETIDA":
            dialogo = DialogoClave(
                longitud=0,
                titulo="Error",
                modo="mensaje",
                parent=self,
                mensaje="La clave ya existe en la estructura."
            )
            dialogo.exec()

        elif isinstance(resultado, str) and resultado.startswith("ERROR:"):
            dialogo = DialogoClave(
                longitud=0,
                titulo="Error",
                modo="mensaje",
                parent=self,
                mensaje=resultado
            )
            dialogo.exec()

        else:
            dialogo = DialogoClave(
                longitud=0,
                titulo="Error",
                modo="mensaje",
                parent=self,
                mensaje=f"Resultado inesperado: {resultado}"
            )
            dialogo.exec()

    def cargar_estructura(self):
        # ⚠️ Advertencia si ya hay datos en memoria
        if self.controller.capacidad > 0 and any(self.controller.estructura.values()):
            dialogo = DialogoClave(
                longitud=0,
                titulo="Advertencia",
                modo="confirmar",
                parent=self,
                mensaje="La estructura actual será sobreescrita. ¿Desea continuar?"
            )
            if dialogo.exec() != QDialog.Accepted:
                return

        # Seleccionar archivo
        ruta, _ = QFileDialog.getOpenFileName(self, "Cargar estructura", "", "Archivos JSON (*.json)")
        if ruta:
            self.controller.ruta_archivo = ruta
            if self.controller.cargar():
                dialogo = DialogoClave(
                    longitud=0,
                    titulo="Éxito",
                    modo="mensaje",
                    parent=self,
                    mensaje="Estructura cargada correctamente."
                )
                dialogo.exec()

                # 🔹 Mostrar según la última estrategia usada
                estrategia_actual = getattr(self.controller, "ultima_estrategia", "")

                if estrategia_actual == "Arreglo anidado":
                    self.actualizar_vista_anidada()
                elif estrategia_actual == "Lista encadenada":
                    self.actualizar_vista_encadenada()
                else:
                    self.actualizar_tabla()

            else:
                dialogo = DialogoClave(
                    longitud=0,
                    titulo="Error",
                    modo="mensaje",
                    parent=self,
                    mensaje="No se pudo cargar la estructura."
                )
                dialogo.exec()

    def eliminar_estructura(self):
        dialogo = DialogoClave(
            longitud=0,
            titulo="Eliminar estructura",
            modo="confirmar",
            parent=self,
            mensaje="¿Está seguro de que desea eliminar la estructura actual?"
        )
        if dialogo.exec() != QDialog.Accepted:
            return

        # --- 🔹 Limpieza visual total (todos los widgets y layouts anidados) ---
        def limpiar_layout(layout):
            """Elimina recursivamente todos los widgets y sublayouts."""
            if layout is not None:
                while layout.count():
                    item = layout.takeAt(0)
                    widget = item.widget()
                    if widget is not None:
                        widget.setParent(None)
                    elif item.layout():
                        limpiar_layout(item.layout())

        limpiar_layout(self.grid)  # limpia todo el grid visual

        # --- 🔹 Reiniciar estructuras del controlador ---
        self.controller.estructura = {}
        self.controller.capacidad = 0
        self.controller.digitos = 0
        self.controller.historial.clear()

        # 🔹 También reiniciar estructuras anidadas si existen
        if hasattr(self.controller, "estructura_anidada"):
            self.controller.estructura_anidada = []

        if hasattr(self.controller, "colisiones_controller"):
            cc = self.controller.colisiones_controller
            cc.estructura = [None] * getattr(cc, "tamaño", 0)
            cc.estructura_anidada = [None] * getattr(cc, "tamaño", 0)
            cc.ultima_estrategia = None
            cc.estrategia_fijada = False

        # 🔹 Limpiar estrategia
        self.controller.ultima_estrategia = None

        # 🔹 Limpiar estrategia visual si existe
        if hasattr(self, "estrategia_label"):
            self.estrategia_label.setText("Sin estrategia seleccionada")

        # 🔹 Reiniciar variables internas
        self.labels.clear()
        self.capacidad = 0

        # 🔓 DESBLOQUEAR controles de rango y dígitos para permitir crear nueva estructura
        self.rango.setEnabled(True)
        self.digitos.setEnabled(True)

        # 🔹 Actualizar vista vacía
        self.grid.update()
        self.scroll.update()

        dialogo = DialogoClave(
            longitud=0,
            titulo="Éxito",
            modo="mensaje",
            parent=self,
            mensaje="Estructura eliminada correctamente."
        )
        dialogo.exec()

    def buscar_clave(self):
        """Busca una clave en la estructura (principal y anidada)."""
        dialogo = DialogoClave(
            longitud=self.digitos.value(),
            titulo="Buscar clave",
            modo="buscar",
            parent=self
        )
        if dialogo.exec() != QDialog.Accepted:
            return

        clave = dialogo.get_clave()
        estructura = self.controller.estructura
        anidados = self.controller.estructura_anidada

        encontrado = None
        detalle = ""

        # 🔹 Buscar en el arreglo principal
        for pos, valor in estructura.items():
            if str(valor).strip() == clave:
                encontrado = pos
                detalle = f"en el arreglo principal (posición {pos})"
                break

        # 🔹 Buscar en los arreglos/listas anidadas si no está en el principal
        if not encontrado and isinstance(anidados, list):
            for i, sublista in enumerate(anidados):
                if not sublista:
                    continue

                # Convertir todos los elementos a str para comparar
                sublista_str = [str(x).strip() for x in sublista if x is not None]

                if clave in sublista_str:
                    encontrado = i + 1  # posición principal (1-based)
                    indice_anidado = sublista_str.index(clave)

                    # Diferenciar el mensaje según la estrategia
                    estrategia_actual = getattr(self.controller, "ultima_estrategia", "")
                    if estrategia_actual == "Lista encadenada":
                        detalle = f"en la lista encadenada de la posición {i + 1}, nodo #{indice_anidado + 1}"
                    else:
                        detalle = f"en el arreglo anidado de la posición {i + 1}, índice interno {indice_anidado + 1}"
                    break

        # 🔹 Resultado final
        if encontrado:
            dialogo_resultado = DialogoClave(
                longitud=0,
                titulo="Resultado",
                modo="mensaje",
                parent=self,
                mensaje=f"Clave {clave} encontrada {detalle}."
            )
            dialogo_resultado.exec()
        else:
            dialogo_resultado = DialogoClave(
                longitud=0,
                titulo="Resultado",
                modo="mensaje",
                parent=self,
                mensaje=f"Clave {clave} no encontrada en la estructura."
            )
            dialogo_resultado.exec()
        estructura = self.controller.estructura
        anidados = self.controller.estructura_anidada

        encontrado = None
        detalle = ""

        # 🔹 Buscar en el arreglo principal
        for pos, valor in estructura.items():
            if str(valor).strip() == clave:
                encontrado = pos
                detalle = f"en el arreglo principal (posición {pos})"
                break

        # 🔹 Buscar en los arreglos/listas anidadas si no está en el principal
        if not encontrado and isinstance(anidados, list):
            for i, sublista in enumerate(anidados):
                if not sublista:
                    continue

                # Convertir todos los elementos a str para comparar
                sublista_str = [str(x).strip() for x in sublista if x is not None]

                if clave in sublista_str:
                    encontrado = i + 1  # posición principal (1-based)
                    indice_anidado = sublista_str.index(clave)

                    # Diferenciar el mensaje según la estrategia
                    estrategia_actual = getattr(self.controller, "ultima_estrategia", "")
                    if estrategia_actual == "Lista encadenada":
                        detalle = f"en la lista encadenada de la posición {i + 1}, nodo #{indice_anidado + 1}"
                    else:
                        detalle = f"en el arreglo anidado de la posición {i + 1}, índice interno {indice_anidado + 1}"
                    break

        # 🔹 Resultado final
        if encontrado:
            dialogo = DialogoClave(
                longitud=0,
                titulo="Resultado",
                modo="mensaje",
                parent=self,
                mensaje=f"Clave {clave} encontrada {detalle}."
            )
            dialogo.exec()
        else:
            dialogo = DialogoClave(
                longitud=0,
                titulo="Resultado",
                modo="mensaje",
                parent=self,
                mensaje=f"Clave {clave} no encontrada en la estructura."
            )
            dialogo.exec()

    def eliminar_clave(self):
        """Elimina una clave de la estructura (principal o anidada)."""
        dialogo = DialogoClave(
            longitud=self.digitos.value(),
            titulo="Eliminar clave",
            modo="eliminar",
            parent=self
        )
        if dialogo.exec() != QDialog.Accepted:
            return

        clave = dialogo.get_clave()
        eliminada = False

        # Guardar estado antes de eliminar
        self.controller._guardar_estado()

        # --- Intentar eliminar del arreglo principal ---
        estructura = self.controller.estructura
        posiciones_a_borrar = [pos for pos, val in estructura.items() if str(val).strip() == clave]

        if posiciones_a_borrar:
            for pos in posiciones_a_borrar:
                estructura[pos] = ""  # limpiar

                # También limpiar en el controlador de colisiones si existe
                if self.controller.colisiones_controller:
                    idx = pos - 1
                    self.controller.colisiones_controller.estructura[idx] = None

            eliminada = True

        # --- Intentar eliminar de los arreglos/listas anidadas ---
        anidados = self.controller.estructura_anidada
        if isinstance(anidados, list):
            for i, sublista in enumerate(anidados):
                if not sublista:
                    continue

                # Convertir a strings para comparar
                sublista_str = [str(x).strip() for x in sublista if x is not None]

                if clave in sublista_str:
                    # Encontrar el índice del elemento original (no el string)
                    for j, elem in enumerate(sublista):
                        if elem is not None and str(elem).strip() == clave:
                            del sublista[j]
                            eliminada = True

                            # Sincronizar con el controlador de colisiones
                            if self.controller.colisiones_controller:
                                self.controller.colisiones_controller.estructura_anidada[i] = sublista.copy()

                            break
                    break

        # --- Resultado final ---
        if eliminada:
            # Actualizar controlador
            self.controller.estructura = estructura
            self.controller.estructura_anidada = anidados

            # Guardar cambios
            self.controller.guardar()

            # Actualizar vista según estrategia
            estrategia_actual = getattr(self.controller, "ultima_estrategia", "")

            if estrategia_actual == "Arreglo anidado":
                self.actualizar_vista_anidada()
            elif estrategia_actual == "Lista encadenada":
                self.actualizar_vista_encadenada()
            else:
                self.actualizar_tabla()

            dialogo = DialogoClave(
                longitud=0,
                titulo="Éxito",
                modo="mensaje",
                parent=self,
                mensaje=f"La clave {clave} fue eliminada correctamente."
            )
            dialogo.exec()
        else:
            # Si no se eliminó nada, remover el estado guardado del historial
            if self.controller.historial:
                self.controller.historial.pop()

            dialogo = DialogoClave(
                longitud=0,
                titulo="Error",
                modo="mensaje",
                parent=self,
                mensaje=f"La clave {clave} no existe en la estructura."
            )
            dialogo.exec()

    def deshacer(self):
        """Deshace el último movimiento (compatible con todas las estrategias)."""
        resultado = self.controller.deshacer()

        if isinstance(resultado, dict):
            # 🧩 Caso extendido: el controlador devolvió un estado completo
            self.controller.estructura = resultado.get("estructura", self.controller.estructura)
            self.controller.estructura_anidada = resultado.get("estructura_anidada",
                                                               getattr(self.controller, "estructura_anidada", []))

            # Restaurar en el controlador de colisiones también
            if self.controller.colisiones_controller:
                # Reconstruir estructura principal del controlador
                self.controller.colisiones_controller.estructura = [None] * self.controller.capacidad
                for pos, valor in self.controller.estructura.items():
                    if valor and valor != "":
                        idx = pos - 1
                        try:
                            self.controller.colisiones_controller.estructura[idx] = int(valor)
                        except ValueError:
                            self.controller.colisiones_controller.estructura[idx] = valor

                # Restaurar estructura anidada del controlador
                self.controller.colisiones_controller.estructura_anidada = [
                    lst.copy() if lst else [] for lst in self.controller.estructura_anidada
                ]

            # 🔁 Refrescar la vista según la estrategia activa
            estrategia_actual = getattr(self.controller, "ultima_estrategia", "")

            if estrategia_actual == "Arreglo anidado":
                self.actualizar_vista_anidada()
            elif estrategia_actual == "Lista encadenada":
                self.actualizar_vista_encadenada()
            else:
                self.actualizar_tabla()

            dialogo = DialogoClave(
                longitud=0,
                titulo="Éxito",
                modo="mensaje",
                parent=self,
                mensaje="Se deshizo el último movimiento."
            )
            dialogo.exec()

        elif resultado == "OK":
            # 🔹 Versión simple (antiguo comportamiento)
            estrategia_actual = getattr(self.controller, "ultima_estrategia", "")

            if estrategia_actual == "Arreglo anidado":
                self.actualizar_vista_anidada()
            elif estrategia_actual == "Lista encadenada":
                self.actualizar_vista_encadenada()
            else:
                self.actualizar_tabla()

            dialogo = DialogoClave(
                longitud=0,
                titulo="Éxito",
                modo="mensaje",
                parent=self,
                mensaje="Se deshizo el último movimiento."
            )
            dialogo.exec()

        elif resultado == "VACIO":
            dialogo = DialogoClave(
                longitud=0,
                titulo="Aviso",
                modo="mensaje",
                parent=self,
                mensaje="No hay movimientos para deshacer."
            )
            dialogo.exec()

        else:
            dialogo = DialogoClave(
                longitud=0,
                titulo="Error",
                modo="mensaje",
                parent=self,
                mensaje=f"Ocurrió un error: {resultado}"
            )
            dialogo.exec()

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
            dialogo = DialogoClave(
                longitud=0,
                titulo="Éxito",
                modo="mensaje",
                parent=self,
                mensaje=f"Estructura guardada en:\n{ruta}"
            )
            dialogo.exec()
        except Exception as e:
            dialogo = DialogoClave(
                longitud=0,
                titulo="Error",
                modo="mensaje",
                parent=self,
                mensaje=f"No se pudo guardar la estructura:\n{e}"
            )
            dialogo.exec()

    def actualizar_vista_anidada(self, modo="vertical"):
        """Dibuja el arreglo principal con sus arreglos anidados pegados visualmente."""
        # Limpiar grid
        for i in reversed(range(self.grid.count())):
            widget = self.grid.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        # --- Ajustes del grid principal ---
        self.grid.setHorizontalSpacing(0)
        self.grid.setVerticalSpacing(5)
        self.grid.setContentsMargins(0, 0, 0, 0)

        # --- Datos ---
        estructura = self.controller.estructura or {}
        anidados = getattr(self.controller, "estructura_anidada", [])
        if not isinstance(anidados, list):
            anidados = []

        if len(anidados) != self.controller.capacidad:
            anidados = (anidados + [[]] * self.controller.capacidad)[:self.controller.capacidad]

        # --- Calcular el máximo global de colisiones (para dibujar estructura completa) ---
        max_colisiones_global = max((len(sublista) for sublista in anidados), default=0)
        # --- Título ---
        # --- Título ---
        titulo = QLabel("Arreglo principal  |  Arreglos anidados (colisiones)")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("font-size: 18px; font-weight: bold; color: #4C1D95; margin-bottom: 15px;")
        self.grid.addWidget(titulo, 0, 0, alignment=Qt.AlignCenter)

        # --- Construcción visual fila por fila ---
        fila_actual = 1
        for fila in range(1, self.controller.capacidad + 1):
            fila_layout = QHBoxLayout()
            fila_layout.setSpacing(0)
            fila_layout.setContentsMargins(0, 0, 0, 0)

            # ---------------- Celda principal ----------------
            val = estructura.get(fila, "")
            texto = str(val).zfill(self.controller.digitos) if val else ""
            celda = QLabel(texto)
            celda.setFixedSize(70, 70)
            celda.setAlignment(Qt.AlignCenter)
            celda.setStyleSheet("""
                        background-color: #EDE9FE;
                        border: 2px solid #7C3AED;
                        border-radius: 10px;
                        font-size: 16px;
                    """)
            fila_layout.addWidget(celda)

            # ---------------- Arreglos anidados ----------------
            sublista = anidados[fila - 1] if fila - 1 < len(anidados) else []

            for j in range(max_colisiones_global):
                if j < len(sublista):
                    texto = str(sublista[j]).zfill(self.controller.digitos)
                    estilo = """
                                background-color: #DDD6FE;
                                border: 2px solid #7C3AED;
                                border-left: none;
                                border-radius: 10px;
                                font-size: 16px;
                            """
                else:
                    texto = ""
                    estilo = """
                                border: 2px dashed #C4B5FD;
                                border-left: none;
                                background-color: #F5F3FF;
                                border-radius: 10px;
                            """

                lbl = QLabel(texto)
                lbl.setFixedSize(70, 70)
                lbl.setAlignment(Qt.AlignCenter)
                lbl.setStyleSheet(estilo)
                fila_layout.addWidget(lbl)

            # ---------------- Índice a la izquierda ----------------
            fila_layout_con_indice = QHBoxLayout()
            fila_layout_con_indice.setSpacing(10)
            fila_layout_con_indice.setContentsMargins(0, 0, 0, 0)

            # Etiqueta de índice al lado izquierdo
            idx = QLabel(str(fila))
            idx.setAlignment(Qt.AlignCenter)
            idx.setFixedWidth(30)
            idx.setStyleSheet("""
                        color: #7C3AED;
                        font-size: 13px;
                        font-weight: bold;
                    """)
            fila_layout_con_indice.addWidget(idx)

            # Agregar el layout original de la fila (principal + anidados)
            fila_layout_con_indice.addLayout(fila_layout)

            # Contenedor final de toda la fila
            fila_contenedor = QWidget()
            fila_contenedor.setLayout(fila_layout_con_indice)
            self.grid.addWidget(fila_contenedor, fila_actual, 0, alignment=Qt.AlignLeft)

            fila_actual += 1

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

    def actualizar_vista_encadenada(self):
        """Dibuja visualmente la estructura con listas encadenadas."""
        # Limpiar grid
        for i in reversed(range(self.grid.count())):
            widget = self.grid.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        # --- Título ---
        titulo = QLabel("Visualización: Lista Encadenada (colisiones con punteros)")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("""
                    font-size: 18px;
                    font-weight: bold;
                    color: #4C1D95;
                    margin-bottom: 15px;
                """)
        self.grid.addWidget(titulo, 0, 0, alignment=Qt.AlignCenter)

        fila_actual = 1

        for fila in range(1, self.controller.capacidad + 1):
            # Obtener valor principal (indexado desde 1)
            val = self.controller.estructura.get(fila, "")

            # Obtener sublista (indexada desde 0)
            sublista = self.controller.estructura_anidada[fila - 1] if fila - 1 < len(
                self.controller.estructura_anidada) else []

            # Asegurar que sublista sea una lista
            if sublista is None:
                sublista = []
            elif not isinstance(sublista, list):
                sublista = []

            fila_layout = QHBoxLayout()
            fila_layout.setSpacing(10)
            fila_layout.setContentsMargins(0, 0, 0, 0)

            # Nodo principal
            nodo = QLabel(str(val).zfill(self.controller.digitos) if val != "" else "")
            nodo.setFixedSize(70, 70)
            nodo.setAlignment(Qt.AlignCenter)
            nodo.setStyleSheet("""
                        background-color: #EDE9FE;
                        border: 2px solid #7C3AED;
                        border-radius: 10px;
                        font-size: 16px;
                    """)
            fila_layout.addWidget(nodo)

            # Dibujar flechas y nodos encadenados
            for clave in sublista:
                flecha = QLabel("→")
                flecha.setAlignment(Qt.AlignCenter)
                flecha.setStyleSheet("font-size: 20px; color: #7C3AED;")
                fila_layout.addWidget(flecha)

                nodo_col = QLabel(str(clave).zfill(self.controller.digitos))
                nodo_col.setFixedSize(70, 70)
                nodo_col.setAlignment(Qt.AlignCenter)
                nodo_col.setStyleSheet("""
                            background-color: #DDD6FE;
                            border: 2px solid #7C3AED;
                            border-radius: 10px;
                            font-size: 16px;
                        """)
                fila_layout.addWidget(nodo_col)

            # Índice a la izquierda
            idx = QLabel(str(fila))
            idx.setAlignment(Qt.AlignCenter)
            idx.setFixedWidth(30)
            idx.setStyleSheet("color: #7C3AED; font-size: 13px; font-weight: bold;")

            fila_layout_final = QHBoxLayout()
            fila_layout_final.addWidget(idx)
            fila_layout_final.addLayout(fila_layout)

            contenedor_fila = QWidget()
            contenedor_fila.setLayout(fila_layout_final)
            self.grid.addWidget(contenedor_fila, fila_actual, 0, alignment=Qt.AlignLeft)

            fila_actual += 1
