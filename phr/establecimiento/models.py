# coding=utf-8
from django.contrib.gis.db import models as models_gis
from django.db import models

from phr.common.models import BaseModel2
from phr.ubigeo.models import UbigeoContinente, UbigeoDepartamento, UbigeoDistrito, UbigeoPais, UbigeoProvincia


class Diresa(BaseModel2):
    nombre = models.CharField('Nombre', max_length=100)
    codigo = models.CharField(blank=True, max_length=3, null=True)
    departamento = models.ForeignKey(UbigeoDepartamento, null=True)
    es_activo = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Diresas'

    def __str__(self):
        return self.nombre

    def get_departamento(self):
        if self.departamento is not None:
            return self.departamento
        else:
            if self.nombre.startswith('LIMA'):
                diresa_nombre = self.nombre.split(' ')[0].capitalize()
            else:
                diresa_nombre = self.nombre.capitalize()
                if diresa_nombre == 'Ancash':
                    diresa_nombre = 'Áncash'
                elif diresa_nombre == 'Apurimac':
                    diresa_nombre = 'Apurímac'
                elif diresa_nombre == 'Huanuco':
                    diresa_nombre = 'Huánuco'
                elif diresa_nombre == 'Junin':
                    diresa_nombre = 'Junín'
                elif diresa_nombre == 'San martin':
                    diresa_nombre = 'San Martín'
            try:
                departamento = UbigeoDepartamento.objects.get(
                    ubigeo_departamento__istartswith=diresa_nombre)
                self.departamento = departamento
                self.save()
            except Exception as ex:
                print(ex)
                departamento = None
            return departamento

    @property
    def departamento_nombre(self):
        departamento = self.get_departamento()
        return departamento.ubigeo_departamento

    @property
    def departamento_ubigeo_inei(self):
        departamento = self.get_departamento()
        return departamento.cod_ubigeo_inei_departamento

    @property
    def departamento_ubigeo_reniec(self):
        departamento = self.get_departamento()
        return departamento.cod_ubigeo_reniec_departamento


class Red(BaseModel2):
    diresa = models.ForeignKey(Diresa, related_name='%(app_label)s_%(class)s_diresa')
    codigo = models.CharField(max_length=2, null=True, blank=True)
    nombre = models.CharField('Nombre', max_length=100, null=False)

    class Meta:
        verbose_name_plural = 'Redes'

    def __str__(self):
        return self.nombre

    @property
    def diresa_nombre(self):
        return self.diresa.nombre

    @property
    def diresa_codigo(self):
        return self.diresa.codigo


class Microred(BaseModel2):
    diresa = models.ForeignKey(Diresa, related_name='%(app_label)s_%(class)s_diresa')
    red = models.ForeignKey(Red, related_name='%(app_label)s_%(class)s_red')
    codigo = models.CharField(max_length=2, null=True, blank=True)
    nombre = models.CharField('Nombre', max_length=100)

    class Meta:
        verbose_name_plural = 'Micro-Redes'

    def __str__(self):
        return self.nombre

    @property
    def red_codigo(self):
        return self.red.codigo

    @property
    def red_nombre(self):
        return self.red.nombre

    @property
    def diresa_codigo(self):
        return self.diresa.codigo

    @property
    def diresa_nombre(self):
        return self.diresa.nombre


