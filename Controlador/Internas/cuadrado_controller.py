import os
from Modelo.manejador_archivos import ManejadorArchivos


class CuadradoController:
    def __init__(self, ruta_archivo="data/cuadrado.json"):
        self.ruta_archivo = ruta_archivo
        self.estructura = {}
        self.capacidad = 0
        self.digitos = 0
        self.historial = []

        os.makedirs(os.path.dirname(self.ruta_archivo), exist_ok=True)

    # -------------------------------
    # UTILIDADES
    # -------------------------------
    def _guardar_estado(self):
        """Guarda el estado actual en el historial para poder deshacer."""
        self.historial.append(self.estructura.copy())

    # -------------------------------
    # CREACIÓN
    # -------------------------------
    def crear_estructura(self, capacidad: int, digitos: int):
        """Crea una nueva estructura hash con el método del cuadrado medio."""
        self.capacidad = capacidad
        self.digitos = digitos
        self.estructura = {i: "" for i in range(1, capacidad + 1)}
        self.historial.clear()
        self.guardar()

    # -------------------------------
    # FUNCIÓN HASH
    # -------------------------------
    def funcion_hash(self, clave: int) -> int:
        """
        Función hash por el método del cuadrado medio:
        1. Se eleva la clave al cuadrado.
        2. Se extraen los dígitos centrales.
        3. Se ajusta al rango [1, capacidad].
        """
        cuadrado = str(clave * clave)
        longitud = len(cuadrado)

        # Extraer los dígitos centrales
        if longitud % 2 == 1:  # impar
            mid = longitud // 2
            extraidos = cuadrado[mid - 1: mid + 1]
        else:  # par
            mid = longitud // 2
            extraidos = cuadrado[mid - 1: mid + 1]

        if not extraidos:
            extraidos = "0"

        pos = int(extraidos)
        pos = ((pos - 1) % self.capacidad) + 1  # ajustar al rango 1..capacidad
        return pos

    # -------------------------------
    # ADICIÓN DE CLAVES
    # -------------------------------
    def adicionar_clave(self, clave: str) -> str:
        """
        Inserta una clave usando la función hash del cuadrado medio.
        Retorna:
        - "OK": si se insertó correctamente
        - "LONGITUD": si la longitud de la clave es incorrecta
        - "REPETIDA": si la clave ya existe
        - "COLISION": si la posición ya está ocupada
        - "ERROR: ...": para otros errores
        """
        # Validar longitud
        if len(clave) != self.digitos:
            return "LONGITUD"

        # Validar duplicado
        if clave in self.estructura.values():
            return "REPETIDA"

        try:
            clave_int = int(clave)
            pos = self.funcion_hash(clave_int)

            # Guardar estado para permitir deshacer
            self._guardar_estado()

            if self.estructura[pos] == "":
                self.estructura[pos] = clave
                self.guardar()
                return "OK"
            else:
                # Colisión sin manejo adicional
                self.historial.pop()  # deshacer el estado
                return "COLISION"

        except ValueError:
            return "ERROR: La clave debe ser numérica"
        except Exception as e:
            return f"ERROR: {e}"

    # -------------------------------
    # ELIMINAR CLAVE
    # -------------------------------
    def eliminar_clave(self, clave: str) -> str:
        """Elimina una clave si existe en la estructura."""
        clave = str(clave)
        encontrada = False

        for k, v in list(self.estructura.items()):
            if v == clave:
                encontrada = True
                self._guardar_estado()
                self.estructura[k] = ""
                self.guardar()
                break

        return "OK" if encontrada else "NO_EXISTE"

    # -------------------------------
    # DESHACER
    # -------------------------------
    def deshacer(self):
        """Deshace el último cambio."""
        if not self.historial:
            return "VACIO"
        self.estructura = self.historial.pop()
        self.guardar()
        return "OK"

    # -------------------------------
    # GUARDAR / CARGAR
    # -------------------------------
    def guardar(self):
        """Guarda la estructura en un archivo JSON."""
        datos = {
            "capacidad": self.capacidad,
            "digitos": self.digitos,
            "estructura": self.estructura,
        }
        ManejadorArchivos.guardar_json(self.ruta_archivo, datos)

    def cargar(self):
        """Carga la estructura desde archivo JSON."""
        datos = ManejadorArchivos.leer_json(self.ruta_archivo)
        if datos:
            self.capacidad = datos.get("capacidad", 0)
            self.digitos = datos.get("digitos", 0)
            self.estructura = {int(k): v for k, v in datos.get("estructura", {}).items()}
            return True
        return False

    # -------------------------------
    # OBTENER DATOS
    # -------------------------------
    def obtener_datos_vista(self):
        """Retorna los datos que la vista necesita mostrar."""
        return {
            "capacidad": self.capacidad,
            "digitos": self.digitos,
            "estructura": self.estructura,
        }

    def get_claves(self):
        """Devuelve las claves no vacías."""
        return [v for v in self.estructura.values() if v != ""]
