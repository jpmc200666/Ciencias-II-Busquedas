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

        level_gap = 100
        start_offset = 400

        pen_line = QPen(QColor("#4C1D95"), 2)
        brush_root = QBrush(QColor("#9F7AEA"))  # morado medio para raíz
        brush_internal = QBrush(QColor("#C4B5FD"))  # morado claro para nodos internos
        brush_leaf = QBrush(QColor("#7C3AED"))  # morado oscuro para hojas con letras
        pen_node = QPen(QColor("#3b0764"), 2)
        edge_color = QColor("#4C1D95")

        def sort_key(item):
            """Ordenar: 00, 01, 10, 11, luego el bit solitario '1'"""
            key, _ = item
            if len(key) == 2:
                return (0, key)
            else:
                return (1, key)

        def draw(node, x, y, offset, depth, is_root=False):
            radio = 28
            circle = QGraphicsEllipseItem(x - radio, y - radio, 2 * radio, 2 * radio)

            # Colores según tipo de nodo
            if is_root:
                circle.setBrush(brush_root)
            elif node.letra:
                circle.setBrush(brush_leaf)
            else:
                circle.setBrush(brush_internal)

            circle.setPen(pen_node)
            self.scene.addItem(circle)

            # Texto del nodo
            if is_root:
                text = "root"
            elif node.letra:
                text = node.letra.upper()
            else:
                text = "*"

            text_item = QGraphicsTextItem(text)
            text_item.setDefaultTextColor(Qt.white)
            text_item.setPos(x - radio / 1.7, y - 10)
            self.scene.addItem(text_item)

            # Dibujar hijos
            children = sorted(node.children.items(), key=sort_key)
            num_children = len(children)

            if num_children == 0:
                return

            # Calcular posiciones de los hijos
            if num_children == 1:
                positions = [x]
            elif num_children == 2:
                positions = [x - offset / 2, x + offset / 2]
            elif num_children == 3:
                positions = [x - offset, x, x + offset]
            else:  # 4 o más
                positions = [x - offset * 1.5, x - offset / 2, x + offset / 2, x + offset * 1.5]

            for idx, (key, child) in enumerate(children):
                if idx < len(positions):
                    child_x = positions[idx]
                else:
                    child_x = x

                child_y = y + level_gap

                # Línea padre-hijo
                self.scene.addLine(x, y + radio, child_x, child_y - radio, pen_line)

                # Etiqueta de la arista (mostrar los bits)
                label_text = key
                mid_x = (x + child_x) / 2
                mid_y = (y + child_y) / 2 - 10
                bit_label = QGraphicsTextItem(label_text)
                bit_label.setDefaultTextColor(edge_color)
                bit_label.setPos(mid_x - 8, mid_y - 6)
                self.scene.addItem(bit_label)

                # Recursión (reducir offset)
                draw(child, child_x, child_y, max(60, offset / 1.8), depth + 1)

        draw(root, 0, 0, start_offset, 0, is_root=True)

        # Ajustar vista
        brect = self.scene.itemsBoundingRect()
        if brect.isNull():
            return
        self.view.setSceneRect(brect)
        self.view.resetTransform()
        self.view.fitInView(brect, Qt.KeepAspectRatio)
        self.view.scale(1.2, 1.2)