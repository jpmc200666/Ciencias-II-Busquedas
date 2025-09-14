import os
from Modelo.manejador_archivos import ManejadorArchivos


class LinealController:
    def __init__(self, ruta_archivo="data/lineal.json"):
        self.ruta_archivo = ruta_archivo
        self.estructura = {}   # Diccionario: {posicion: clave}
        self.capacidad = 0
        self.digitos = 0       # Número de dígitos de las claves

        # Crear carpeta si no existe
        os.makedirs(os.path.dirname(self.ruta_archivo), exist_ok=True)

    def crear_estructura(self, capacidad: int, digitos: int):
        """Crea la estructura vacía con una capacidad y número de dígitos dado."""
        self.capacidad = capacidad
        self.digitos = digitos
        self.estructura = {i: "" for i in range(capacidad)}
        self.guardar()  # Se guarda apenas se crea

    def agregar_clave(self, clave: str) -> bool:
        """Agrega una clave en la primera posición vacía.
        Devuelve True si se pudo, False si está lleno o si no cumple los dígitos.
        """
        if len(clave) != self.digitos:
            return False

        for i in range(self.capacidad):
            if self.estructura[i] == "":
                self.estructura[i] = clave
                self.guardar()  # Guardar automáticamente al insertar
                return True
        return False

    def adicionar_clave(self, clave: str) -> bool:
        """Alias para compatibilidad con la vista."""
        return self.agregar_clave(clave)

    def guardar(self):
        """Usa ManejadorArchivos para guardar en JSON."""
        datos = {
            "capacidad": self.capacidad,
            "digitos": self.digitos,
            "estructura": self.estructura
        }
        ManejadorArchivos.guardar_json(self.ruta_archivo, datos)

    def cargar(self):
        """Usa ManejadorArchivos para cargar desde JSON."""
        datos = ManejadorArchivos.leer_json(self.ruta_archivo)
        if datos:
            self.capacidad = datos.get("capacidad", 0)
            self.digitos = datos.get("digitos", 0)
            self.estructura = {int(k): v for k, v in datos.get("estructura", {}).items()}
            return True
        return False

    def obtener_datos_vista(self):
        """
        Devuelve los datos listos para que la vista se reconstruya.
        Incluye: capacidad, digitos y el diccionario de estructura.
        """
        return {
            "capacidad": self.capacidad,
            "digitos": self.digitos,
            "estructura": self.estructura
        }
