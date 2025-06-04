from especialidad import Especialidad

class Medico:
    def __init__(self, nombre: str, matricula: str):
        self.__nombre__ = nombre
        self.__matricula__ = matricula
        self.__especialidades__ = []

    def agregar_especialidad(self, especialidad: Especialidad):
        self.__especialidades__.append(especialidad)

    def obtener_matricula(self) -> str:
        return self.__matricula__

    def obtener_especialidad_para_dia(self, dia: str):
        for esp in self.__especialidades__:
            if esp.verificar_dia(dia):
                return esp.obtener_especialidad()
        return None

    def __str__(self):
        especialidades_str = "\n  ".join(str(e) for e in self.__especialidades__)
        return f"{self.__nombre__} (Matrícula: {self.__matricula__})\n  {especialidades_str}"
