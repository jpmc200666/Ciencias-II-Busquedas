# Controlador/Internas/ArbolesDigitalesController.py

class NodoBinario:
    def __init__(self):
        self.children = {'0': None, '1': None}  # hijos binarios
        self.letters = []      # letras almacenadas en este nodo
        self.end_words = set() # palabra final si termina aquí


class ArbolesDigitalesController:
    def __init__(self):
        self.root = NodoBinario()
        # Mapeo letras -> binario de 5 bits
        self.codigos = {chr(97 + i): format(i + 1, "05b") for i in range(26)}
        self.current_word = None  # solo una clave a la vez

    def insertar(self, palabra: str):
        palabra = palabra.lower().strip()
        if not palabra:
            return "EMPTY"

        letras = [ch for ch in palabra if ch.isalpha()]
        if not letras:
            return "INVALID"

        # reiniciar árbol y clave actual
        self.root = NodoBinario()
        self.current_word = "".join(letras)

        # set para controlar letras ya insertadas
        letras_insertadas = set()

        # primera letra en raíz
        primera = letras[0]
        if primera not in self.codigos:
            return "INVALID_CHAR"
        self.root.letters = [primera]
        letras_insertadas.add(primera)

        # resto de letras
        current = self.root
        for letra in letras[1:]:
            if letra not in self.codigos:
                continue

            # ignorar si ya se insertó antes
            if letra in letras_insertadas:
                continue

            codigo = self.codigos[letra]
            nodo = self.root
            placed = False

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
            letras_insertadas.add(letra)  # marcar letra como insertada

        # marcar palabra completa
        current.end_words.add(self.current_word)
        return "OK"

    def buscar_clave(self, letra: str):
        """Busca una letra y devuelve su código binario si existe, None si no."""
        letra = letra.lower().strip()
        if len(letra) != 1 or letra not in self.codigos:
            return None

        return self.codigos[letra]

        resultado = None

        def dfs(nodo):
            nonlocal resultado
            if resultado:
                return
            if letra in nodo.letters:
                idx = nodo.letters.index(letra)
                resultado = (nodo, idx)
                return
            for b in ('0', '1'):
                hijo = nodo.children.get(b)
                if hijo:
                    dfs(hijo)

        dfs(self.root)
        return resultado
