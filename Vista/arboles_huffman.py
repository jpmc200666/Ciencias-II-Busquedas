from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel, QFrame,
    QPushButton, QLineEdit, QMessageBox,
    QGraphicsScene, QGraphicsView, QGraphicsEllipseItem, QGraphicsTextItem,
    QHBoxLayout, QTextEdit
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPen, QBrush, QColor
from Controlador.Internas.ArbolesHuffmanController import ArbolesHuffmanController
from fractions import Fraction


class ArbolesHuffman(QMainWindow):
    def __init__(self, cambiar_ventana):
        super().__init__()
        self.cambiar_ventana = cambiar_ventana
        self.controller = ArbolesHuffmanController()

        self.setWindowTitle("Ciencias de la Computación II - Árboles de Huffman")
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
        titulo = QLabel("Ciencias de la Computación II - Árboles de Huffman")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("font-size: 22px; font-weight: bold;")

        # Subtítulo más pequeño (opcional)
        subtitulo = QLabel("Compresión de Texto")
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

        # Insertar texto
        lbl_insertar = QLabel("Insertar Texto:")
        lbl_insertar.setStyleSheet("font-size: 14px; color: #4C1D95; font-weight: bold;")
        self.input_insertar = QTextEdit()
        self.input_insertar.setPlaceholderText("Ingrese el texto a comprimir")
        self.input_insertar.setMaximumHeight(100)
        self.input_insertar.setStyleSheet("""
            QTextEdit {
                border: 2px solid #C4B5FD;
                border-radius: 6px;
                padding: 5px;
                background-color: white;
            }
        """)

        # Botón insertar
        btn_insertar = QPushButton("Generar Árbol de Huffman")
        btn_insertar.clicked.connect(self.generar_arbol)

        # Botón limpiar
        btn_limpiar = QPushButton("Limpiar Todo")
        btn_limpiar.clicked.connect(self.limpiar_todo)

        # Estilos botones morados
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

        # ================= TABLA DE FRECUENCIAS Y CÓDIGOS =================
        lbl_tabla = QLabel("Frecuencias y Códigos:")
        lbl_tabla.setStyleSheet("font-size: 14px; color: #4C1D95; font-weight: bold;")

        self.tabla_codigos = QTextEdit()
        self.tabla_codigos.setReadOnly(True)
        self.tabla_codigos.setMaximumHeight(200)
        self.tabla_codigos.setStyleSheet("""
            QTextEdit {
                font-family: Consolas, monospace;
                font-size: 12px;
                background-color: #EDE9FE;
                border: 1px solid #C4B5FD;
                border-radius: 8px;
                padding: 6px;
            }
        """)

        controls_layout.addWidget(lbl_tabla)
        controls_layout.addWidget(self.tabla_codigos)

        body_layout.addWidget(controls_frame, stretch=1)

        # Agregar el cuerpo al layout principal
        main_layout.addLayout(body_layout)

        self.setCentralWidget(central)

    # --- Lógica ---
    def generar_arbol(self):
        texto = self.input_insertar.toPlainText().strip()
        if texto:
            try:
                self.controller.construir_arbol(texto)
                self.input_insertar.setReadOnly(True)
                self.input_insertar.setStyleSheet("""
                    QTextEdit {
                        background-color: #E9D5FF;
                        color: #4C1D95;
                        font-weight: bold;
                        border: 2px solid #C4B5FD;
                        border-radius: 6px;
                        padding: 5px;
                    }
                """)
                self.dibujar_arbol()
                self.mostrar_tabla_codigos()
                QMessageBox.information(
                    self,
                    "Éxito",
                    "Árbol de Huffman generado correctamente."
                )
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al generar el árbol: {str(e)}")
        else:
            QMessageBox.warning(self, "Error", "Debe ingresar un texto para generar el árbol.")

    def dibujar_arbol(self):
        """Dibuja el árbol de Huffman en la escena."""
        self.scene.clear()
        self.view.setScene(self.scene)
        root = self.controller.root

        if not root:
            text_item = QGraphicsTextItem("Árbol vacío")
            text_item.setDefaultTextColor(QColor("#4C1D95"))
            text_item.setScale(1.5)
            text_item.setPos(-60, -20)
            self.scene.addItem(text_item)
            self.view.setSceneRect(self.scene.itemsBoundingRect())
            return

        level_gap = 90
        start_offset = 280

        pen_line = QPen(QColor("#4C1D95"), 2)
        brush_node = QBrush(QColor("#7C3AED"))
        brush_leaf = QBrush(QColor("#C4B5FD"))
        text_color = Qt.white

        def draw(node, x, y, offset, depth):
            radio = 22
            circle = QGraphicsEllipseItem(x - radio, y - radio, 2 * radio, 2 * radio)

            # Si es hoja (tiene carácter), usar color diferente
            if node.char is not None:
                circle.setBrush(brush_leaf)
            else:
                circle.setBrush(brush_node)

            circle.setPen(QPen(QColor("#3b0764"), 2))
            self.scene.addItem(circle)

            # Texto del nodo (carácter y frecuencia)
            try:
                freq_frac = str(Fraction(node.freq).limit_denominator())
            except Exception:
                freq_frac = str(node.freq)

            # Mostrar fracción y carácter (si lo tiene)
            if node.char is not None:
                txt = f"{node.char}\n{freq_frac}"
            else:
                # Si es raíz, mostrar '1' si la suma total es 1.0
                if abs(node.freq - 1.0) < 1e-6:
                    txt = "1"
                else:
                    txt = freq_frac

            text_item = QGraphicsTextItem(txt)
            text_item.setDefaultTextColor(text_color)
            text_item.setPos(x - radio / 1.3, y - 8)
            self.scene.addItem(text_item)

            # Dibujar hijo izquierdo (0)
            if node.left:
                child_x = x - offset
                child_y = y + level_gap
                self.scene.addLine(x, y + radio, child_x, child_y - radio, pen_line)

                # Etiqueta "0"
                mid_x = (x + child_x) / 2
                mid_y = (y + child_y) / 2 - 10
                bit_label = QGraphicsTextItem("0")
                bit_label.setDefaultTextColor(QColor("#4C1D95"))
                bit_label.setPos(mid_x, mid_y)
                self.scene.addItem(bit_label)

                draw(node.left, child_x, child_y, max(40, offset / 2), depth + 1)

            # Dibujar hijo derecho (1)
            if node.right:
                child_x = x + offset
                child_y = y + level_gap
                self.scene.addLine(x, y + radio, child_x, child_y - radio, pen_line)

                # Etiqueta "1"
                mid_x = (x + child_x) / 2
                mid_y = (y + child_y) / 2 - 10
                bit_label = QGraphicsTextItem("1")
                bit_label.setDefaultTextColor(QColor("#4C1D95"))
                bit_label.setPos(mid_x, mid_y)
                self.scene.addItem(bit_label)

                draw(node.right, child_x, child_y, max(40, offset / 2), depth + 1)

        draw(root, 0, 0, start_offset, 1)
        self.view.setSceneRect(self.scene.itemsBoundingRect())

    def mostrar_tabla_codigos(self):
        """Muestra la tabla de frecuencias y códigos Huffman."""
        frecuencias = self.controller.obtener_frecuencias()
        codigos = self.controller.obtener_codigos()

        if not frecuencias or not codigos:
            self.tabla_codigos.setText("No hay datos para mostrar")
            return

        texto = "Carácter | Frecuencia | Código\n"
        texto += "-" * 40 + "\n"

        for char in frecuencias.keys():
            char_display = char if char != ' ' else '[espacio]'
            freq = frecuencias[char]
            codigo = codigos.get(char, "N/A")
            texto += f"   {char_display:^8} | {freq:^10} | {codigo}\n"

        self.tabla_codigos.setText(texto)

    def limpiar_todo(self):
        """Elimina completamente el árbol y reinicia los campos."""
        confirm = QMessageBox.question(
            self,
            "Confirmar limpieza",
            "¿Seguro que deseas limpiar todo?\nEsta acción no se puede deshacer.",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirm == QMessageBox.No:
            return

        try:
            # Reiniciar estructura del árbol
            self.controller.limpiar()

            # Limpiar campo y desbloquearlo
            self.input_insertar.clear()
            self.input_insertar.setReadOnly(False)
            self.input_insertar.setStyleSheet("""
                QTextEdit {
                    border: 2px solid #C4B5FD;
                    border-radius: 6px;
                    padding: 5px;
                    background-color: white;
                }
            """)

            # Limpiar tabla de códigos
            self.tabla_codigos.clear()

            # Limpiar escena del árbol
            self.scene.clear()

            # Mostrar mensaje visual
            text_item = QGraphicsTextItem("Árbol vacío")
            text_item.setDefaultTextColor(QColor("#4C1D95"))
            text_item.setScale(1.5)
            text_item.setPos(-60, -20)
            self.scene.addItem(text_item)
            self.view.setScene(self.scene)
            self.view.setSceneRect(self.scene.itemsBoundingRect())

            QMessageBox.information(
                self,
                "Limpieza completada",
                "Se ha limpiado el árbol y puedes insertar nuevo texto."
            )

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ocurrió un problema al limpiar: {str(e)}")
