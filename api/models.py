from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('operador', 'Operador'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='operador')

    def __str__(self):
        return f"{self.username} ({self.role})"


class Departamento(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Sensor(models.Model):
    STATE_CHOICES = (
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
        ('bloqueado', 'Bloqueado'),
        ('perdido', 'Perdido'),
    )

    uid = models.CharField(max_length=100, unique=True)   # UID/MAC único
    nombre = models.CharField(max_length=100, blank=True)
    descripcion = models.CharField(max_length=255, blank=True)
    estado = models.CharField(max_length=20, choices=STATE_CHOICES, default='inactivo')
    departamento = models.ForeignKey(Departamento, null=True, blank=True, on_delete=models.SET_NULL, related_name='sensores')
    usuario = models.ForeignKey('User', null=True, blank=True, on_delete=models.SET_NULL, related_name='sensores')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.uid} - {self.estado}"


class Evento(models.Model):
    ACTION_CHOICES = (
        ('intento', 'Intento'),
        ('abrir_manual', 'Abrir manual'),
        ('cerrar_manual', 'Cerrar manual'),
    )
    RESULT_CHOICES = (
        ('permitido', 'Permitido'),
        ('denegado', 'Denegado'),
    )

    sensor = models.ForeignKey(Sensor, null=True, blank=True, on_delete=models.SET_NULL, related_name='eventos')
    timestamp = models.DateTimeField(auto_now_add=True)
    accion = models.CharField(max_length=50, choices=ACTION_CHOICES)
    resultado = models.CharField(max_length=20, choices=RESULT_CHOICES)
    notas = models.TextField(blank=True)

    def __str__(self):
        return f"{self.accion} - {self.resultado} @ {self.timestamp}"
