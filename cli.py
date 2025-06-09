from clases.paciente import Paciente
from clases.medico import Medico
from clases.especialidad import Especialidad
from clases.clinica import Clinica
from datetime import datetime
from clases.excepciones import PacienteNoEncontradoException, TurnoOcupadoException

class CLI:
    def __init__(self):
        self.clinica = Clinica()

    def mostrar_menu(self):
        while True:
            print("\n--- Menú Clínica ---")
            print("1) Agregar paciente")
            print("2) Agregar médico")
            print("3) Agendar turno")
            print("4) Agregar especialidad a médico")
            print("5) Emitir receta")
            print("6) Ver historia clínica")
            print("7) Ver todos los turnos")
            print("8) Ver todos los pacientes")
            print("9) Ver todos los médicos")
            print("0) Salir")

            opcion = input("Seleccioná una opción: ")

            try:
                match opcion:
                    case "1": self.agregar_paciente()
                    case "2": self.agregar_medico()
                    case "3": self.agendar_turno()
                    case "4": self.agregar_especialidad()
                    case "5": self.emitir_receta()
                    case "6": self.ver_historia_clinica()
                    case "7": self.ver_turnos()
                    case "8": self.ver_pacientes()
                    case "9": self.ver_medicos()
                    case "0": print("Saliendo..."); break
                    case _: print("Opción inválida.")
            except PacienteNoEncontradoException as e:
                print(f"Paciente no encontrado: {e}")
            except TurnoOcupadoException:
                print("El turno ya está ocupado.")
            except Exception as e:
                print(f"Error inesperado: {e}")


    def agregar_paciente(self):
        nombre = input("Nombre del paciente: ")
        dni = input("DNI: ")
        fecha = input("Fecha de nacimiento (dd/mm/aaaa): ")
        paciente = Paciente(nombre, dni, fecha)
        self.clinica.agregar_paciente(paciente)
        print("Paciente agregado.")

    def agregar_medico(self):
        nombre = input("Nombre del médico: ")
        matricula = input("Matrícula: ")
        medico = Medico(nombre, matricula)
        self.clinica.agregar_medico(medico)
        print("Médico agregado.")

    def agregar_especialidad(self):
        matricula = input("Matrícula del médico: ")
        medico = self.clinica.obtener_medico_por_matricula(matricula)
        if not medico:
            print("Médico no encontrado.")
            return
        tipo = input("Especialidad (ej: Pediatría): ")
        dias = input("Días de atención (separados por coma): ").split(",")
        dias = [d.strip().lower() for d in dias]
        especialidad = Especialidad(tipo, dias)
        medico.agregar_especialidad(especialidad)
        print("Especialidad agregada.")

    def agendar_turno(self):
        dni = input("DNI del paciente: ")
        matricula = input("Matrícula del médico: ")
        especialidad = input("Especialidad: ")
        fecha_str = input("Fecha y hora (dd/mm/aaaa HH:MM): ")
        fecha = datetime.strptime(fecha_str, "%d/%m/%Y %H:%M")
        self.clinica.agendar_turno(dni, matricula, especialidad, fecha)
        print("Turno agendado.")

    def emitir_receta(self):
        dni = input("DNI del paciente: ")
        matricula = input("Matrícula del médico: ")
        medicamentos = input("Medicamentos (separados por coma): ").split(",")
        medicamentos = [m.strip() for m in medicamentos]
        self.clinica.emitir_receta(dni, matricula, medicamentos)
        print("Receta emitida.")

    def ver_historia_clinica(self):
        dni = input("DNI del paciente: ")
        historia = self.clinica.obtener_historia_clinica(dni)
        print(historia)

    def ver_turnos(self):
        for turno in self.clinica.obtener_turnos():
            print(f"- {turno}")

    def ver_pacientes(self):
        for paciente in self.clinica.obtener_pacientes():
            print(f"- {paciente}")

    def ver_medicos(self):
        for medico in self.clinica.obtener_medicos():
            print(f"- {medico}")
