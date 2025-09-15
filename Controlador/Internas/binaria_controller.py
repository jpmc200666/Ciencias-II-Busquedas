class BinariaController:
    def __init__(self):
        self.capacidad = 0
        self.digitos = 0
        self.estructura = {}

    def crear_estructura(self, capacidad, digitos):
        """Inicializa la estructura binaria vacía."""
        self.capacidad = capacidad
        self.digitos = digitos
        self.estructura = {}
        return True

    def adicionar_clave(self, clave: str):
        """Agrega una clave en orden para permitir búsqueda binaria."""
        if len(clave) != self.digitos:
            return "LONGITUD"

        if clave in self.estructura.values():
            return "REPETIDA"

        if len(self.estructura) >= self.capacidad:
            return "LLENO"

        # Convertimos en lista, insertamos y mantenemos orden
        lista = list(self.estructura.values())
        lista.append(clave)
        lista.sort()

        # Reconstruimos el diccionario con índices ordenados
        self.estructura = {i: lista[i] for i in range(len(lista))}
        return "OK"

    def buscar(self, clave: str):
        """Búsqueda binaria en la estructura ordenada."""
        lista = list(self.estructura.values())
        low, high = 0, len(lista) - 1

        while low <= high:
            mid = (low + high) // 2
            if lista[mid] == clave:
                return mid  # lo encontró en la posición mid
            elif lista[mid] < clave:
                low = mid + 1
            else:
                high = mid - 1
        return -1  # no encontrado

    def cargar(self):
        """Simula carga desde archivo (por ahora falso)."""
        return bool(self.estructura)

    def obtener_datos_vista(self):
        """Devuelve datos para la GUI."""
        return {
            "capacidad": self.capacidad,
            "estructura": self.estructura
        }

    def guardar(self):
        pass
