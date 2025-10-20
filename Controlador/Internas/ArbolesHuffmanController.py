import heapq
from collections import Counter


class NodoHuffman:
    """Nodo para el árbol de Huffman."""

    def __init__(self, char, freq):
        self.char = char  # Carácter (None para nodos internos)
        self.freq = freq  # Frecuencia
        self.left = None  # Hijo izquierdo
        self.right = None  # Hijo derecho

    def __lt__(self, other):
        """Comparador para la cola de prioridad (heap)."""
        return self.freq < other.freq


class ArbolesHuffmanController:
    def __init__(self):
        self.root = None
        self.codigos = {}  # Diccionario de códigos Huffman {carácter: código}
        self.frecuencias = {}  # Diccionario de frecuencias {carácter: frecuencia}
        self.texto_original = ""

    def construir_arbol(self, texto):
        """
        Construye el árbol de Huffman a partir de un texto.

        Args:
            texto (str): Texto a comprimir
        """
        if not texto:
            raise ValueError("El texto no puede estar vacío")

        self.texto_original = texto

        # 1. Calcular frecuencias
        self.frecuencias = Counter(texto)

        # 2. Crear una cola de prioridad (min-heap) con nodos hoja
        heap = []
        for char, freq in self.frecuencias.items():
            nodo = NodoHuffman(char, freq)
            heapq.heappush(heap, nodo)

        # 3. Construir el árbol de Huffman
        while len(heap) > 1:
            # Extraer los dos nodos con menor frecuencia
            izq = heapq.heappop(heap)
            der = heapq.heappop(heap)

            # Crear un nuevo nodo interno con la suma de frecuencias
            padre = NodoHuffman(None, izq.freq + der.freq)
            padre.left = izq
            padre.right = der

            # Insertar el nodo padre de vuelta en el heap
            heapq.heappush(heap, padre)

        # 4. El último nodo en el heap es la raíz
        self.root = heap[0] if heap else None

        # 5. Generar los códigos Huffman
        self.codigos = {}
        self._generar_codigos(self.root, "")

    def _generar_codigos(self, nodo, codigo_actual):
        """
        Genera los códigos Huffman recursivamente mediante recorrido del árbol.

        Args:
            nodo: Nodo actual
            codigo_actual: Código binario acumulado hasta este nodo
        """
        if nodo is None:
            return

        # Si es una hoja, guardar el código
        if nodo.char is not None:
            self.codigos[nodo.char] = codigo_actual if codigo_actual else "0"
            return

        # Recorrer hijo izquierdo (agregar '0')
        self._generar_codigos(nodo.left, codigo_actual + "0")

        # Recorrer hijo derecho (agregar '1')
        self._generar_codigos(nodo.right, codigo_actual + "1")

    def obtener_codigos(self):
        """Retorna el diccionario de códigos Huffman."""
        return self.codigos

    def obtener_frecuencias(self):
        """Retorna el diccionario de frecuencias."""
        return self.frecuencias

    def codificar_texto(self):
        """
        Codifica el texto original usando los códigos Huffman.

        Returns:
            str: Texto codificado en binario
        """
        if not self.texto_original or not self.codigos:
            return ""

        return "".join(self.codigos[char] for char in self.texto_original)

    def decodificar_texto(self, codigo_binario):
        """
        Decodifica un texto binario usando el árbol de Huffman.

        Args:
            codigo_binario (str): Cadena binaria a decodificar

        Returns:
            str: Texto decodificado
        """
        if not self.root or not codigo_binario:
            return ""

        resultado = []
        nodo_actual = self.root

        for bit in codigo_binario:
            # Navegar por el árbol
            if bit == '0':
                nodo_actual = nodo_actual.left
            else:
                nodo_actual = nodo_actual.right

            # Si llegamos a una hoja, agregar el carácter y reiniciar
            if nodo_actual.char is not None:
                resultado.append(nodo_actual.char)
                nodo_actual = self.root

        return "".join(resultado)

    def calcular_compresion(self):
        """
        Calcula el porcentaje de compresión logrado.

        Returns:
            dict: Diccionario con estadísticas de compresión
        """
        if not self.texto_original or not self.codigos:
            return {}

        # Tamaño original (8 bits por carácter en ASCII)
        bits_originales = len(self.texto_original) * 8

        # Tamaño comprimido
        bits_comprimidos = sum(len(self.codigos[char]) for char in self.texto_original)

        # Porcentaje de compresión
        porcentaje = ((bits_originales - bits_comprimidos) / bits_originales) * 100

        return {
            "bits_originales": bits_originales,
            "bits_comprimidos": bits_comprimidos,
            "ahorro_bits": bits_originales - bits_comprimidos,
            "porcentaje_compresion": round(porcentaje, 2)
        }

    def limpiar(self):
        """Limpia el árbol y todas las estructuras de datos."""
        self.root = None
        self.codigos = {}
        self.frecuencias = {}
        self.texto_original = ""