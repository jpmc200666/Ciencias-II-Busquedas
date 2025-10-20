# Controlador/Internas/MultiplesResiduosController.py
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
    def __init__(self, letra=None, is_leaf=False):
        self.is_leaf = is_leaf  # True si es una hoja (contiene letra)
        self.letra = letra  # letra almacenada (A-Z) si es hoja
        self.children = {}  # hijos del nodo: '00', '01', '10', '11'


class MultiplesResiduosController:
    def __init__(self):
        self.root = TrieNode()  # raíz vacía
        self.codigos = CODIGO_BINARIO
        self.letras_insertadas = set()

    def _dividir_en_pares(self, codigo):
        """Divide el código binario en pares de bits"""
        # código de 5 bits: dividir en [2, 2, 1]
        pares = []
        pares.append(codigo[0:2])  # bits 0-1
        pares.append(codigo[2:4])  # bits 2-3
        pares.append(codigo[4:5])  # bit 4 (último)
        return pares

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
        pares = self._dividir_en_pares(codigo)

        nodo = self.root

        # Navegar por los niveles usando los pares
        for i, par in enumerate(pares):
            # Si no existe el hijo con ese par de bits, crearlo
            if par not in nodo.children:
                # Si es el último nivel, crear hoja con la letra
                if i == len(pares) - 1:
                    nodo.children[par] = TrieNode(letra=letra, is_leaf=True)
                else:
                    # Crear nodo interno
                    nodo.children[par] = TrieNode()
            else:
                # Si el nodo ya existe y es el último nivel
                if i == len(pares) - 1:
                    # Si ya hay una letra ahí y es diferente, hay colisión
                    if nodo.children[par].letra and nodo.children[par].letra != letra:
                        # En múltiples residuos, las colisiones se resuelven
                        # manteniendo ambas letras (lista)
                        pass
                    elif not nodo.children[par].letra:
                        # Asignar la letra
                        nodo.children[par].letra = letra
                        nodo.children[par].is_leaf = True
                    # Si es la misma letra, no hacer nada

            # Moverse al siguiente nivel
            if i < len(pares) - 1:
                nodo = nodo.children[par]

    def buscar(self, letra: str):
        """
        Busca una letra y retorna la posición donde se encuentra.
        Retorna: (encontrada: bool, posicion: str, nodo: TrieNode o None)
        """
        letra = letra.upper()
        if letra not in self.codigos:
            return (False, "", None)

        codigo = self.codigos[letra]
        pares = self._dividir_en_pares(codigo)

        nodo = self.root
        posicion = ""  # Acumular la ruta de pares

        for i, par in enumerate(pares):
            if par not in nodo.children:
                return (False, "", None)

            posicion += par
            if i < len(pares) - 1:
                posicion += "-"  # Separador visual

            hijo = nodo.children[par]

            # Si es el último nivel, verificar si es la letra buscada
            if i == len(pares) - 1:
                if hijo.is_leaf and hijo.letra == letra:
                    return (True, posicion, hijo)
                else:
                    return (False, "", None)

            # Moverse al siguiente nivel
            nodo = hijo

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
        self.root = TrieNode()

        # Re-insertar todas las letras
        for letra in letras_temp:
            self._insertar_letra(letra)

    def limpiar(self):
        self.root = TrieNode()
        self.letras_insertadas.clear()