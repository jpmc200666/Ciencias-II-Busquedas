from Vista.lineal_interna import LinealInterna
from Vista.binaria_interna import BinariaInterna
from Vista.mod_interna import ModInterna

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

        # --- Menú horizontal (con estilo consistente con tu inicio) ---
        menu_bar = QMenuBar()
        # Forzar estilo en la barra y en los submenus para que no se vean "basicos"
        menu_bar.setStyleSheet("""
            QMenuBar {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #E9D5FF, stop:1 #C4B5FD
                );
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

            /* Submenu general style */
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
            /* Arrow for submenus (visual tweak) */
            QMenu::right-arrow {
                image: none; /* keep system arrow or remove if you want a custom icon */
            }
        """)

        # ✅ Menú Inicio (acción que no cambia texto)
        inicio_action = menu_bar.addAction("🏠 Inicio")
        inicio_action.triggered.connect(lambda: self.cambiar_ventana("inicio"))

        # 🔎 Construimos el menú "Búsquedas Internas" como QMenu y lo vinculamos a una acción
        menu_internas = QMenu("🔎 Búsquedas Internas", self)
        # Acciones directas
        menu_internas.addAction("Lineal", self.abrir_lineal)
        menu_internas.addAction("Binaria", self.abrir_binaria)

        # Submenú "Funciones Hash" (aparece al poner el mouse encima)
        submenu_hash = QMenu("Funciones Hash", self)
        submenu_hash.addAction("Función mod", self.abrir_mod)
        submenu_hash.addAction("Función cuadrado", lambda t="Función cuadrado": self.mostrar_opcion(t))
        submenu_hash.addAction("Función truncamiento", lambda t="Función truncamiento": self.mostrar_opcion(t))
        submenu_hash.addAction("Función plegamiento", lambda t="Función plegamiento": self.mostrar_opcion(t))

        menu_internas.addMenu(submenu_hash)
        menu_internas.addAction("Otras", lambda t="Otras": self.mostrar_opcion(t))

        # Añadimos como acción raíz para que el texto del botón no cambie
        busquedas_action = menu_bar.addAction("🔎 Búsquedas Internas")
        busquedas_action.setMenu(menu_internas)

        # 🌍 Menú Búsquedas Externas (igual lógica: acción raíz + QMenu)
        menu_externas = QMenu("🌍 Búsquedas Externas", self)
        menu_externas.addAction("Indexadas", lambda t="Indexadas": self.mostrar_opcion(t))
        menu_externas.addAction("Secuenciales", lambda t="Secuenciales": self.mostrar_opcion(t))
        menu_externas.addAction("Otras", lambda t="Otras externas": self.mostrar_opcion(t))

        busquedas_ext_action = menu_bar.addAction("🌍 Búsquedas Externas")
        busquedas_ext_action.setMenu(menu_externas)

        # Finalmente añadimos la barra al header
        header_layout.addWidget(menu_bar)

        # --- Contenido principal ---
        self.label = QLabel("Selecciona una opción del menú")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("font-size: 20px; color: #2c3e50; font-weight: bold; margin-top: 40px;")

        main_layout.addWidget(header)
        main_layout.addWidget(self.label, stretch=1)

    def mostrar_opcion(self, texto):
        """Método que sí existe y actualiza el label.
           Si prefieres otra lógica (ej: abrir un panel, llamar a cambiar_ventana),
           cámbialo aquí.
        """
        self.label.setText(f"Opción seleccionada: {texto}")

    def abrir_lineal(self):
        self.cambiar_ventana("lineal_interna")  # ✅ cambia de página en el stack

    def abrir_binaria(self):
        self.cambiar_ventana("binaria_interna")  # ✅ cambia de página en el stack

    def abrir_mod(self):
        self.cambiar_ventana("mod_interna")
