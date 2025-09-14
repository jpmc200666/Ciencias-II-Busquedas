import json

class ManejadorArchivos:
    @staticmethod
    def guardar_json(nombre_archivo, datos):
        with open(nombre_archivo, "w", encoding="utf-8") as f:
            json.dump(datos, f, indent=4, ensure_ascii=False)

    @staticmethod
    def leer_json(nombre_archivo):
        try:
            with open(nombre_archivo, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}