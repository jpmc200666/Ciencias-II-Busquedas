from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel, QFrame,
    QPushButton, QLineEdit, QMessageBox,
    QGraphicsScene, QGraphicsView, QGraphicsEllipseItem, QGraphicsTextItem,
    QHBoxLayout
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPen, QBrush, QColor
from Controlador.Internas.TriesController import TriesController


class TriesResiduos(QMainWindow):
    def __init__(self, cambiar_ventana=None):
        super().__init__()
        self.cambiar_ventana = cambiar_ventana
        self.controller = TriesController()

        self.setWindowTitle("Ciencias de la Computación II - Tries por Residuos")
        self.resize(1100, 700)

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

        titulo = QLabel("Ciencias de la Computación II - Tries por Residuos")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("font-size: 22px; font-weight: bold;")

        subtitulo = QLabel("Operaciones")
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
        self.view.scale(1.5, 1.5)  # Zoom para que se vea más grande
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
        controls_layout.setSpacing(20)
        controls_layout.setAlignment(Qt.AlignTop)

        lbl_insertar = QLabel("Insertar Palabra:")
        lbl_insertar.setStyleSheet("font-size: 14px; color: #4C1D95; font-weight: bold;")

        self.input_insertar = QLineEdit()
        self.input_insertar.setPlaceholderText("Ingrese palabra (A-Z)")

        btn_insertar = QPushButton("Insertar")
        btn_insertar.clicked.connect(self.insertar_palabra)

        btn_limpiar = QPushButton("Limpiar Trie")
        btn_limpiar.clicked.connect(self.limpiar_trie)

        for btn in (btn_insertar, btn_limpiar):
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
                self.dibujar_trie()
            except ValueError as e:
                QMessageBox.warning(self, "Error", str(e))
        else:
            QMessageBox.warning(self, "Error", "Debe ingresar una palabra para insertar.")

    def limpiar_trie(self):
        """Reinicia el trie"""
        self.controller = TriesController()
        self.scene.clear()

    def dibujar_trie(self):
        self.scene.clear()
        root = self.controller.root

        level_gap = 110
        start_offset = 380

        pen_line = QPen(QColor("#4C1D95"), 2)
        brush_link = QBrush(QColor("#9F7AEA"))  # morado medio para '*'
        brush_other = QBrush(QColor("#C4B5FD"))  # morado claro para letras/raíz
        pen_node = QPen(QColor("#3b0764"), 2)
        edge_color = QColor("#4C1D95")

        def sort_key(item):
            key, _ = item
            if key.startswith('0'):
                return (0, key)
            if key.startswith('1'):
                return (1, key)
            return (2, key)  # hojas 'L...' al final

        def draw(node, x, y, offset, depth):
            radio = 28
            circle = QGraphicsEllipseItem(x - radio, y - radio, 2 * radio, 2 * radio)

            # colores
            if getattr(node, "is_link", False):
                circle.setBrush(brush_link)
            else:
                circle.setBrush(brush_other)

            circle.setPen(pen_node)
            self.scene.addItem(circle)

            # texto del nodo
            text = ""
            if getattr(node, "is_link", False):
                text = "*"
            elif getattr(node, "letra", None):
                text = node.letra.upper()
            elif node is root:
                text = "root"

            text_item = QGraphicsTextItem(text)
            text_item.setDefaultTextColor(Qt.white)
            text_item.setPos(x - radio / 1.7, y - 10)
            self.scene.addItem(text_item)

            # hijos: iterar TODOS los children (no agrupar por pares)
            children = sorted(node.children.items(), key=sort_key)
            for key, child in children:
                # dirección según primer carácter real ('0' izquierda, '1' derecha, otros centrado)
                first = key[0] if key else ''
                if first == '0':
                    child_x = x - offset
                elif first == '1':
                    child_x = x + offset
                else:
                    child_x = x  # hoja: colgar centrada bajo el último '*'
                child_y = y + level_gap

                # línea padre-hijo
                self.scene.addLine(x, y + radio, child_x, child_y - radio, pen_line)

                # etiqueta para arista: solo mostrar bits (0/1). hojas no muestran etiqueta.
                label_text = key if key in ('0', '1') else ""
                if label_text:
                    mid_x = (x + child_x) / 2
                    mid_y = (y + child_y) / 2 - 10
                    bit_label = QGraphicsTextItem(label_text)
                    bit_label.setDefaultTextColor(edge_color)
                    # pequeño ajuste centrar
                    bit_label.setPos(mid_x - 6, mid_y - 6)
                    self.scene.addItem(bit_label)

                # recursión (offset reducido)
                draw(child, child_x, child_y, max(40, offset / 2), depth + 1)

        draw(root, 0, 0, start_offset, 1)

        # ajustar vista y aplicar un ligero zoom para que no quede muy pequeño
        brect = self.scene.itemsBoundingRect()
        if brect.isNull():
            return
        self.view.setSceneRect(brect)
        self.view.resetTransform()
        self.view.fitInView(brect, Qt.KeepAspectRatio)
        self.view.scale(1.25, 1.25)

