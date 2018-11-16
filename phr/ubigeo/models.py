# coding=utf-8
from django.core.validators import RegexValidator
from django.db import models

REGION_GEOGRAFICA_CHOICES = (
    (1, "Costa"),
    (2, "Sierra"),
    (3, "Selva"),
    (4, "Lima Metropolitana"),
)
AREA_CHOICES = (
    (1, 'Urbano'),
    (2, 'Rural'),
)


class UbigeoContinente(models.Model):
    alpha2 = models.CharField(max_length=2)
    alpha3 = models.CharField(max_length=3)
    cod_ubigeo_reniec_continente = models.CharField(
        'Código Ubigeo Continente - RENIEC', max_length=2,
        validators=[
            RegexValidator(
                regex='^[0-9]{1,2}$',
                message='Numero de 1 o 2 digitos',
            ),
        ], null=False, blank=False)
    cod_ubigeo_inei_continente = models.CharField(
        'Código Ubigeo Continente - INEI', max_length=2,
        validators=[
            RegexValidator(
                regex='^[0-9]{1,2}$',
                message='Numero de 1 o 2 digitos',
            ),
        ], null=False, blank=False)
    ubigeo_continente = models.CharField(
        'Nombre Ubigeo Continente', max_length=100, null=False, blank=False)

    def __str__(self):
        return self.ubigeo_continente

    class Meta:
        verbose_name_plural = '1. Ubigeo Continentes'


class UbigeoPais(models.Model):
    alpha3 = models.CharField(max_length=3, null=True, blank=True)
    alpha2 = models.CharField(max_length=2, null=True, blank=True)
    cod_ubigeo_reniec_pais = models.CharField(
        'Código Ubigeo Pais - RENIEC', max_length=3,
        validators=[
            RegexValidator(
                regex='^[0-9]{1,3}$',
                message='Numero de 1 o 3 digitos',
            ),
        ], null=False, blank=False)
    cod_ubigeo_inei_pais = models.CharField(
        'Código Ubigeo Pais - INEI', max_length=3,
        validators=[
            RegexValidator(
                regex='^[0-9]{1,3}$',
                message='Numero de 1 o 3 digitos',
            ),
        ], null=False, blank=False)
    ubigeo_pais = models.CharField(
        'Nombre Ubigeo Pais', max_length=100, null=False, blank=False)
    continente = models.ForeignKey(
        UbigeoContinente,
        related_name='%(app_label)s_%(class)s_continente', null=True, blank=True)

    def __str__(self):
        return self.ubigeo_pais

    class Meta:
        verbose_name_plural = '2. Ubigeo Paises'


class UbigeoDepartamento(models.Model):
    cod_ubigeo_reniec_departamento = models.CharField(
        'Código Ubigeo Departamento - RENIEC', max_length=2,
        validators=[
            RegexValidator(
                regex='^[0-9]{2}$',
                message='Numero de 2 digitos',
            ),
        ], null=False, blank=False)
    cod_ubigeo_inei_departamento = models.CharField(
        'Código Ubigeo Departamento - INEI', max_length=2,
        validators=[
            RegexValidator(
                regex='^[0-9]{2}$',
                message='Numero de 2 digitos',
            ),
        ], null=False, blank=False)
    ubigeo_departamento = models.CharField(
        'Nombre Ubigeo Departamento', max_length=100, null=False, blank=False)
    continente = models.ForeignKey(
        UbigeoContinente,
        related_name='%(app_label)s_%(class)s_continente')
    pais = models.ForeignKey(
        UbigeoPais,
        related_name='%(app_label)s_%(class)s_pais')

    def __str__(self):
        return self.ubigeo_departamento

    class Meta:
        verbose_name_plural = '3. Ubigeo Departamentos'


class UbigeoProvincia(models.Model):
    cod_ubigeo_reniec_provincia = models.CharField(
        'Código Ubigeo Provincia - RENIEC', max_length=4,
        validators=[
            RegexValidator(
                regex='^[0-9]{4}$',
                message='Numero de 4 digitos',
            ),
        ], null=False, blank=False)
    cod_ubigeo_inei_provincia = models.CharField(
        'Código Ubigeo Provincia - INEI', max_length=4,
        validators=[
            RegexValidator(
                regex='^[0-9]{4}$',
                message='Numero de 4 digitos',
            ),
        ], null=False, blank=False)
    ubigeo_provincia = models.CharField(
        'Nombre Ubigeo Provincia', max_length=100, null=False, blank=False)
    continente = models.ForeignKey(
        UbigeoContinente,
        related_name='%(app_label)s_%(class)s_continente')
    pais = models.ForeignKey(
        UbigeoPais,
        related_name='%(app_label)s_%(class)s_pais')
    departamento = models.ForeignKey(
        UbigeoDepartamento,
        related_name='%(app_label)s_%(class)s_departamento')

    def __str__(self):
        return self.ubigeo_provincia

    class Meta:
        verbose_name_plural = '4. Ubigeo Provincias'

    @property
    def ubigeo_departamento(self):
        return self.departamento.ubigeo_departamento


