from PySide6.QtWidgets import QLabel, QWidget, QHBoxLayout
from PySide6.QtCore import Qt


class VistaListaEncadenada:
    def __init__(self, grid, controller, resaltar=None):
        self.grid = grid
        self.controller = controller
        self.resaltar = resaltar

    def dibujar(self):
        for i in reversed(range(self.grid.count())):
            widget = self.grid.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        estructura, anidados = self.controller.obtener_datos()

        titulo = QLabel("Visualización: Lista Encadenada (colisiones con punteros)")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("font-size: 18px; font-weight: bold; color: #4C1D95; margin-bottom: 15px;")
        self.grid.addWidget(titulo, 0, 0, alignment=Qt.AlignCenter)

        # Extraer información de resaltado
        posicion_resaltar = None
        es_anidado = False
        indice_anidado = -1

        if self.resaltar:
            posicion_resaltar = self.resaltar[0]
            detalle = self.resaltar[1]

            # Verificar si es un nodo encadenado (colisión)
            if "lista encadena" in detalle.lower() or "encaden" in detalle.lower():
                es_anidado = True
                # Extraer el índice del nodo encadenado
                import re
                # Buscar patrón como "lista encadenada 2" o "encadenada 2"
                match = re.search(r'encaden(?:ad)?a\s+(\d+)', detalle.lower())
                if match:
                    indice_anidado = int(match.group(1)) - 1

        fila_actual = 1
        for i in range(1, self.controller.controller.capacidad + 1):
            val = estructura.get(i, "")
            sublista = anidados[i - 1] if i - 1 < len(anidados) else []

            fila_layout = QHBoxLayout()

            # Nodo principal
            nodo = QLabel(str(val).zfill(self.controller.controller.digitos) if val else "")
            nodo.setFixedSize(70, 70)
            nodo.setAlignment(Qt.AlignCenter)

            # Resaltar solo si es el nodo principal y NO es un nodo anidado
            if posicion_resaltar == i and not es_anidado and val:
                nodo.setStyleSheet("""
                    background-color: #C4B5FD;
                    border: 2px solid #8B5CF6;
                    border-radius: 10px;
                    font-size: 16px;
                    font-weight: bold;
                """)
            else:
                nodo.setStyleSheet("""
                    background-color: #EDE9FE;
                    border: 2px solid #7C3AED;
                    border-radius: 10px;
                    font-size: 16px;
                """)
            fila_layout.addWidget(nodo)

            # Dibujar flechas y nodos encadenados
            for idx, clave in enumerate(sublista):
                flecha = QLabel("→")
                flecha.setAlignment(Qt.AlignCenter)
                flecha.setStyleSheet("font-size: 20px; color: #7C3AED;")
                fila_layout.addWidget(flecha)

                nodo_col = QLabel(str(clave).zfill(self.controller.controller.digitos))
                nodo_col.setFixedSize(70, 70)
                nodo_col.setAlignment(Qt.AlignCenter)

                # Resaltar solo si coincide la posición Y es el nodo anidado correcto
                if posicion_resaltar == i and es_anidado and indice_anidado == idx:
                    nodo_col.setStyleSheet("""
                        background-color: #C4B5FD;
                        border: 2px solid #8B5CF6;
                        border-radius: 10px;
                        font-size: 16px;
                        font-weight: bold;
                    """)
                else:
                    nodo_col.setStyleSheet("""
                        background-color: #DDD6FE;
                        border: 2px solid #7C3AED;
                        border-radius: 10px;
                        font-size: 16px;
                    """)
                fila_layout.addWidget(nodo_col)

            fila_contenedor = QWidget()
            fila_contenedor.setLayout(fila_layout)
            self.grid.addWidget(fila_contenedor, fila_actual, 0, alignment=Qt.AlignLeft)
            fila_actual += 1