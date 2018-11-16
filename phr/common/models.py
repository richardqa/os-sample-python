import uuid

from django.db import models
from django.utils import timezone


class TimeStampedModel(models.Model):
    """ Modelo abstracto TimeStamped """
    fecha_creacion = models.DateTimeField(
        blank=True, null=True, editable=False, auto_now_add=True)
    fecha_modificacion = models.DateTimeField(
        blank=True, null=True, editable=False, auto_now=True)

    def save(self, *args, **kwargs):
        if self.pk:
            self.fecha_modificacion = timezone.now()
        else:
            self.fecha_creacion = timezone.now()
            kwargs['force_insert'] = False
        super().save(*args, **kwargs)

    class Meta:
        abstract = True


class UUIDModel(models.Model):
    """ Modelo abstracto field uuid """
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    class Meta:
        abstract = True


class StatusModel(models.Model):
    """ Modelo abstracto boleano para el registro """
    es_removido = models.BooleanField(default=False, editable=False)

    class Meta:
        abstract = True


class BaseModel(UUIDModel, TimeStampedModel, StatusModel):
    """ Modelo Inherente para abstraer campos con uuid """

    class Meta:
        abstract = True


class BaseModel2(TimeStampedModel, StatusModel):
    """ Modelo Inherente para abstraer campos sin uuid """

    class Meta:
        abstract = True


class UUIDTimeStampedModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        abstract = True


class ConfiguracionConexionInternet(models.Model):
    """
    Modelo para configurar conexión a Internet.
    """
    con_conexion = models.BooleanField('Con conexión', default=True, help_text='Conexión disponible a Internet')
    ping_time = models.FloatField(default=150.0)

    class Meta:
        verbose_name = 'Configuración de conexión a Internet'
        verbose_name_plural = 'Configuración de conexión a Internet'

    def __str__(self):
        return "Editar configuración de conexión a Internet"
