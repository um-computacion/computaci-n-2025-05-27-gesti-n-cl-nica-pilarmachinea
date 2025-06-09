from clases.historia_clinica import HistoriaClinica
from clases.turno import Turno
from clases.receta import Receta
from datetime import datetime
from clases.excepciones import PacienteNoEncontradoException, MedicoNoEncontradoException, TurnoOcupadoException, MedicoNoDisponibleException, EspecialidadNoCoincideException, RecetaInvalidaException


class Clinica:
    def __init__(self):
        self.__pacientes__ = {}  
        self.__medicos__ = {}   
        self.__turnos__ = []
        self.__historias_clinicas__ = {}

    def agregar_paciente(self, paciente):
        dni = paciente.obtener_dni()
        if dni in self.__pacientes__:
            raise Exception("Paciente ya registrado.")
        self.__pacientes__[dni] = paciente
        self.__historias_clinicas__[dni] = HistoriaClinica(paciente)

    def agregar_medico(self, medico):
        matricula = medico.obtener_matricula()
        if matricula in self.__medicos__:
            raise Exception("Médico ya registrado.")
        self.__medicos__[matricula] = medico

    def obtener_pacientes(self):
        return list(self.__pacientes__.values())

    def obtener_medicos(self):
        return list(self.__medicos__.values())

    def obtener_medico_por_matricula(self, matricula):
        return self.__medicos__.get(matricula)


    def agendar_turno(self, dni, matricula, especialidad, fecha_hora):
        self.validar_existencia_paciente(dni)
        self.validar_existencia_medico(matricula)
        self.validar_turno_no_duplicado(matricula, fecha_hora)

        medico = self.__medicos__[matricula]
        dia_semana = self.obtener_dia_semana_en_espanol(fecha_hora)
        self.validar_especialidad_en_dia(medico, especialidad, dia_semana)

        paciente = self.__pacientes__[dni]
        turno = Turno(paciente, medico, fecha_hora, especialidad)
        self.__turnos__.append(turno)
        self.__historias_clinicas__[dni].agregar_turno(turno)

    def obtener_turnos(self):
        return self.__turnos__

    def emitir_receta(self, dni, matricula, medicamentos):
        self.validar_existencia_paciente(dni)
        self.validar_existencia_medico(matricula)

        if not medicamentos:
            raise RecetaInvalidaException("La receta debe tener al menos un medicamento.")

        paciente = self.__pacientes__[dni]
        medico = self.__medicos__[matricula]
        receta = Receta(paciente, medico, medicamentos)
        self.__historias_clinicas__[dni].agregar_receta(receta)

    def obtener_historia_clinica(self, dni):
        self.validar_existencia_paciente(dni)
        return self.__historias_clinicas__[dni]

    def validar_existencia_paciente(self, dni):
        if dni not in self.__pacientes__:
            raise PacienteNoEncontradoException("Paciente no encontrado.")

    def validar_existencia_medico(self, matricula):
        if matricula not in self.__medicos__:
            raise MedicoNoEncontradoException("Médico no encontrado.")

    def validar_turno_no_duplicado(self, matricula, fecha_hora):
        for turno in self.__turnos__:
            if turno.obtener_medico().obtener_matricula() == matricula and turno.obtener_fecha_hora() == fecha_hora:
                raise TurnoOcupadoException("Ese turno ya está ocupado.")

    def obtener_dia_semana_en_espanol(self, fecha_hora):
        dias = ['lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo']
        return dias[fecha_hora.weekday()]

    def validar_especialidad_en_dia(self, medico, especialidad_solicitada, dia_semana):
        especialidad_real = medico.obtener_especialidad_para_dia(dia_semana)
        if especialidad_real is None:
            raise MedicoNoDisponibleException("El médico no atiende ese día.")
        if especialidad_real.lower() != especialidad_solicitada.lower():
            raise EspecialidadNoCoincideException("El médico no atiende esa especialidad ese día.")