class UbigeoDistrito(models.Model):
    cod_ubigeo_reniec_distrito = models.CharField(
        'Código Ubigeo Distrito - RENIEC', max_length=6,
        validators=[
            RegexValidator(
                regex='^[0-9]{6}$',
                message='Numero de 6 digitos',
            ),
        ], null=False, blank=False)
    cod_ubigeo_inei_distrito = models.CharField(
        'Código Ubigeo Distrito - INEI', max_length=6,
        validators=[
            RegexValidator(
                regex='^[0-9]{6}$',
                message='Numero de 6 digitos',
            ),
        ], null=False, blank=False)
    ubigeo_distrito = models.CharField(
        'Nombre Ubigeo Distrito', max_length=100, null=False, blank=False)
    continente = models.ForeignKey(
        UbigeoContinente,
        related_name='%(app_label)s_%(class)s_continente')
    pais = models.ForeignKey(
        UbigeoPais,
        related_name='%(app_label)s_%(class)s_pais')
    departamento = models.ForeignKey(
        UbigeoDepartamento,
        related_name='%(app_label)s_%(class)s_departamento')
    provincia = models.ForeignKey(
        UbigeoProvincia,
        related_name='%(app_label)s_%(class)s_provincia')
    l_inf = models.FloatField(null=True, blank=True)
    l_sup = models.FloatField(null=True, blank=True)
    pobreza = models.FloatField(null=True, blank=True)
    quintil_20 = models.PositiveSmallIntegerField(null=True, blank=True)
    area = models.PositiveSmallIntegerField(null=True, blank=True, choices=AREA_CHOICES)
    region = models.PositiveSmallIntegerField(null=True, blank=True, choices=REGION_GEOGRAFICA_CHOICES)
    tiene_friaje = models.BooleanField(default=False)

    def __str__(self):
        return self.ubigeo_distrito

    class Meta:
        verbose_name_plural = '5. Ubigeo Distritos'

    @property
    def ubigeo_departamento(self):
        return self.departamento.ubigeo_departamento

    @property
    def ubigeo_provincia(self):
        return self.provincia.ubigeo_provincia


class UbigeoLocalidad(models.Model):
    cod_ubigeo_reniec_localidad = models.CharField(
        'Código Ubigeo Localidad - RENIEC', max_length=9,
        validators=[
            RegexValidator(
                regex='^[0-9]{9}$',
                message='Numero de 9 digitos',
            ),
        ], null=False, blank=False)
    cod_ubigeo_inei_localidad = models.CharField(
        'Código Ubigeo Localidad - INEI', max_length=9,
        validators=[
            RegexValidator(
                regex='^[0-9]{9}$',
                message='Numero de 9 digitos',
            ),
        ], null=False, blank=False)
    ubigeo_localidad = models.CharField(
        'Nombre Ubigeo Localidad', max_length=100, null=False, blank=False)
    continente = models.ForeignKey(
        UbigeoContinente,
        related_name='%(app_label)s_%(class)s_continente')
    pais = models.ForeignKey(
        UbigeoPais,
        related_name='%(app_label)s_%(class)s_pais')
    departamento = models.ForeignKey(
        UbigeoDepartamento,
        related_name='%(app_label)s_%(class)s_departamento')
    provincia = models.ForeignKey(
        UbigeoProvincia,
        related_name='%(app_label)s_%(class)s_provincia')
    distrito = models.ForeignKey(
        UbigeoDistrito,
        related_name='%(app_label)s_%(class)s_distrito')

    def __str__(self):
        return self.ubigeo_localidad

    class Meta:
        verbose_name_plural = '6. Ubigeo Localidades'

    @property
    def ubigeo_departamento(self):
        return self.departamento.ubigeo_departamento

    @property
    def ubigeo_provincia(self):
        return self.provincia.ubigeo_provincia

    @property
    def ubigeo_distrito(self):
        return self.distrito.ubigeo_distrito
