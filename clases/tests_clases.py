import unittest
from paciente import Paciente
from especialidad import Especialidad
from medico import Medico

class TestPaciente(unittest.TestCase):
    def test_creacion_paciente(self):
        paciente = Paciente("Ana López", "98765432", "10/10/1985")
        self.assertEqual(paciente.obtener_dni(), "98765432")
        self.assertIn("Ana López", str(paciente))

class TestEspecialidad(unittest.TestCase):
    def test_verificar_dia_valido(self):
        esp = Especialidad("Dermatología", ["lunes", "miércoles"])
        self.assertTrue(esp.verificar_dia("lunes"))
        self.assertTrue(esp.verificar_dia("MiÉrColEs"))  # prueba con mayúsculas
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

if __name__ == '__main__':
    unittest.main()