class EstablecimientoCategoria(BaseModel2):
    nombre_categoria = models.CharField(verbose_name='nombre categoria', max_length=15)
    categoria_nivel = models.IntegerField(verbose_name='nivel establecimiento', blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Establecimiento Categoria'

    def __str__(self):
        return self.nombre_categoria


class Servicio(models.Model):
    SERVICIO_ESTADO_CHOICES = (
        (0, 'Inactivo'),
        (1, 'Activo'),
    )
    codigo = models.CharField(max_length=6)
    descripcion = models.CharField(max_length=120)
    estado = models.PositiveSmallIntegerField(choices=SERVICIO_ESTADO_CHOICES)

    def __str__(self):
        return "{} - {}".format(self.codigo, self.descripcion)


class EstablecimientoSector(BaseModel2):
    codigo = models.CharField(max_length=2, unique=True)
    descripcion = models.CharField(max_length=60)

    def __str__(self):
        return self.descripcion

    def save(self, raw=False, force_insert=False,
             force_update=False, using=None, update_fields=None):
        return super().save()


class Establecimiento(BaseModel2):
    codigo_renaes = models.CharField('código Renaes', max_length=8)
    nombre = models.CharField('nombre', max_length=150)
    telefono = models.CharField('teléfono', max_length=80, blank=True)
    direccion = models.TextField('dirección', blank=True, null=True)
    horario_atencion = models.CharField('Horario de atención', max_length=100, blank=True, null=True)
    descripcion = models.TextField(
        'Descripción', max_length=150, blank=True, null=True)
    sector = models.ForeignKey(EstablecimientoSector, default=1)
    codigo_his = models.CharField(
        'Código HIS', max_length=10, null=True, blank=True)
    lote = models.SmallIntegerField('lote', blank=True, null=True, default=0)
    location = models_gis.PointField(
        "longitude/latitude", geography=True, null=True, blank=True)
    categoria = models.ForeignKey(
        EstablecimientoCategoria, blank=True, null=True, related_name='%(app_label)s_%(class)s_categoria')
    diresa = models.ForeignKey(
        Diresa, related_name='%(app_label)s_%(class)s_diresa', blank=True, null=True)
    red = models.ForeignKey(Red, related_name='%(app_label)s_%(class)s_red', blank=True, null=True)
    microred = models.ForeignKey(
        Microred, related_name='%(app_label)s_%(class)s_microred', blank=True, null=True)
    ubigeo = models.CharField(verbose_name='ubigeo', max_length=8, blank=True, null=True)
    continente = models.ForeignKey(
        UbigeoContinente, related_name='%(app_label)s_%(class)s_continente', null=True, blank=True)
    pais = models.ForeignKey(
        UbigeoPais, related_name='%(app_label)s_%(class)s_pais', null=True, blank=True)
    departamento = models.ForeignKey(
        UbigeoDepartamento, related_name='%(app_label)s_%(class)s_departamento', null=True, blank=True)
    distrito = models.ForeignKey(
        UbigeoDistrito, related_name='%(app_label)s_%(class)s_distrito', null=True, blank=True)
    provincia = models.ForeignKey(
        UbigeoProvincia, related_name='%(app_label)s_%(class)s_provincia', null=True, blank=True)
    servicios = models.ManyToManyField(Servicio, blank=True)
    objects = models_gis.GeoManager()
    tiene_influenza = models.BooleanField(default=False)
    es_para_anemia = models.BooleanField(default=False)
    es_banco_sangre = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = 'Establecimientos'

    def save(self, *args, **kwargs):
        if self.ubigeo is None and self.distrito is not None:
            self.ubigeo = self.distrito.cod_ubigeo_inei_distrito
        return super().save(*args, **kwargs)

    @property
    def sector_codigo(self):
        return self.sector.codigo

    @property
    def microred_nombre(self):
        return self.microred.nombre

    @property
    def categoria_nombre(self):
        return self.categoria.nombre_categoria

    @property
    def categoria_nivel(self):
        return self.categoria.categoria_nivel

    @property
    def get_codigo_renaes(self):
        return '{:08}'.format(int(self.codigo_renaes))

    @property
    def nombre_microred(self):
        return '{} ({})'.format(self.nombre, self.microred.nombre)

    @property
    def nombre_ambito(self):
        try:
            if self.diresa and self.diresa.nombre:
                return '{} ({}/{}/{})'.format(self.nombre, self.diresa.nombre, self.red.nombre, self.microred.nombre)
            elif self.departamento_nombre and self.provincia_nombre and self.distrito_nombre:
                return '{} ({}/{}/{})'.format(self.nombre, self.departamento_nombre, self.provincia_nombre,
                                              self.distrito_nombre)
            else:
                return self.nombre
        except AttributeError:
            return self.nombre

    @property
    def departamento_nombre(self):
        return '{}'.format(self.departamento.ubigeo_departamento)

    @property
    def provincia_nombre(self):
        return '{}'.format(self.provincia.ubigeo_provincia)

    @property
    def distrito_nombre(self):
        return '{}'.format(self.distrito.ubigeo_distrito)

    @property
    def red_nombre(self):
        return self.red.nombre

    @property
    def diresa_nombre(self):
        return self.diresa.nombre

    @property
    def diresa_codigo(self):
        return self.diresa.codigo

    @property
    def red_codigo(self):
        return self.red.codigo

    @property
    def microred_codigo(self):
        return self.microred.codigo

    @property
    def sector_nombre(self):
        return self.sector.descripcion

    @property
    def servicios_estab(self):
        return [{'codigo': serv.codigo, 'descripcion': serv.descripcion} for serv in self.servicios.all()]
