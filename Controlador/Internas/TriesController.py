# Controlador/Internas/TriesController.py
# -*- coding: utf-8 -*-

# --- Código Binario de 5 Bits ---
CODIGO_BINARIO = {
    'A': '00001', 'B': '00010', 'C': '00011', 'D': '00100', 'E': '00101',
    'F': '00110', 'G': '00111', 'H': '01000', 'I': '01001', 'J': '01010',
    'K': '01011', 'L': '01100', 'M': '01101', 'N': '01110', 'O': '01111',
    'P': '10000', 'Q': '10001', 'R': '10010', 'S': '10011', 'T': '10100',
    'U': '10101', 'V': '10110', 'W': '10111', 'X': '11000', 'Y': '11001',
    'Z': '11010'
}


class TrieNode:
    def __init__(self, letra=None, is_link=False):
        self.is_link = is_link  # True -> nodo de enlace '*'
        self.letra = letra  # letra almacenada (A-Z) si es nodo hoja
        self.children = {}  # hijos del nodo


class TriesController:
    def __init__(self):
        self.root = TrieNode(is_link=True)  # raíz siempre es '*'
        self.codigos = CODIGO_BINARIO
        self.letras_insertadas = set()  # mantener registro de letras insertadas

    def insertar(self, palabra: str):
        if not palabra:
            return "EMPTY"
        palabra = palabra.upper()
        for ch in palabra:
            if ch not in self.codigos:
                raise ValueError(f"Letra no válida: {ch}")
            self._insertar_letra(ch)
            self.letras_insertadas.add(ch)
        return "OK"

    def _insertar_letra(self, letra: str):
        codigo = self.codigos[letra]
        nodo = self.root
        pos = 0

        while pos < len(codigo):
            bit = codigo[pos]

            # Si no existe el hijo con ese bit
            if bit not in nodo.children:
                # Insertar la letra aquí
                nodo.children[bit] = TrieNode(letra=letra, is_link=False)
                return

            # Si existe el hijo
            hijo = nodo.children[bit]

            # Si es un nodo de enlace '*', continuamos bajando
            if hijo.is_link:
                nodo = hijo
                pos += 1
                continue

            # Si es un nodo con letra -> HAY COLISIÓN
            letra_existente = hijo.letra

            # Si es la misma letra, ya existe
            if letra == letra_existente:
                return

            # COLISIÓN: convertir el nodo en enlace '*'
            hijo.is_link = True
            letra_vieja = hijo.letra
            hijo.letra = None

            # Obtener códigos de ambas letras
            codigo_vieja = self.codigos[letra_vieja]
            codigo_nueva = codigo

            # Re-insertar AMBAS letras desde la siguiente posición
            pos_siguiente = pos + 1

            # Insertar letra vieja
            self._insertar_desde_posicion(hijo, letra_vieja, codigo_vieja, pos_siguiente)

            # Insertar letra nueva
            self._insertar_desde_posicion(hijo, letra, codigo_nueva, pos_siguiente)

            return

    def _insertar_desde_posicion(self, nodo, letra, codigo, pos):
        """Inserta una letra desde una posición específica del código"""
        nodo_actual = nodo

        while pos < len(codigo):
            bit = codigo[pos]

            # Si no existe el hijo
            if bit not in nodo_actual.children:
                nodo_actual.children[bit] = TrieNode(letra=letra, is_link=False)
                return

            # Si existe el hijo
            hijo = nodo_actual.children[bit]

            # Si es un nodo de enlace, continuamos
            if hijo.is_link:
                nodo_actual = hijo
                pos += 1
                continue

            # Si es un nodo con letra -> OTRA COLISIÓN
            if hijo.letra == letra:
                # Ya existe
                return

            # Convertir en enlace y continuar
            letra_existente_ahi = hijo.letra
            codigo_existente_ahi = self.codigos[letra_existente_ahi]

            hijo.is_link = True
            hijo.letra = None

            # Re-insertar recursivamente
            self._insertar_desde_posicion(hijo, letra_existente_ahi, codigo_existente_ahi, pos + 1)

            # Continuar con la letra actual
            nodo_actual = hijo
            pos += 1

    def buscar(self, letra: str):
        """
        Busca una letra y retorna la posición (secuencia de bits) donde se encuentra.
        Retorna: (encontrada: bool, posicion: str, nodo: TrieNode o None)
        """
        letra = letra.upper()
        if letra not in self.codigos:
            return (False, "", None)

        codigo = self.codigos[letra]
        nodo = self.root
        pos = 0
        posicion = ""  # Acumular la secuencia de bits

        while pos < len(codigo):
            bit = codigo[pos]

            if bit not in nodo.children:
                return (False, "", None)

            hijo = nodo.children[bit]
            posicion += bit  # Agregar el bit a la posición

            # Si es un nodo de enlace, seguimos bajando
            if hijo.is_link:
                nodo = hijo
                pos += 1
                continue

            # Si es un nodo con letra, verificamos si es la que buscamos
            if hijo.letra == letra:
                return (True, posicion, hijo)
            else:
                return (False, "", None)

        return (False, "", None)

    def eliminar(self, letra: str):
        """Elimina una letra y reconstruye el árbol"""
        letra = letra.upper()
        if letra not in self.codigos:
            raise ValueError(f"Letra no válida: {letra}")

        if letra not in self.letras_insertadas:
            raise ValueError(f"La letra {letra} no está en el Trie")

        # Eliminar la letra del conjunto
        self.letras_insertadas.discard(letra)

        # Reconstruir el árbol desde cero con las letras restantes
        self._reconstruir()

        return "OK"

    def _reconstruir(self):
        """Reconstruye el árbol con las letras actuales"""
        # Guardar las letras actuales
        letras_temp = list(self.letras_insertadas)

        # Limpiar el árbol
        self.root = TrieNode(is_link=True)

        # Re-insertar todas las letras
        for letra in letras_temp:
            self._insertar_letra(letra)

    def limpiar(self):
        self.root = TrieNode(is_link=True)
        self.letras_insertadas.clear()