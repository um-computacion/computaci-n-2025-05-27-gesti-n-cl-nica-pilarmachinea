import unittest
from clases.paciente import Paciente
from clases.especialidad import Especialidad
from clases.medico import Medico
from clases.turno import Turno
from datetime import datetime
from clases.receta import Receta
from clases.historia_clinica import HistoriaClinica
from clases.clinica import Clinica


class TestPaciente(unittest.TestCase):
    def test_creacion_paciente(self):
        paciente = Paciente("Ana López", "98765432", "10/10/1985")
        self.assertEqual(paciente.obtener_dni(), "98765432")
        self.assertIn("Ana López", str(paciente))

class TestEspecialidad(unittest.TestCase):
    def test_verificar_dia_valido(self):
        esp = Especialidad("Dermatología", ["lunes", "miércoles"])
        self.assertTrue(esp.verificar_dia("lunes"))
        self.assertTrue(esp.verificar_dia("MiÉrColEs"))  
        self.assertFalse(esp.verificar_dia("viernes"))

    def test_str_especialidad(self):
        esp = Especialidad("Pediatría", ["lunes", "viernes"])
        self.assertIn("Pediatría", str(esp))
        self.assertIn("viernes", str(esp))

class TestMedico(unittest.TestCase):
    def test_agregar_especialidad_y_consulta_dia(self):
        esp = Especialidad("Neurología", ["jueves"])
        medico = Medico("Dr. Ruiz", "MAT456")
        medico.agregar_especialidad(esp)

        self.assertEqual(medico.obtener_matricula(), "MAT456")
        self.assertEqual(medico.obtener_especialidad_para_dia("jueves"), "Neurología")
        self.assertIsNone(medico.obtener_especialidad_para_dia("lunes"))

    def test_str_medico(self):
        esp = Especialidad("Clínica Médica", ["martes"])
        medico = Medico("Dra. Bianchi", "MAT789")
        medico.agregar_especialidad(esp)

        descripcion = str(medico)
        self.assertIn("Dra. Bianchi", descripcion)
        self.assertIn("Clínica Médica", descripcion)
        self.assertIn("martes", descripcion)

class TestTurno(unittest.TestCase):
    def test_turno_correcto(self):
        paciente = Paciente("Juan Test", "11222333", "01/01/2000")
        medico = Medico("Dr. Test", "MAT001")
        fecha = datetime(2025, 6, 10, 14, 30)
        turno = Turno(paciente, medico, fecha, "Cardiología")

        self.assertEqual(turno.obtener_medico(), medico)
        self.assertEqual(turno.obtener_fecha_hora(), fecha)
        self.assertIn("Cardiología", str(turno))
        self.assertIn("Juan Test", str(turno))

class TestReceta(unittest.TestCase):
    def test_receta_correcta(self):
        paciente = Paciente("Laura Test", "99887766", "02/02/1980")
        medico = Medico("Dr. Medicina", "MAT002")
        medicamentos = ["Ibuprofeno 400mg", "Paracetamol 500mg"]
        receta = Receta(paciente, medico, medicamentos)

        self.assertIn("Ibuprofeno", str(receta))
        self.assertIn("Dr. Medicina", str(receta))
        self.assertIn("Laura Test", str(receta))

class TestHistoriaClinica(unittest.TestCase):
    def test_agregar_turno_y_receta(self):
        paciente = Paciente("Carlos Clínica", "11112222", "03/03/1985")
        medico = Medico("Dra. Historial", "MAT999")
        historia = HistoriaClinica(paciente)

        turno = Turno(paciente, medico, datetime(2025, 6, 15, 9, 0), "Clínica Médica")
        receta = Receta(paciente, medico, ["Ibuprofeno", "Vitamina C"])

        historia.agregar_turno(turno)
        historia.agregar_receta(receta)

        self.assertEqual(len(historia.obtener_turnos()), 1)
        self.assertEqual(len(historia.obtener_recetas()), 1)
        self.assertIn("Clínica Médica", str(historia))
        self.assertIn("Ibuprofeno", str(historia))

class TestClinica(unittest.TestCase):
    def setUp(self):
        self.clinica = Clinica()
        self.paciente = Paciente("Test Paciente", "10000001", "01/01/1990")
        self.medico = Medico("Test Medico", "M001")
        self.especialidad = Especialidad("Clínica Médica", ["lunes", "miércoles"])
        self.medico.agregar_especialidad(self.especialidad)

    def test_agregar_paciente_y_medico(self):
        self.clinica.agregar_paciente(self.paciente)
        self.clinica.agregar_medico(self.medico)
        self.assertEqual(len(self.clinica.obtener_pacientes()), 1)
        self.assertEqual(len(self.clinica.obtener_medicos()), 1)

    def test_agendar_turno_exitoso(self):
        self.clinica.agregar_paciente(self.paciente)
        self.clinica.agregar_medico(self.medico)
        fecha = datetime(2025, 6, 9, 10, 0)  # lunes
        self.clinica.agendar_turno("10000001", "M001", "Clínica Médica", fecha)
        self.assertEqual(len(self.clinica.obtener_turnos()), 1)

    def test_emitir_receta_valida(self):
        self.clinica.agregar_paciente(self.paciente)
        self.clinica.agregar_medico(self.medico)
        self.clinica.emitir_receta("10000001", "M001", ["Ibuprofeno"])
        historia = self.clinica.obtener_historia_clinica("10000001")
        self.assertEqual(len(historia.obtener_recetas()), 1)

    def test_turno_duplicado_error(self):
        self.clinica.agregar_paciente(self.paciente)
        self.clinica.agregar_medico(self.medico)
        fecha = datetime(2025, 6, 9, 10, 0)  # lunes
        self.clinica.agendar_turno("10000001", "M001", "Clínica Médica", fecha)
        with self.assertRaises(Exception):
            self.clinica.agendar_turno("10000001", "M001", "Clínica Médica", fecha)

    def test_especialidad_incorrecta_error(self):
        self.clinica.agregar_paciente(self.paciente)
        self.clinica.agregar_medico(self.medico)
        fecha = datetime(2025, 6, 9, 10, 0)  # lunes
        with self.assertRaises(Exception):
            self.clinica.agendar_turno("10000001", "M001", "Cardiología", fecha)


if __name__ == '__main__':
    unittest.main()
