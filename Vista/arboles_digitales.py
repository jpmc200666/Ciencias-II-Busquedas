from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel, QFrame,
    QPushButton, QLineEdit, QMessageBox,
    QGraphicsScene, QGraphicsView, QGraphicsEllipseItem, QGraphicsTextItem,
    QHBoxLayout, QSpacerItem, QSizePolicy
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPen, QBrush, QColor
from Controlador.Internas.ArbolesDigitalesController import ArbolesDigitalesController


class ArbolesDigitales(QMainWindow):
    def __init__(self, cambiar_ventana):
        super().__init__()
        self.cambiar_ventana = cambiar_ventana
        self.controller = ArbolesDigitalesController()

        self.setWindowTitle("Ciencias de la Computación II - Árboles Digitales")
        self.resize(1100, 700)

        # --- Widget central con layout vertical (encabezado arriba, resto abajo)
        central = QWidget()
        main_layout = QVBoxLayout(central)

        # ================= ENCABEZADO (ARRIBA) =================
        header_frame = QFrame()
        header_layout = QVBoxLayout(header_frame)
        header_layout.setContentsMargins(0, 0, 0, 0)

        # Fondo degradado y bordes redondeados
        header_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #d8b4fe, stop:1 #a78bfa
                );
                border-radius: 12px;
            }
            QLabel {
                color: white;
            }
        """)

        # Título grande
        titulo = QLabel("Ciencias de la Computación II - Árboles Digitales")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("font-size: 22px; font-weight: bold;")

        # Subtítulo más pequeño (opcional)
        subtitulo = QLabel("Operaciones")
        subtitulo.setAlignment(Qt.AlignCenter)
        subtitulo.setStyleSheet("font-size: 14px; font-weight: bold;")

        # Menú de navegación centrado abajo
        nav_layout = QHBoxLayout()
        btn_inicio = QPushButton("Inicio")
        btn_busqueda = QPushButton("Menú de Búsqueda")
        for btn in (btn_inicio, btn_busqueda):
            btn.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    color: #2E1065;
                    font-size: 14px;
                    font-weight: bold;
                    border: none;
                }
                QPushButton:hover {
                    text-decoration: underline;
                }
            """)
        btn_inicio.clicked.connect(lambda: self.cambiar_ventana("inicio"))
        btn_busqueda.clicked.connect(lambda: self.cambiar_ventana("busqueda"))
        nav_layout.addStretch()
        nav_layout.addWidget(btn_inicio)
        nav_layout.addWidget(btn_busqueda)
        nav_layout.addStretch()

        # Armado del encabezado
        header_layout.addWidget(titulo)
        header_layout.addWidget(subtitulo)
        header_layout.addLayout(nav_layout)

        main_layout.addWidget(header_frame)

        # ================= CUERPO (Árbol + Controles) =================
        body_layout = QHBoxLayout()

        # --- Panel izquierdo: Árbol ---
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.view.setRenderHints(self.view.renderHints())
        self.view.setStyleSheet("background-color: #F3E8FF; border-radius: 8px;")
        body_layout.addWidget(self.view, stretch=2)

        # --- Panel derecho: Controles ---
        controls_frame = QFrame()
        controls_frame.setStyleSheet("""
            QFrame {
                background-color: #F5F3FF;
                border-radius: 12px;
            }
        """)
        controls_layout = QVBoxLayout(controls_frame)
        controls_layout.setSpacing(20)
        controls_layout.setAlignment(Qt.AlignTop)

        # Insertar clave
        lbl_insertar = QLabel("Insertar Clave:")
        lbl_insertar.setStyleSheet("font-size: 14px; color: #4C1D95; font-weight: bold;")
        self.input_insertar = QLineEdit()
        self.input_insertar.setPlaceholderText("Ingrese clave (una palabra)")

        # Buscar clave
        lbl_buscar = QLabel("Buscar Clave (una letra):")
        lbl_buscar.setStyleSheet("font-size: 14px; color: #4C1D95; font-weight: bold;")
        self.input_buscar = QLineEdit()
        self.input_buscar.setPlaceholderText("Ingrese una letra para buscar")

        btn_buscar = QPushButton("Buscar")
        btn_buscar.clicked.connect(self.buscar_palabra)

        # Botón insertar
        btn_insertar = QPushButton("Insertar")
        btn_insertar.clicked.connect(self.insertar_palabra)

        # Botón buscar
        btn_buscar = QPushButton("Buscar")
        btn_buscar.clicked.connect(self.buscar_palabra)

        # Estilos botones morados
        for btn in (btn_insertar, btn_buscar):
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #7C3AED;
                    color: white;
                    font-size: 14px;
                    font-weight: bold;
                    border-radius: 8px;
                    padding: 8px 14px;
                }
                QPushButton:hover {
                    background-color: #6D28D9;
                }
            """)

        controls_layout.addWidget(lbl_insertar)
        controls_layout.addWidget(self.input_insertar)
        controls_layout.addWidget(btn_insertar)
        controls_layout.addWidget(lbl_buscar)
        controls_layout.addWidget(self.input_buscar)
        controls_layout.addWidget(btn_buscar)

        body_layout.addWidget(controls_frame, stretch=1)

        # Agregar el cuerpo al layout principal
        main_layout.addLayout(body_layout)

        self.setCentralWidget(central)

        # ================= ALFABETO Y CÓDIGOS =================
        lbl_abecedario = QLabel("Abecedario y Códigos Binarios:")
        lbl_abecedario.setStyleSheet("font-size: 14px; color: #4C1D95; font-weight: bold;")

        # Layout horizontal para dividir en 2 columnas
        alphabet_layout = QHBoxLayout()

        # Primera columna (A–M)
        col1 = QLabel()
        col1.setStyleSheet("""
            font-family: Consolas, monospace;
            font-size: 13px;
            background-color: #EDE9FE;
            border: 1px solid #C4B5FD;
            border-radius: 8px;
            padding: 6px;
        """)
        col1.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        # Segunda columna (N–Z)
        col2 = QLabel()
        col2.setStyleSheet(col1.styleSheet())
        col2.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        # Llenar texto para cada columna
        letras = list(self.controller.codigos.items())
        texto1 = "\n".join(f"{letra.upper()} : {codigo}" for letra, codigo in letras[:13])
        texto2 = "\n".join(f"{letra.upper()} : {codigo}" for letra, codigo in letras[13:])

        col1.setText(texto1)
        col2.setText(texto2)

        # Añadir al layout horizontal
        alphabet_layout.addWidget(col1)
        alphabet_layout.addWidget(col2)

        # Agregar todo al panel de controles
        controls_layout.addWidget(lbl_abecedario)
        controls_layout.addLayout(alphabet_layout)

    # --- Lógica ---
    def insertar_palabra(self):
        palabra = self.input_insertar.text().strip()
        if palabra:
            estado = self.controller.insertar(palabra)
            if estado == "OK":
                self.input_insertar.clear()
                self.dibujar_arbol()
            else:
                QMessageBox.warning(self, "Error", f"No se pudo insertar: {estado}")
        else:
            QMessageBox.warning(self, "Error", "Debe ingresar una palabra para insertar.")

    def buscar_palabra(self):
        clave = self.input_buscar.text().strip().lower()
        if clave and len(clave) == 1 and clave.isalpha():
            posicion = self.controller.buscar_clave(clave)
            if posicion is not None:
                QMessageBox.information(
                    self,
                    "Resultado",
                    f"La letra '{clave}' se encuentra en la posición binaria {posicion}."
                )
            else:
                QMessageBox.warning(
                    self,
                    "Resultado",
                    f"La letra '{clave}' NO se encuentra en el árbol."
                )

        else:
            QMessageBox.warning(
                self,
                "Error",
                "Debe ingresar una sola letra para buscar."
            )

    def dibujar_arbol(self):
        """Dibuja el árbol binario en la escena."""
        self.scene.clear()
        root = self.controller.root
        level_gap = 90
        start_offset = 280

        pen_line = QPen(QColor("#4C1D95"), 2)
        brush_node = QBrush(QColor("#7C3AED"))
        brush_end = QBrush(QColor("#C4B5FD"))
        text_color = Qt.white

        def draw(node, x, y, offset, depth):
            radio = 22
            circle = QGraphicsEllipseItem(x - radio, y - radio, 2 * radio, 2 * radio)
            if node.end_words:
                circle.setBrush(brush_end)
            else:
                circle.setBrush(brush_node)
            circle.setPen(QPen(QColor("#3b0764"), 2))
            self.scene.addItem(circle)

            # texto del nodo
            txt = ", ".join(node.letters[:2]) if node.letters else ""
            if len(node.letters) > 2:
                txt += "..."
            if not txt and node is self.controller.root:
                txt = "(root)"
            text_item = QGraphicsTextItem(txt)
            text_item.setDefaultTextColor(text_color)
            text_item.setPos(x - radio / 1.3, y - 8)
            self.scene.addItem(text_item)

            for bit in ('0', '1'):
                hijo = node.children.get(bit)
                if hijo:
                    child_x = x - offset if bit == '0' else x + offset
                    child_y = y + level_gap
                    self.scene.addLine(x, y + radio, child_x, child_y - radio, pen_line)

                    # etiqueta del bit
                    mid_x = (x + child_x) / 2
                    mid_y = (y + child_y) / 2 - 10
                    bit_label = QGraphicsTextItem(bit)
                    bit_label.setDefaultTextColor(QColor("#4C1D95"))
                    bit_label.setPos(mid_x, mid_y)
                    self.scene.addItem(bit_label)

                    draw(hijo, child_x, child_y, max(40, offset / 2), depth + 1)

        draw(root, 0, 0, start_offset, 1)
        self.view.setSceneRect(self.scene.itemsBoundingRect())
