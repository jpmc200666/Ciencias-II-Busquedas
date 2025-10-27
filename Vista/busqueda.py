from Vista.lineal_interna import LinealInterna
from Vista.binaria_interna import BinariaInterna
from Vista.mod_interna import ModInterna
from Vista.cuadrado_interna import CuadradoInterna
from Vista.truncamiento_interna import TruncamientoInterna
from Vista.plegamiento_interna import PlegamientoInterna

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel, QFrame,
    QMenuBar, QMenu
)
from PySide6.QtCore import Qt


class Busqueda(QMainWindow):
    def __init__(self, cambiar_ventana):
        super().__init__()
        self.cambiar_ventana = cambiar_ventana

        self.setWindowTitle("Ciencias de la Computación II - Búsqueda")
        self.setGeometry(300, 200, 1000, 600)

        # --- Widget central ---
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # --- Encabezado ---
        header = QFrame()
        header.setStyleSheet("""
            background: qlineargradient(
                x1:0, y1:0, x2:1, y2:0,
                stop:0 #D8B4FE, stop:1 #A78BFA
            );
        """)
        header_layout = QVBoxLayout(header)

        titulo = QLabel("Ciencias de la Computación II")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("font-size: 28px; font-weight: bold; color: white; margin: 15px;")
        header_layout.addWidget(titulo)

        # --- Menú horizontal ---
        menu_bar = QMenuBar()
        menu_bar.setStyleSheet("""
            QMenuBar {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #E9D5FF, stop:1 #C4B5FD);
                font-weight: bold;
                font-size: 16px;
                color: #4C1D95;
            }
            QMenuBar::item {
                spacing: 20px;
                padding: 8px 14px;
                border-radius: 8px;
            }
            QMenuBar::item:selected {
                background: #7e22ce;
                color: white;
                border-radius: 6px;
            }
            QMenu {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #F8F4FF, stop:1 #E9D5FF);
                border: 1px solid #C4B5FD;
                font-size: 15px;
                color: #4C1D95;
                padding: 6px;
                border-radius: 8px;
            }
            QMenu::item {
                padding: 6px 18px;
            }
            QMenu::item:selected {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #7e22ce, stop:1 #5a2ea6);
                color: white;
                border-radius: 6px;
            }
        """)

        # 🏠 Inicio
        inicio_action = menu_bar.addAction("🏠 Inicio")
        inicio_action.triggered.connect(lambda: self.cambiar_ventana("inicio"))

        # 🔎 Búsquedas Internas
        menu_internas = QMenu("🔎 Búsquedas Internas", self)
        menu_internas.addAction("Lineal", self.abrir_lineal)
        menu_internas.addAction("Binaria", self.abrir_binaria)

        submenu_hash = QMenu("Funciones Hash", self)
        submenu_hash.addAction("Función mod", self.abrir_mod)
        submenu_hash.addAction("Función cuadrado", self.abrir_cuadrado)
        submenu_hash.addAction("Función truncamiento", self.abrir_truncamiento)
        submenu_hash.addAction("Función plegamiento", self.abrir_plegamiento)
        menu_internas.addMenu(submenu_hash)

        submenu_arboles = QMenu("Otras", self)
        submenu_arboles.addAction("Árboles digitales", self.abrir_arboles_digitales)
        submenu_arboles.addAction("Tries (residuos)", self.abrir_tries_residuos)
        submenu_arboles.addAction("Residuos múltiples", self.abrir_multiples_residuos)
        submenu_arboles.addAction("Árboles Huffman", self.abrir_arboles_huffman)
        menu_internas.addMenu(submenu_arboles)

        busquedas_action = menu_bar.addAction("🔎 Búsquedas Internas")
        busquedas_action.setMenu(menu_internas)

        # 🌍 Búsquedas Externas
        menu_externas = QMenu("🌍 Búsquedas Externas", self)
        menu_externas.addAction("Lineal", self.abrir_lineal_externa)
        menu_externas.addAction("Binaria", self.abrir_binaria_externa)

        submenu_hash_ext = QMenu("Funciones Hash", self)
        submenu_hash_ext.addAction("Función mod", self.abrir_mod_externa)
        submenu_hash_ext.addAction("Función cuadrado", self.abrir_cuadrado_externa)
        submenu_hash_ext.addAction("Función truncamiento", self.abrir_truncamiento_externa)
        submenu_hash_ext.addAction("Función plegamiento", self.abrir_plegamiento_externa)
        menu_externas.addMenu(submenu_hash_ext)

        busquedas_ext_action = menu_bar.addAction("🌍 Búsquedas Externas")
        busquedas_ext_action.setMenu(menu_externas)

        # --- Añadir al header ---
        header_layout.addWidget(menu_bar)

        # --- Contenido principal ---
        self.label = QLabel("Selecciona una opción del menú")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("font-size: 20px; color: #2c3e50; font-weight: bold; margin-top: 40px;")

        main_layout.addWidget(header)
        main_layout.addWidget(self.label, stretch=1)


        # 🪣 Cubetas
        cubetas_action = menu_bar.addAction("🪣 Cubetas")
        cubetas_action.triggered.connect(self.abrir_cubetas)


    # ==== Métodos de navegación ====
    def mostrar_opcion(self, texto):
        self.label.setText(f"Opción seleccionada: {texto}")

    # Internas
    def abrir_lineal(self): self.cambiar_ventana("lineal_interna")
    def abrir_binaria(self): self.cambiar_ventana("binaria_interna")
    def abrir_mod(self): self.cambiar_ventana("mod_interna")
    def abrir_cuadrado(self): self.cambiar_ventana("cuadrado_interna")
    def abrir_truncamiento(self): self.cambiar_ventana("truncamiento_interna")
    def abrir_plegamiento(self): self.cambiar_ventana("plegamiento_interna")
    def abrir_busqueda_residuos(self): self.cambiar_ventana("busqueda_residuos")
    def abrir_arboles_digitales(self): self.cambiar_ventana("arboles_digitales")
    def abrir_tries_residuos(self): self.cambiar_ventana("tries_residuos")
    def abrir_multiples_residuos(self): self.cambiar_ventana("multiples_residuos")
    def abrir_arboles_huffman(self): self.cambiar_ventana("arboles_huffman")

    # Externas
    def abrir_lineal_externa(self): self.cambiar_ventana("lineal_externa")
    def abrir_binaria_externa(self): self.cambiar_ventana("binaria_externa")
    def abrir_mod_externa(self): self.cambiar_ventana("mod_externa")
    def abrir_cuadrado_externa(self): self.cambiar_ventana("cuadrado_externa")
    def abrir_truncamiento_externa(self): self.cambiar_ventana("truncamiento_externa")
    def abrir_plegamiento_externa(self): self.cambiar_ventana("plegamiento_externa")

    # Cubetas
    def abrir_cubetas(self):self.cambiar_ventana("Cubetas")
