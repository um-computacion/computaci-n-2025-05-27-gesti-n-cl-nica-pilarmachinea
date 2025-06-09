from datetime import datetime

class Receta:
    def __init__(self, paciente, medico, medicamentos):
        self.__paciente__ = paciente
        self.__medico__ = medico
        self.__medicamentos__ = medicamentos
        self.__fecha__ = datetime.now()

    def __str__(self):
        meds = ", ".join(self.__medicamentos__)
        return (
            f"Receta para {self.__paciente__} emitida por {self.__medico__} "
            f"el {self.__fecha__.strftime('%d/%m/%Y')}:\n  Medicamentos: {meds}"
        )
