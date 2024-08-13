from django.test import TestCase
from .models import Usuario
from rest_framework.exceptions import ValidationError

class UsuarioModelTest(TestCase):

    def test_usuario_str(self):
        usuario = Usuario(first_name="Juan", last_name="Pérez")
        self.assertEqual(str(usuario), "Juan Pérez")

    def test_edad_negativa(self):
        usuario = Usuario(edad=-1)
        with self.assertRaises(ValidationError) as context:
            usuario.clean()
        self.assertIn("La edad no puede ser un número negativo.", str(context.exception))

    def test_edad_mayor_que_120(self):
        usuario = Usuario(edad=121)
        with self.assertRaises(ValidationError) as context:
            usuario.clean()
        self.assertIn("La edad no puede ser mayor que 120.", str(context.exception))

    def test_cpf_invalido_formato(self):
        usuario = Usuario(cpf="123456789")
        with self.assertRaises(ValidationError) as context:
            usuario.clean()
        self.assertIn("El CPF debe contener exactamente 11 dígitos.", str(context.exception))

    def test_cpf_invalido_digitos_verificadores(self):
        usuario = Usuario(cpf="12345678901")
        with self.assertRaises(ValidationError) as context:
            usuario.clean()
        self.assertIn("El CPF no es válido.", str(context.exception))

    def test_cpf_valido(self):
        usuario = Usuario(cpf="12345678909")  # Un CPF válido para la prueba
        try:
            usuario.clean()
        except ValidationError:
            self.fail("clean() raised ValidationError unexpectedly!")
