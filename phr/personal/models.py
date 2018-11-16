# coding=utf-8
from django.db import models

from phr.ciudadano.models import Ciudadano
from phr.establecimiento.models import Establecimiento


class TipoPersonal(models.Model):
    slug = models.SlugField(unique=True)
    tipo_personal = models.CharField(max_length=500)

    def __str__(self):
        return self.tipo_personal


class Personal(models.Model):
    ciudadano = models.OneToOneField(Ciudadano)
    tipo_personal = models.ForeignKey(TipoPersonal, null=True, blank=True)
    establecimientos = models.ManyToManyField(Establecimiento, blank=True)
    cmp = models.CharField(max_length=10, blank=True)
    rne = models.CharField(max_length=10, null=True, blank=True)
    inforhus = models.CharField(max_length=20, null=True, blank=True)
    especialidad = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        return self.ciudadano.nombre_completo


def actualiza_cache(sender, instance, **kwargs):
    from django_redis import get_redis_connection
    get_redis_connection("default").flushall()

# post_save.connect(actualiza_cache, sender=Personal)
