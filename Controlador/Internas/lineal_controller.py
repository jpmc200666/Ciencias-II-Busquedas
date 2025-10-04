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

    def agregar_clave(self, clave: str) -> str:
        """
        Intenta agregar una clave en la primera posición vacía.
        Devuelve:
            - "OK" si se insertó
            - "REPETIDA" si ya existía
            - "LLENO" si no hay espacio
            - "LONGITUD" si no cumple los dígitos
        """
        # Validar longitud
        if len(clave) != self.digitos:
            return "LONGITUD"

        # Validar repetida
        if str(clave) in map(str, self.estructura.values()):
            return "REPETIDA"

        # Insertar en la primera posición vacía
        for i in range(self.capacidad):
            if self.estructura[i] == "":
                self.estructura[i] = str(clave)
                break
        else:
            return "LLENO"

        # 🔽 Reordenar claves (de menor a mayor) y volver a llenar el diccionario
        claves_ordenadas = sorted(
            [v for v in self.estructura.values() if v != ""],
            key=lambda x: int(x)
        )
        self.estructura = {i: (claves_ordenadas[i] if i < len(claves_ordenadas) else "")
                           for i in range(self.capacidad)}

        self.guardar()
        return "OK"

    def adicionar_clave(self, clave: str) -> str:
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

    def get_claves(self):
        """Devuelve la lista de claves actuales, ordenadas, sin vacíos."""
        return [v for v in self.estructura.values() if v != ""]

    def buscar_clave(self, clave: str) -> int:
        """Devuelve índice 0-based donde está la clave, o -1 si no existe."""
        clave = str(clave).strip()
        # comparación directa por string
        for i in range(self.capacidad):
            if str(self.estructura.get(i, "")).strip() == clave:
                return i
        # intento por entero (por si hay diferencias de formato: '0008' vs '8')
        try:
            k = int(clave)
            for i in range(self.capacidad):
                val = self.estructura.get(i, "")
                if val != "":
                    try:
                        if int(str(val).strip()) == k:
                            return i
                    except ValueError:
                        pass
        except ValueError:
            pass
        return -1

    def eliminar_clave(self, clave: str) -> bool:
        """
        Elimina la clave si existe. Reordena la estructura (como hace agregar_clave)
        y guarda. Devuelve True si se eliminó, False si no se encontró.
        """
        clave = str(clave).strip()

        # 1) buscar por igualdad directa
        for i in range(self.capacidad):
            if str(self.estructura.get(i, "")).strip() == clave:
                self.estructura[i] = ""
                # reordenar las restantes (mantener la lógica que ya usas al insertar)
                restantes = [v for v in self.estructura.values() if v != ""]
                try:
                    restantes = sorted(restantes, key=lambda x: int(x))
                except Exception:
                    restantes = list(restantes)
                self.estructura = {j: (restantes[j] if j < len(restantes) else "") for j in range(self.capacidad)}
                self.guardar()
                return True

        # 2) si no, intentar por valor numérico (por si la representación cambió)
        try:
            k = int(clave)
            for i in range(self.capacidad):
                val = self.estructura.get(i, "")
                if val != "":
                    try:
                        if int(str(val).strip()) == k:
                            self.estructura[i] = ""
                            restantes = [v for v in self.estructura.values() if v != ""]
                            try:
                                restantes = sorted(restantes, key=lambda x: int(x))
                            except Exception:
                                restantes = list(restantes)
                            self.estructura = {j: (restantes[j] if j < len(restantes) else "") for j in
                                               range(self.capacidad)}
                            self.guardar()
                            return True
                    except ValueError:
                        pass
        except ValueError:
            pass

        return False

