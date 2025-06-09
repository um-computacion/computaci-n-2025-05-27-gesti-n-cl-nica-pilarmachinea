class HistoriaClinica:
    def __init__(self, paciente):
        self.__paciente__ = paciente
        self.__turnos__ = []
        self.__recetas__ = []

    def agregar_turno(self, turno):
        self.__turnos__.append(turno)

    def agregar_receta(self, receta):
        self.__recetas__.append(receta)

    def obtener_turnos(self):
        return self.__turnos__.copy()

    def obtener_recetas(self):
        return self.__recetas__.copy()

    def __str__(self):
        resultado = f"Historia clínica de {self.__paciente__}\n\n"
        resultado += "Turnos:\n"
        if self.__turnos__:
            for t in self.__turnos__:
                resultado += f"  - {t}\n"
        else:
            resultado += "  (sin turnos registrados)\n"

        resultado += "\n Recetas:\n"
        if self.__recetas__:
            for r in self.__recetas__:
                resultado += f"  - {r}\n"
        else:
            resultado += "  (sin recetas registradas)\n"

        return resultado
