import re
from django.contrib.auth.models import AbstractUser
from django.db import models
from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class Usuario(AbstractUser):
    """ Se definen edad y CPF en null=True y blank=True para poder crear el superusuario"""
    edad = models.IntegerField(null=True, blank=True)
    cpf = models.CharField(max_length=11, unique=True, null=True, blank=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def clean(self):
        super().clean()

        # Validar que la edad sea un número positivo y razonable
        if self.edad is not None:
            if self.edad < 0:
                raise ValidationError({'edad': _("La edad no puede ser un número negativo.")})
            if self.edad > 120:
                raise ValidationError({'edad': _("La edad no puede ser mayor que 120.")})

        # Validar el formato del CPF
        if self.cpf:
            if not re.match(r'^\d{11}$', self.cpf):
                raise ValidationError({'cpf': _("El CPF debe contener exactamente 11 dígitos.")})

            # Validar los dígitos verificadores del CPF
            def calcular_digito(cpf, peso):
                suma = sum(int(digito) * peso for digito, peso in zip(cpf, range(peso, 1, -1)))
                resto = suma % 11
                return 0 if resto < 2 else 11 - resto

            if (calcular_digito(self.cpf[:9], 10) != int(self.cpf[9]) or
                    calcular_digito(self.cpf[:10], 11) != int(self.cpf[10])):
                raise ValidationError({'cpf': _("El CPF no es válido.")})
