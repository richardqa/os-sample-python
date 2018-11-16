from django.contrib.gis.db import models as models_gis
from django.db import models

from phr.common.constants import NIVEL_INSTEDUC, TIPO_INSTEDUC
from phr.establecimiento.models import Establecimiento


class InstitucionEducativa(models.Model):
    nombre = models.CharField('Nombre', max_length=255, blank=True, null=True)
    codigo_modular = models.CharField('Código modular', max_length=15, unique=True)
    codigo_colegio = models.CharField('Código colegio', max_length=15, unique=True)
    ubigeo = models.CharField('Ubigeo', max_length=10, blank=True, null=True)
    nombre_ugel = models.CharField('Ugel', max_length=150, blank=True, null=True)
    direccion = models.CharField('Dirección', max_length=255, blank=True, null=True)
    establecimiento = models.ForeignKey(Establecimiento, blank=True, null=True)
    tipo = models.CharField(max_length=1, choices=TIPO_INSTEDUC, default='3')
    nivel = models.CharField(max_length=1, choices=NIVEL_INSTEDUC, default='3')
    ubicacion = models_gis.PointField("longitud/latitud", geography=True, null=True, blank=True)

    def __str__(self):
        return '{} - {} - {}'.format(self.nombre, self.direccion, self.get_nivel_display())

    @property
    def nivel_descripcion(self):
        return self.get_nivel_display()

    @property
    def tipo_descripcion(self):
        return self.get_tipo_display()

    @property
    def establecimiento_renaes(self):
        if self.establecimiento:
            return self.establecimiento.codigo_renaes
        else:
            return '-'

    @property
    def establecimiento_nombre(self):
        if self.establecimiento:
            return self.establecimiento.nombre
        else:
            return '-'
