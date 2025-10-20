from PySide6.QtWidgets import QLabel, QWidget, QHBoxLayout
from PySide6.QtCore import Qt


class VistaArregloAnidado:
    def __init__(self, grid, controller, resaltar=None):
        self.grid = grid
        self.controller = controller
        self.resaltar = resaltar  # Tupla: (posicion, detalle) o None

    def dibujar(self):
        # limpiar grid
        for i in reversed(range(self.grid.count())):
            widget = self.grid.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        estructura, anidados, max_col = self.controller.obtener_datos()

        titulo = QLabel("Arreglo principal  |  Arreglos anidados (colisiones)")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("font-size: 18px; font-weight: bold; color: #4C1D95; margin-bottom: 15px;")
        self.grid.addWidget(titulo, 0, 0, alignment=Qt.AlignCenter)

        # Extraer información de resaltado si existe
        posicion_resaltar = None
        es_anidado = False
        indice_anidado = -1

        if self.resaltar:
            posicion_resaltar = self.resaltar[0]
            detalle = self.resaltar[1]
            if "arreglo anidado" in detalle:
                es_anidado = True
                # Extraer el índice del arreglo anidado del detalle
                import re
                match = re.search(r'arreglo anidado (\d+)', detalle)
                if match:
                    indice_anidado = int(match.group(1)) - 1

        fila_actual = 1
        for fila in range(1, self.controller.controller.capacidad + 1):
            fila_layout = QHBoxLayout()
            fila_layout.setSpacing(0)
            fila_layout.setContentsMargins(0, 0, 0, 0)

            # Índice a la izquierda
            idx = QLabel(str(fila))
            idx.setAlignment(Qt.AlignCenter)
            idx.setFixedWidth(30)
            idx.setStyleSheet("""
                color: #7C3AED;
                font-size: 13px;
                font-weight: bold;
            """)
            fila_layout.addWidget(idx)

            # Celda principal
            val = estructura.get(fila, "")
            texto = str(val).zfill(self.controller.controller.digitos) if val else ""
            celda = QLabel(texto)
            celda.setFixedSize(70, 70)
            celda.setAlignment(Qt.AlignCenter)

            # Aplicar resaltado si corresponde
            if posicion_resaltar == fila and not es_anidado:
                celda.setStyleSheet("""
                    background-color: #FCD34D;
                    border: 3px solid #F59E0B;
                    border-radius: 10px;
                    font-size: 16px;
                    font-weight: bold;
                """)
            else:
                celda.setStyleSheet("""
                    background-color: #EDE9FE;
                    border: 2px solid #7C3AED;
                    border-radius: 10px;
                    font-size: 16px;
                """)
            fila_layout.addWidget(celda)

            # Arreglos anidados
            sublista = anidados[fila - 1] if fila - 1 < len(anidados) else []
            for j in range(max_col):
                if j < len(sublista):
                    texto = str(sublista[j]).zfill(self.controller.controller.digitos)

                    # Aplicar resaltado si corresponde
                    if posicion_resaltar == fila and es_anidado and indice_anidado == j:
                        estilo = """
                            background-color: #ad47ed;
                            border: 3px solid #b13cfa;
                            border-left: none;
                            border-radius: 10px;
                            font-size: 16px;
                            font-weight: bold;
                        """
                    else:
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

            fila_contenedor = QWidget()
            fila_contenedor.setLayout(fila_layout)
            self.grid.addWidget(fila_contenedor, fila_actual, 0, alignment=Qt.AlignLeft)
            fila_actual += 1