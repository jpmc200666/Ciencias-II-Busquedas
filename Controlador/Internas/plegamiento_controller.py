class PlegamientoController:
    def __init__(self):
        self.estructura = []
        self.capacidad = 0
        self.digitos = 0

    def crear_estructura(self, capacidad, digitos):
        self.capacidad = capacidad
        self.digitos = digitos
        self.estructura = [None] * capacidad

    def adicionar_clave(self, clave: str):
        if len(clave) != self.digitos:
            return "LONGITUD"
        if clave in self.estructura:
            return "REPETIDA"

        # 🔹 Algoritmo de Plegamiento
        partes = [int(clave[i:i+2]) for i in range(0, len(clave), 2)]
        suma = sum(partes)
        pos = suma % self.capacidad

        inicio = pos
        while self.estructura[pos] is not None:
            pos = (pos + 1) % self.capacidad
            if pos == inicio:
                return "LLENO"

        self.estructura[pos] = clave
        return "OK"

    def obtener_datos_vista(self):
        datos = {"estructura": {}}
        for i, val in enumerate(self.estructura, start=1):
            if val is not None:
                datos["estructura"][i] = val
        return datos
