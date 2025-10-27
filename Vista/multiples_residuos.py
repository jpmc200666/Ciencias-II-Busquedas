from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel, QFrame,
    QPushButton, QLineEdit, QMessageBox,
    QGraphicsScene, QGraphicsView, QGraphicsEllipseItem, QGraphicsTextItem,
    QHBoxLayout
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPen, QBrush, QColor
from Controlador.Internas.MultiplesResiduosController import MultiplesResiduosController


class MultiplesResiduos(QMainWindow):
    def __init__(self, cambiar_ventana=None):
        super().__init__()
        self.cambiar_ventana = cambiar_ventana
        self.controller = MultiplesResiduosController()
        self.nodo_resaltado = None  # Para resaltar el nodo buscado

        self.setWindowTitle("Ciencias de la Computación II - Múltiples Residuos")
        self.resize(1200, 750)

        # =================== WIDGET CENTRAL ===================
        central = QWidget()
        main_layout = QVBoxLayout(central)

        # ================= ENCABEZADO =================
        header_frame = QFrame()
        header_layout = QVBoxLayout(header_frame)
        header_layout.setContentsMargins(0, 0, 0, 0)

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

        titulo = QLabel("Ciencias de la Computación II - Múltiples Residuos")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("font-size: 22px; font-weight: bold;")

        subtitulo = QLabel("Operaciones - Asociación de 2 bits")
        subtitulo.setAlignment(Qt.AlignCenter)
        subtitulo.setStyleSheet("font-size: 14px; font-weight: bold;")

        nav_layout = QHBoxLayout()
        btn_inicio = QPushButton("Inicio")
        btn_volver = QPushButton("Volver")
        for btn in (btn_inicio, btn_volver):
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
        btn_volver.clicked.connect(lambda: self.cambiar_ventana("busqueda"))

        nav_layout.addStretch()
        nav_layout.addWidget(btn_inicio)
        nav_layout.addWidget(btn_volver)
        nav_layout.addStretch()

        header_layout.addWidget(titulo)
        header_layout.addWidget(subtitulo)
        header_layout.addLayout(nav_layout)

        main_layout.addWidget(header_frame)

        # ================= CUERPO PRINCIPAL =================
        body_layout = QHBoxLayout()

        # --- IZQUIERDA: Grafo ---
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.view.setRenderHints(self.view.renderHints())
        self.view.setStyleSheet("background-color: #F3E8FF; border-radius: 8px;")

        self.view.resetTransform()
        self.view.scale(1.5, 1.5)
        body_layout.addWidget(self.view, stretch=2)

        # --- DERECHA: Controles ---
        controls_frame = QFrame()
        controls_frame.setStyleSheet("""
            QFrame {
                background-color: #F5F3FF;
                border-radius: 12px;
            }
        """)
        controls_layout = QVBoxLayout(controls_frame)
        controls_layout.setSpacing(15)
        controls_layout.setAlignment(Qt.AlignTop)

        # === INSERTAR ===
        lbl_insertar = QLabel("Insertar Palabra:")
        lbl_insertar.setStyleSheet("font-size: 14px; color: #4C1D95; font-weight: bold;")

        self.input_insertar = QLineEdit()
        self.input_insertar.setPlaceholderText("Ingrese palabra (A-Z)")

        btn_insertar = QPushButton("Insertar")
        btn_insertar.clicked.connect(self.insertar_palabra)

        # === BUSCAR ===
        lbl_buscar = QLabel("Buscar Letra:")
        lbl_buscar.setStyleSheet("font-size: 14px; color: #4C1D95; font-weight: bold;")

        self.input_buscar = QLineEdit()
        self.input_buscar.setPlaceholderText("Ingrese letra (A-Z)")
        self.input_buscar.setMaxLength(1)

        btn_buscar = QPushButton("Buscar")
        btn_buscar.clicked.connect(self.buscar_letra)

        # === ELIMINAR ===
        lbl_eliminar = QLabel("Eliminar Letra:")
        lbl_eliminar.setStyleSheet("font-size: 14px; color: #4C1D95; font-weight: bold;")

        self.input_eliminar = QLineEdit()
        self.input_eliminar.setPlaceholderText("Ingrese letra (A-Z)")
        self.input_eliminar.setMaxLength(1)

        btn_eliminar = QPushButton("Eliminar")
        btn_eliminar.clicked.connect(self.eliminar_letra)

        # === LIMPIAR ===
        btn_limpiar = QPushButton("Limpiar Trie")
        btn_limpiar.clicked.connect(self.limpiar_trie)

        # Estilos para botones
        for btn in (btn_insertar, btn_buscar, btn_eliminar):
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

        btn_limpiar.setStyleSheet("""
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

        # Agregar widgets al layout
        controls_layout.addWidget(lbl_insertar)
        controls_layout.addWidget(self.input_insertar)
        controls_layout.addWidget(btn_insertar)

        controls_layout.addSpacing(10)
        controls_layout.addWidget(lbl_buscar)
        controls_layout.addWidget(self.input_buscar)
        controls_layout.addWidget(btn_buscar)

        controls_layout.addSpacing(10)
        controls_layout.addWidget(lbl_eliminar)
        controls_layout.addWidget(self.input_eliminar)
        controls_layout.addWidget(btn_eliminar)

        controls_layout.addSpacing(15)
        controls_layout.addWidget(btn_limpiar)

        body_layout.addWidget(controls_frame, stretch=1)

        main_layout.addLayout(body_layout)

        self.setCentralWidget(central)

    # ================= MÉTODOS =================
    def insertar_palabra(self):
        palabra = self.input_insertar.text().strip()
        if palabra:
            try:
                self.controller.insertar(palabra)
                self.input_insertar.clear()
                self.nodo_resaltado = None
                self.dibujar_trie()
                QMessageBox.information(self, "Éxito", f"Palabra '{palabra}' insertada correctamente.")
            except ValueError as e:
                QMessageBox.warning(self, "Error", str(e))
        else:
            QMessageBox.warning(self, "Error", "Debe ingresar una palabra para insertar.")

    def buscar_letra(self):
        letra = self.input_buscar.text().strip().upper()
        if letra:
            try:
                encontrada, posicion, nodo = self.controller.buscar(letra)
                if encontrada:
                    self.nodo_resaltado = letra
                    self.dibujar_trie()
                    QMessageBox.information(
                        self,
                        "Búsqueda",
                        f"✓ La letra '{letra}' SÍ está en el Trie.\n\n"
                        f"Posición (secuencia de bits): {posicion}\n"
                        f"Código binario completo: {self.controller.codigos[letra]}"
                    )
                else:
                    self.nodo_resaltado = None
                    self.dibujar_trie()
                    QMessageBox.information(self, "Búsqueda", f"✗ La letra '{letra}' NO está en el Trie.")
                self.input_buscar.clear()
            except Exception as e:
                QMessageBox.warning(self, "Error", str(e))
        else:
            QMessageBox.warning(self, "Error", "Debe ingresar una letra para buscar.")

    def eliminar_letra(self):
        letra = self.input_eliminar.text().strip().upper()
        if letra:
            try:
                self.controller.eliminar(letra)
                self.input_eliminar.clear()
                self.nodo_resaltado = None
                self.dibujar_trie()
                QMessageBox.information(self, "Éxito", f"Letra '{letra}' eliminada. Árbol reconstruido.")
            except ValueError as e:
                QMessageBox.warning(self, "Error", str(e))
        else:
            QMessageBox.warning(self, "Error", "Debe ingresar una letra para eliminar.")

    def limpiar_trie(self):
        """Reinicia el trie"""
        self.controller = MultiplesResiduosController()
        self.scene.clear()

    def dibujar_trie(self):
        self.scene.clear()
        root = self.controller.root

        # Parámetros visuales
        level_gap = 120
        node_radius = 26
        horizontal_gap = 70  # espacio base entre nodos hermanos

        pen_line = QPen(QColor("#4C1D95"), 2)
        brush_root = QBrush(QColor("#9F7AEA"))
        brush_internal = QBrush(QColor("#C4B5FD"))
        brush_leaf = QBrush(QColor("#7C3AED"))
        pen_node = QPen(QColor("#3b0764"), 2)
        edge_color = QColor("#4C1D95")

        def calcular_ancho(node):
            """Devuelve el ancho total (en px) que ocupa el subárbol."""
            if not node.children:
                return horizontal_gap
            total = 0
            for child in node.children.values():
                total += calcular_ancho(child)
            return total

        def draw(node, x, y, is_root=False):
            """Dibuja recursivamente cada nodo del trie."""
            circle = QGraphicsEllipseItem(x - node_radius, y - node_radius, 2 * node_radius, 2 * node_radius)

            # Color según tipo
            if is_root:
                circle.setBrush(brush_root)
            elif node.letra:
                circle.setBrush(brush_leaf)
            else:
                circle.setBrush(brush_internal)

            circle.setPen(pen_node)
            self.scene.addItem(circle)

            # Texto centrado
            text = "root" if is_root else (node.letra.upper() if node.letra else "*")
            text_item = QGraphicsTextItem(text)
            text_item.setDefaultTextColor(Qt.white)
            text_item.setScale(1.1)
            text_rect = text_item.boundingRect()
            text_item.setPos(x - text_rect.width() / 2, y - text_rect.height() / 2)
            self.scene.addItem(text_item)

            # Dibujar hijos
            children = list(node.children.items())
            if not children:
                return

            total_width = sum(calcular_ancho(child) for _, child in children)
            start_x = x - total_width / 2
            for key, child in children:
                ancho_child = calcular_ancho(child)
                child_x = start_x + ancho_child / 2
                child_y = y + level_gap

                # Línea padre-hijo
                self.scene.addLine(x, y + node_radius, child_x, child_y - node_radius, pen_line)

                # Etiqueta de arista
                mid_x = (x + child_x) / 2
                mid_y = (y + child_y) / 2 - 14
                label = QGraphicsTextItem(key)
                label.setDefaultTextColor(edge_color)
                label.setScale(0.9)
                label.setPos(mid_x - 8, mid_y)
                self.scene.addItem(label)

                draw(child, child_x, child_y)
                start_x += ancho_child

        draw(root, 0, 0, is_root=True)

        # Ajuste de vista
        brect = self.scene.itemsBoundingRect()
        margin = 80
        brect.adjust(-margin, -margin, margin, margin)
        self.view.setSceneRect(brect)
        self.view.fitInView(brect, Qt.KeepAspectRatio)
        self.view.scale(1.1, 1.1)
