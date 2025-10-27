#Controlador.Externas.LinealController

import math
import random


class LinealExternaController:
    """Controlador para la estructura de búsqueda lineal externa"""

    def __init__(self):
        self.bloques = []
        self.num_claves = 0
        self.tamanio_bloque = 0
        self.historial = []  # Para la funcionalidad de deshacer

    def crear_estructura(self, num_claves):
        """
        Crea la estructura de bloques vacía

        Args:
            num_claves (int): Número total de claves que soportará la estructura

        Returns:
            dict: Información de la estructura creada
        """
        self.num_claves = num_claves
        self.tamanio_bloque = math.floor(math.sqrt(num_claves))
        num_bloques = math.ceil(num_claves / self.tamanio_bloque)

        # Guardar estado para deshacer
        self.guardar_estado()

        # Crear bloques vacíos
        self.bloques = [[] for _ in range(num_bloques)]

        return {
            'num_claves': self.num_claves,
            'tamanio_bloque': self.tamanio_bloque,
            'num_bloques': num_bloques,
            'bloques': self.bloques
        }

    def insertar_clave(self, clave):
        """
        Inserta una clave en la estructura

        Args:
            clave (int): Clave a insertar

        Returns:
            dict: Resultado de la operación
        """
        # Verificar si la estructura está inicializada
        if not self.bloques:
            return {'exito': False, 'mensaje': 'La estructura no ha sido creada'}

        # Verificar si la clave ya existe
        if self.buscar_clave(clave)['encontrada']:
            return {'exito': False, 'mensaje': f'La clave {clave} ya existe'}

        # Verificar si hay espacio
        total_claves = sum(len(bloque) for bloque in self.bloques)
        if total_claves >= self.num_claves:
            return {'exito': False, 'mensaje': 'La estructura está llena'}

        # Guardar estado para deshacer
        self.guardar_estado()

        # Buscar el primer bloque con espacio
        for i, bloque in enumerate(self.bloques):
            if len(bloque) < self.tamanio_bloque:
                bloque.append(clave)
                return {
                    'exito': True,
                    'mensaje': f'Clave {clave} insertada en bloque {i + 1}',
                    'bloque': i,
                    'posicion': len(bloque) - 1
                }

        return {'exito': False, 'mensaje': 'Error al insertar la clave'}

    def buscar_clave(self, clave):
        """
        Busca una clave en la estructura mediante búsqueda lineal

        Args:
            clave (int): Clave a buscar

        Returns:
            dict: Resultado de la búsqueda
        """
        if not self.bloques:
            return {
                'encontrada': False,
                'mensaje': 'La estructura no ha sido creada'
            }

        # Búsqueda lineal secuencial
        bloques_revisados = 0
        comparaciones = 0

        for i, bloque in enumerate(self.bloques):
            bloques_revisados += 1
            for j, valor in enumerate(bloque):
                comparaciones += 1
                if valor == clave:
                    return {
                        'encontrada': True,
                        'clave': clave,
                        'bloque': i,
                        'posicion': j,
                        'bloques_revisados': bloques_revisados,
                        'comparaciones': comparaciones,
                        'mensaje': f'Clave {clave} encontrada en bloque {i + 1}, posición {j + 1}'
                    }

        return {
            'encontrada': False,
            'clave': clave,
            'bloques_revisados': bloques_revisados,
            'comparaciones': comparaciones,
            'mensaje': f'Clave {clave} no encontrada'
        }

    def eliminar_clave(self, clave):
        """
        Elimina una clave y reacomoda las demás para no dejar espacios vacíos.
        """
        if not self.bloques:
            return {"exito": False, "mensaje": "No hay estructura creada."}

        # Buscar la clave
        for i, bloque in enumerate(self.bloques):
            if clave in bloque:
                # Guardar estado antes de modificar (para deshacer)
                self.guardar_estado()
                bloque.remove(clave)
                # Reacomodar todas las claves para eliminar huecos
                self.compactar_bloques()
                return {"exito": True, "mensaje": f"Clave {clave} eliminada correctamente y bloques reacomodados."}

        return {"exito": False, "mensaje": f"La clave {clave} no existe."}

    def compactar_bloques(self):
        """
        Reacomoda las claves en los bloques para eliminar huecos (corrimiento hacia la izquierda).
        Mantiene el tamaño de bloque (self.tamanio_bloque) y el número de bloques.
        """
        # Aplanar todas las claves existentes (ignorando None si existieran)
        todas = [x for bloque in self.bloques for x in bloque if x is not None]

        # Vaciar todos los bloques
        for bloque in self.bloques:
            bloque.clear()

        # Volver a llenarlos manteniendo el tamaño fijo por bloque
        idx = 0
        for bloque in self.bloques:
            for _ in range(self.tamanio_bloque):
                if idx < len(todas):
                    bloque.append(todas[idx])
                    idx += 1
                else:
                    # Si prefieres dejar bloques más cortos en vez de llenar con None,
                    # simplemente no hagas append cuando no hay más valores.
                    # Aquí uso append(None) solo si quieres representar huecos explícitos.
                    # En tu visualización actual es mejor dejar bloques cortos (sin None).
                    pass

    def guardar_estado(self):
        """Guarda el estado actual para la funcionalidad de deshacer"""
        # Hacer una copia profunda del estado actual
        estado = {
            'bloques': [bloque.copy() for bloque in self.bloques],
            'num_claves': self.num_claves,
            'tamanio_bloque': self.tamanio_bloque
        }
        self.historial.append(estado)

        # Limitar el historial a las últimas 10 operaciones
        if len(self.historial) > 10:
            self.historial.pop(0)

    def deshacer(self):
        """
        Deshace la última operación

        Returns:
            dict: Resultado de la operación
        """
        if not self.historial:
            return {
                'exito': False,
                'mensaje': 'No hay operaciones para deshacer'
            }

        # Restaurar el último estado guardado
        estado = self.historial.pop()
        self.bloques = estado['bloques']
        self.num_claves = estado['num_claves']
        self.tamanio_bloque = estado['tamanio_bloque']

        return {
            'exito': True,
            'mensaje': 'Operación deshecha correctamente',
            'bloques': self.bloques
        }

    def limpiar_estructura(self):
        """Limpia toda la estructura"""
        self.guardar_estado()
        self.bloques = []
        self.num_claves = 0
        self.tamanio_bloque = 0

        return {
            'exito': True,
            'mensaje': 'Estructura limpiada correctamente'
        }

    def exportar_estructura(self):
        """
        Exporta la estructura a un formato serializable

        Returns:
            dict: Estructura serializable
        """
        return {
            'num_claves': self.num_claves,
            'tamanio_bloque': self.tamanio_bloque,
            'bloques': self.bloques
        }

    def importar_estructura(self, datos):
        """
        Importa una estructura desde datos serializados

        Args:
            datos (dict): Datos de la estructura

        Returns:
            dict: Resultado de la operación
        """
        try:
            self.guardar_estado()
            self.num_claves = datos['num_claves']
            self.tamanio_bloque = datos['tamanio_bloque']
            self.bloques = datos['bloques']

            return {
                'exito': True,
                'mensaje': 'Estructura importada correctamente'
            }
        except Exception as e:
            return {
                'exito': False,
                'mensaje': f'Error al importar estructura: {str(e)}'
            }