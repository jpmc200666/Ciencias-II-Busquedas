class ListaEncadenadaController:
    def __init__(self, controller):
        self.controller = controller

    def obtener_datos(self):
        estructura = self.controller.estructura or {}
        anidados = self.controller.lista_encadenada or []  # CAMBIO AQUÍ
        if not isinstance(anidados, list):
            anidados = []
        return estructura, anidados