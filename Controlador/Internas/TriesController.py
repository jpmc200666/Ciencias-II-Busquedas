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
        self.is_link = is_link     # True -> nodo de enlace '*' (por bit)
        self.letra = letra         # si es hoja guarda la letra (ej. 'A')
        self.children = {}         # claves: '0','1', o 'L<LETRA>' para hoja


class TriesController:
    def __init__(self):
        self.root = TrieNode(is_link=True)
        # usar CODIGO_BINARIO tal cual (llaves mayúsculas)
        self.codigos = CODIGO_BINARIO

    def insertar(self, palabra: str):
        if not palabra:
            return "EMPTY"
        palabra = palabra.upper()
        for ch in palabra:
            if ch not in self.codigos:
                raise ValueError(f"Letra no válida: {ch}")
            self._insertar_letra(ch)
        return "OK"

    def _insertar_letra(self, letra: str):
        codigo = self.codigos[letra]
        nodo = self.root

        # CREAR un nodo '*' para CADA bit (incluido el último)
        for bit in codigo:
            if bit not in nodo.children:
                nodo.children[bit] = TrieNode(is_link=True)
            nodo = nodo.children[bit]

        # ahora colgamos la hoja con la letra como hijo especial
        leaf_key = f"L{letra}"   # ej. 'LA' para la letra 'A'
        if leaf_key not in nodo.children:
            nodo.children[leaf_key] = TrieNode(letra=letra, is_link=False)

    def buscar(self, letra: str) -> bool:
        letra = letra.upper()
        if letra not in self.codigos:
            return False
        codigo = self.codigos[letra]
        nodo = self.root
        for bit in codigo:
            if bit not in nodo.children:
                return False
            nodo = nodo.children[bit]
        leaf_key = f"L{letra}"
        return leaf_key in nodo.children and nodo.children[leaf_key].letra == letra

    def limpiar(self):
        self.root = TrieNode(is_link=True)

