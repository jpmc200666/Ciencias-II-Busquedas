# Controlador/Internas/ArbolesDigitalesController.py

class NodoBinario:
    def __init__(self):
        self.children = {'0': None, '1': None}  # hijos binarios
        self.letters = []       # letras almacenadas en este nodo
        self.end_words = set()  # palabras que terminan aquí


class ArbolesDigitalesController:
    def __init__(self):
        # Nodo raíz del árbol
        self.root = NodoBinario()

        # Mapeo: letra → binario de 5 bits (a = 00001, b = 00010, ..., z = 11010)
        self.codigos = {chr(97 + i): format(i + 1, "05b") for i in range(26)}

        # Lista de palabras actualmente en el árbol
        self.palabras = []

        # Última palabra insertada
        self.current_word = None

    # =========================================================
    # MÉTODO: INSERTAR PALABRA
    # =========================================================
    def insertar(self, palabra: str):
        palabra = palabra.lower().strip()
        if not palabra:
            return "EMPTY"

        letras = [ch for ch in palabra if ch.isalpha()]
        if not letras:
            return "INVALID"

        self.current_word = "".join(letras)
        letras_insertadas = set()

        if self.root is None:
            self.root = NodoBinario()

        # Primera letra (va en la raíz)
        primera = letras[0]
        if primera not in self.codigos:
            return "INVALID_CHAR"

        if not self.root.letters:
            self.root.letters = [primera]
        elif primera not in self.root.letters:
            self.root.letters.append(primera)

        letras_insertadas.add(primera)
        current = self.root

        # Resto de letras
        for letra in letras[1:]:
            if letra not in self.codigos:
                continue
            if letra in letras_insertadas:
                continue

            codigo = self.codigos[letra]
            nodo = self.root
            placed = False

            # Recorre el código binario
            for bit in codigo:
                if nodo.children[bit] is None:
                    nodo.children[bit] = NodoBinario()
                    nodo = nodo.children[bit]
                    nodo.letters = [letra]
                    placed = True
                    break
                else:
                    nodo = nodo.children[bit]

            if not placed and letra not in nodo.letters:
                nodo.letters.append(letra)

            current = nodo
            letras_insertadas.add(letra)

        # Marca palabra completa
        current.end_words.add(self.current_word)

        # Guarda la palabra en la lista
        if self.current_word not in self.palabras:
            self.palabras.append(self.current_word)

        return "OK"

    # =========================================================
    # MÉTODO: BUSCAR CLAVE
    # =========================================================
    def buscar_clave(self, letra: str):
        """Devuelve la ruta binaria donde se encuentra una letra, o None si no existe."""
        if not self.root:
            return None

        def recorrer(node, actual_path):
            if node is None:
                return None

            if letra in node.letters:
                return actual_path

            for bit, hijo in node.children.items():
                resultado = recorrer(hijo, actual_path + bit)
                if resultado is not None:
                    return resultado
            return None

        return recorrer(self.root, "")

    # =========================================================
    # MÉTODO: ELIMINAR CLAVE
    # =========================================================
    def eliminar_clave(self, letra: str):
        """
        Elimina una letra del árbol y reconstruye las palabras sin dicha letra.
        """
        letra = letra.lower().strip()

        if not letra or len(letra) != 1 or letra not in self.codigos:
            return "Debe ingresar una sola letra válida (a-z)."

        # Verificar si la letra existe en el árbol
        if self.buscar_clave(letra) is None:
            return f"La letra '{letra}' no existe en el árbol."

        # 🔥 Crear nuevas palabras quitando la letra
        nuevas_palabras = []
        for p in self.palabras:
            nueva = p.replace(letra, "")
            if nueva:  # evita insertar palabras vacías
                nuevas_palabras.append(nueva)

        if not nuevas_palabras:
            # Si ninguna palabra sobrevive, vacía todo
            self.eliminar_arbol()
            return "OK", None

        # Actualizar lista de palabras
        self.palabras = nuevas_palabras

        # 🔁 Vaciar y reconstruir el árbol
        self.root = NodoBinario()
        for p in self.palabras:
            self.insertar(p)

        return "OK", self.root

    # =========================================================
    # MÉTODO: ELIMINAR ÁRBOL COMPLETO
    # =========================================================
    def eliminar_arbol(self):
        """
        Elimina completamente el árbol digital, todas las palabras y resetea los datos internos.
        """
        # Crear nueva raíz vacía
        self.root = NodoBinario()

        # Vaciar la lista de palabras y la palabra actual
        self.palabras.clear()
        self.current_word = None

        return "OK"

