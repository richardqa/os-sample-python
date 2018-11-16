import re

from django.contrib.postgres.fields.array import ArrayField
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models
from django.utils import timezone

from dateutil.relativedelta import relativedelta
from multiselectfield import MultiSelectField

from phr.catalogo.models import CatalogoCIE
from phr.common import constants as core_constants
from phr.common.constants import (
    GRUPO_ANTECEDENTES_CHOICES, GRUPO_ANTECEDENTES_FAMILIARES, GRUPO_ANTECEDENTES_PERSONALES, ORIGEN_DATA_CHOICES,
    ORIGEN_DATA_CREADO, ORIGEN_DATA_IMPORTADO, ORIGEN_DATA_MIGRACIONES, ORIGEN_DATA_RENIEC, PARENTESCO_CHOICES,
    REGISTRO_ANTECEDENTE_CHOICES, REGISTRO_ANTECEDENTE_POSITIVO, SUBGRUPO_ANTECEDENTES_CHOICES,
    TIPO_ANTECEDENTE_CHOICES, TIPO_ANTECEDENTE_PERSONAL, TIPODOC_CARNET_EXTRANJERIA, TIPODOC_DNI,
    ETNIA_MESTIZO)
from phr.common.models import BaseModel, ConfiguracionConexionInternet, UUIDTimeStampedModel
from phr.ubigeo.models import (
    UbigeoContinente, UbigeoDepartamento, UbigeoDistrito, UbigeoLocalidad, UbigeoPais, UbigeoProvincia,
)


class Ciudadano(BaseModel):
    cui = models.CharField('N° CUI', max_length=10, null=True, blank=True)
    nombres = models.CharField('Nombres', max_length=100, null=True, blank=True)
    apellido_paterno = models.CharField('Apellido paterno', max_length=100, null=True, blank=True)
    apellido_materno = models.CharField('Apellido materno', max_length=100, null=True, blank=True)
    tipo_documento = models.CharField(
        'Tipo de documento', max_length=2, choices=core_constants.TDOC_CHOICES, null=True, blank=True)
    tipo_documento_minsa = models.CharField(
        'Tipo de documento', max_length=1, choices=core_constants.TDOC_CHOICES_HISMINSA, null=True, blank=True)
    numero_documento = models.CharField('Número de documento', max_length=15, null=True, blank=True, db_index=True)
    fecha_nacimiento = models.DateField('Fecha de nacimiento', blank=True, null=True)
    sexo = models.CharField("Sexo", max_length=1, null=True, blank=True, choices=core_constants.SEXO_CHOICES)
    correo = models.EmailField('Correo', null=True, blank=True)
    telefono = models.CharField('Teléfono', max_length=10, null=True, blank=True)
    celular = models.CharField('Celular', max_length=10, null=True, blank=True)

    domicilio_direccion = models.CharField('Domicilio Direccion', max_length=500, null=True, blank=True)
    domicilio_referencia = models.CharField('Domicilio Referencia', max_length=500, null=True, blank=True)
    continente_domicilio = models.ForeignKey(
        UbigeoContinente, related_name='%(app_label)s_%(class)s_continente_domicilio', null=True, blank=True)
    pais_domicilio = models.ForeignKey(
        UbigeoPais, related_name='%(app_label)s_%(class)s_pais_domicilio', null=True, blank=True)
    departamento_domicilio = models.ForeignKey(
        UbigeoDepartamento, related_name='%(app_label)s_%(class)s_departamento_domicilio', null=True, blank=True)
    provincia_domicilio = models.ForeignKey(
        UbigeoProvincia, related_name='%(app_label)s_%(class)s_provincia_domicilio', null=True, blank=True)
    distrito_domicilio = models.ForeignKey(
        UbigeoDistrito, related_name='%(app_label)s_%(class)s_distrito_domicilio', null=True, blank=True)
    localidad_domicilio = models.ForeignKey(
        UbigeoLocalidad, related_name='%(app_label)s_%(class)s_localidad_domicilio', null=True, blank=True)

    domicilio_direccion_actual = models.CharField('Direccion Actual', max_length=500, null=True, blank=True)
    domicilio_referencia_actual = models.CharField(
        'Domicilio Referencia Actual', max_length=500, null=True, blank=True)
    pais_domicilio_actual = models.ForeignKey(
        UbigeoPais, related_name='pais_domicilio_actual', null=True, blank=True)
    departamento_domicilio_actual = models.ForeignKey(
        UbigeoDepartamento, related_name='departamento_domicilio_actual', null=True, blank=True)
    provincia_domicilio_actual = models.ForeignKey(
        UbigeoProvincia, related_name='provincia_domicilio_actual', null=True, blank=True)
    distrito_domicilio_actual = models.ForeignKey(
        UbigeoDistrito, related_name='distrito_domicilio_actual', null=True, blank=True)
    localidad_domicilio_actual = models.ForeignKey(
        UbigeoLocalidad, related_name='localidad_domicilio_actual', null=True, blank=True)

    pais_origen = models.ForeignKey(UbigeoPais, blank=True, null=True, related_name="pais_origen")
    nacimiento_ubigeo = models.CharField('Nacimiento Ubigeo', max_length=10, null=True, blank=True)
    departamento_nacimiento = models.ForeignKey(
        UbigeoDepartamento, related_name='%(app_label)s_%(class)s_departamento_nacimiento', null=True, blank=True)
    provincia_nacimiento = models.ForeignKey(
        UbigeoProvincia, related_name='%(app_label)s_%(class)s_provincia_nacimiento', null=True, blank=True)
    distrito_nacimiento = models.ForeignKey(
        UbigeoDistrito, related_name='%(app_label)s_%(class)s_distrito_nacimiento', null=True, blank=True)

    estado_civil = models.CharField(
        'Estado civil', max_length=2, choices=core_constants.ESTADO_CIVIL_CHOICES, default='1', null=True, blank=True)
    etnia = models.CharField('Etnia', max_length=2, choices=core_constants.ETNIA_CHOICES, default=ETNIA_MESTIZO)
    lengua = models.CharField('Lengua', max_length=10, choices=core_constants.LENGUA_CHOICES, null=True, blank=True)
    tipo_seguro = models.CharField(
        'Tipo de seguro', choices=core_constants.FINANCIADOR_CHOICES, null=True, blank=True, max_length=2)
    codigo_asegurado = models.CharField(
        'Código de asegurado', max_length=24, null=True, blank=True)
    grado_instruccion = models.CharField(
        max_length=4, choices=core_constants.GI_CHOICES, null=True, blank=True)
    ocupacion = models.CharField(
        max_length=2, choices=core_constants.OCUPACION_CHOICES, null=True, blank=True)
    estado = models.CharField(
        'Estado', max_length=1, choices=core_constants.STATUS_MODEL, null=True, blank=True, default='1')
    foto = models.TextField(null=True, blank=True)
    origen_datos = models.PositiveSmallIntegerField(
        default=ORIGEN_DATA_CREADO, choices=ORIGEN_DATA_CHOICES, null=True, blank=True)
    ultima_actualizacion_tipo_seguro = models.DateField(editable=False, blank=True, null=True)
    es_persona_viva = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Ciudadano"
        verbose_name_plural = "Ciudadanos"

        unique_together = ['tipo_documento', 'numero_documento']

    def __str__(self):
        return self.nombre_completo

    def save(self, *args, **kwargs):
        conexion_internet = ConfiguracionConexionInternet.objects.first()
        if (self.origen_datos not in (ORIGEN_DATA_RENIEC, ORIGEN_DATA_MIGRACIONES, ORIGEN_DATA_IMPORTADO) and
                conexion_internet):
            if self.tipo_documento == TIPODOC_DNI and conexion_internet.con_conexion:
                raise Exception("No puede crear un ciudadano con DNI al usar conexión a RENIEC")
            if self.tipo_documento == TIPODOC_CARNET_EXTRANJERIA and conexion_internet.con_conexion:
                raise Exception("No puede crear un ciudadano con carnet de extranjería al usar conexión a MIGRACIONES")
        elif (self.numero_documento and self.tipo_documento and not self.numero_documento.startswith("SD")
              and not re.match(r"^\d{6,15}$", self.numero_documento)):
            raise Exception("El número de documento debe ser numérico entre 6 y 15 caracteres.")
        if self.estado_civil == '' or self.estado_civil is None:
            self.estado_civil = '1'
        if self.domicilio_direccion:
            self.domicilio_direccion = self.domicilio_direccion.replace("SIN DATOS", "-").strip()
        if not self.tipo_documento and self.numero_documento and re.match(r"^\d{8}$", self.numero_documento):
            self.tipo_documento = '01'
            self.tipo_documento_minsa = '1'
        if self.pais_origen is None and self.departamento_nacimiento:
            self.pais_origen = self.departamento_nacimiento.pais
        if self.cui:
            try:
                ciudadano_rn = CiudadanoRN.objects.get(cui=self.cui, es_ficha_activa=True)
                ciudadano_rn.ciudadano = self
                if self.tipo_documento == TIPODOC_DNI and re.match(r'^\d{8}$', self.numero_documento):
                    ciudadano_rn.numero_dni_ciudadano = self.numero_documento
                ciudadano_rn.save(crear_ciudadano=False)
            except CiudadanoRN.DoesNotExist:
                pass
        self.registrar_historial_direccion_actual()
        if (self.nacimiento_ubigeo and self.distrito_nacimiento and
                self.nacimiento_ubigeo != self.distrito_nacimiento.cod_ubigeo_reniec_distrito):
            self.nacimiento_ubigeo = self.distrito_nacimiento.cod_ubigeo_reniec_distrito
        super().save()

    @property
    def nombre_completo(self):
        return "{0} {1} {2}".format(self.nombres, self.apellido_paterno, self.apellido_materno)

    @property
    def edad(self):
        try:
            return relativedelta(timezone.now().date(), self.fecha_nacimiento)
        except Exception:
            return ''

    @property
    def edad_anios(self):
        try:
            return self.edad.years
        except Exception:
            return ""

    @property
    def edad_meses(self):
        try:
            return self.edad.months
        except Exception:
            return ""

    @property
    def edad_dias(self):
        try:
            return self.edad.days
        except Exception:
            return ""

    @property
    def edad_str(self):
        try:
            edad = relativedelta(timezone.now().date(), self.fecha_nacimiento)
            txt_anios = '{} {}'.format(edad.years or 0, edad.years == 1 and 'año' or 'años')
            txt_meses = '{} {}'.format(edad.months or 0, edad.months == 1 and 'mes' or 'meses')
            txt_dias = '{} {}'.format(edad.days or 0, edad.days == 1 and 'día' or 'días')
            txt_tiempo = '{}, {}, {}.'.format(txt_anios, txt_meses, txt_dias)
            return txt_tiempo
        except Exception as ex:
            return ""

    @property
    def etnia_descripcion(self):
        return self.get_etnia_display

    @property
    def get_ubigeo_nacimiento(self):
        if self.nacimiento_ubigeo is None or len(self.nacimiento_ubigeo) <= 4:
            self.nacimiento_ubigeo = self.distrito_nacimiento.cod_ubigeo_reniec_distrito
            self.save()
        return self.nacimiento_ubigeo

    @property
    def get_departamento_domicilio_ubigeo_reniec(self):
        return self.departamento_domicilio.cod_ubigeo_reniec_departamento

    @property
    def get_provincia_domicilio_ubigeo_reniec(self):
        return self.provincia_domicilio.cod_ubigeo_reniec_provincia

    @property
    def get_distrito_domicilio_ubigeo_reniec(self):
        return self.distrito_domicilio.cod_ubigeo_reniec_distrito

    @property
    def get_departamento_domicilio_ubigeo_inei(self):
        return self.departamento_domicilio.cod_ubigeo_inei_departamento

    @property
    def get_provincia_domicilio_ubigeo_inei(self):
        return self.provincia_domicilio.cod_ubigeo_inei_provincia

    @property
    def get_distrito_domicilio_ubigeo_inei(self):
        return self.distrito_domicilio.cod_ubigeo_inei_distrito

    @property
    def get_departamento_domicilio_nombre(self):
        return self.departamento_domicilio.ubigeo_departamento

    @property
    def get_provincia_domicilio_nombre(self):
        return self.provincia_domicilio.ubigeo_provincia

    @property
    def get_distrito_domicilio_nombre(self):
        return self.distrito_domicilio.ubigeo_distrito

    @property
    def get_departamento_nacimiento_nombre(self):
        return self.departamento_nacimiento.ubigeo_departamento

    @property
    def get_provincia_nacimiento_nombre(self):
        return self.provincia_nacimiento.ubigeo_provincia

    @property
    def get_distrito_nacimiento_nombre(self):
        return self.distrito_nacimiento.ubigeo_distrito

    @property
    def uid(self):
        return self.uuid

    @property
    def tiempo_desde_ultima_actualizacion(self):
        return relativedelta(timezone.now().date(), self.fecha_modificacion)

    def registrar_historial_direccion_actual(self):
        try:
            datos_ciudadano = Ciudadano.objects.get(
                tipo_documento=self.tipo_documento, numero_documento=self.numero_documento)
        except (Ciudadano.DoesNotExist, Ciudadano.MultipleObjectsReturned):
            datos_ciudadano = self

        if datos_ciudadano.domicilio_direccion_actual != self.domicilio_direccion_actual:
            DomicilioCiudadanoHistorial.objects.create(
                domicilio_direccion=datos_ciudadano.domicilio_direccion_actual,
                domicilio_referencia=datos_ciudadano.domicilio_referencia_actual,
                pais_domicilio=datos_ciudadano.pais_domicilio_actual,
                departamento_domicilio=datos_ciudadano.departamento_domicilio_actual,
                provincia_domicilio=datos_ciudadano.provincia_domicilio_actual,
                distrito_domicilio=datos_ciudadano.distrito_domicilio_actual,
                ciudadano=datos_ciudadano,
            )


class DomicilioCiudadanoHistorial(models.Model):
    domicilio_direccion = models.CharField(max_length=500, null=True, blank=True)
    domicilio_referencia = models.CharField(max_length=500, null=True, blank=True)
    pais_domicilio = models.ForeignKey(UbigeoPais, null=True, blank=True)
    departamento_domicilio = models.ForeignKey(UbigeoDepartamento, null=True, blank=True)
    provincia_domicilio = models.ForeignKey(UbigeoProvincia, null=True, blank=True)
    distrito_domicilio = models.ForeignKey(UbigeoDistrito, null=True, blank=True)
    localidad_domicilio = models.ForeignKey(UbigeoLocalidad, null=True, blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    ciudadano = models.ForeignKey(Ciudadano, on_delete=models.CASCADE)

    def __str__(self):
        return "{} - {}".format(self.ciudadano.nombre_completo, self.domicilio_direccion)


class CiudadanoRN(BaseModel):
    cui = models.CharField('N° CUI', primary_key=True, max_length=10, null=False, blank=False)
    codigo_renaes = models.CharField('Código Renaes', max_length=8, null=True, blank=True)
    hci = models.CharField(max_length=20, blank=True, null=True)
    fecha_nacimiento = models.DateField('Fecha de nacimiento', blank=True, null=True)
    hora_nacimiento = models.TimeField('Hora de nacimiento', blank=True, null=True)
    sexo_nacido = models.CharField(
        "Sexo Nacido", max_length=2, null=True, blank=True,
        choices=core_constants.SEXO_CHOICES)
    nombre_nacido = models.CharField("Nombre RN", max_length=250, null=True, blank=True)
    peso_nacido = models.PositiveIntegerField(
        "Peso Nacido", validators=[MinValueValidator(300), MaxValueValidator(5000)], null=True, blank=True)

    talla_nacido = models.DecimalField(
        max_digits=4, decimal_places=2,
        validators=[MinValueValidator(25), MaxValueValidator(99)], null=True, blank=True)

    numero_temperatura = models.PositiveSmallIntegerField(
        validators=[RegexValidator(regex='^[0-9]{1,2}$', message='Número de 2 digitos'),
                    MinValueValidator(30, MaxValueValidator(50))],
        null=True, blank=True)
    resultado_examen_fisico = models.CharField(
        max_length=2, validators=[RegexValidator(regex='^[0-9]{2}$', message='Número de 2 digitos')],
        choices=core_constants.REF_CHOICES, null=True, blank=True)

    edad_examen_fisico = models.CharField(max_length=2, null=True, blank=True)

    unida_medida_edad = models.CharField(max_length=2, null=True, blank=True, choices=core_constants.UM_EDAD_CHOICES)

    numero_nacido_perim_cefalico = models.DecimalField(
        max_digits=4, decimal_places=2, null=True, blank=True,
        validators=[MinValueValidator(20), MaxValueValidator(50)])

    numero_nacido_perim_toracico = models.DecimalField(
        max_digits=4, decimal_places=2, null=True, blank=True,
        validators=[MinValueValidator(20), MaxValueValidator(50)])

    apgar_uno_nacido = models.PositiveSmallIntegerField(
        "Apgar 1", validators=[MinValueValidator(0), MaxValueValidator(10)], null=True, blank=True)

    apgar_cinco_nacido = models.PositiveSmallIntegerField(
        "Apgar 5", validators=[MinValueValidator(0), MaxValueValidator(10)], null=True, blank=True)

    etnia_nacido = models.CharField('Etnia RN', max_length=2, choices=core_constants.ETNIA_CHOICES,
                                    default=ETNIA_MESTIZO, null=True)
    peso_edad_gestacional = models.CharField(
        max_length=2, null=True, blank=True,
        validators=[RegexValidator(regex='^[0-9]{2}$', message='Número de 2 digitos')],
        choices=core_constants.PEG_CHOICES)
    reanimacion_respiratoria = models.CharField(
        max_length=2, null=True, blank=True, default="00",
        validators=[RegexValidator(regex='^[0-9]{2}$', message='Número de 2 digitos')],
        choices=core_constants.REARESP_CHOICES)
    es_medicacion_reanimacion = models.BooleanField(default=False)
    es_hospitalizacion = models.BooleanField('Es Hospitalización', default=False)
    es_profilaxis_ocular = models.BooleanField('Es Profilaxis Ocular', default=False)
    es_vitamina_k = models.BooleanField('Es Vitamina K', default=False)
    es_contacto_piel_a_piel = models.NullBooleanField('Es Contacto Piel a Piel', default=None)
    es_alojamiento_conjunto = models.NullBooleanField('Es Alojamiento Conjunto', default=None)

    deposiciones = models.CharField(
        "Deposiciones", max_length=2, null=True, blank=True,
        validators=[RegexValidator(regex='^[0-9]{2}$', message='Número de 2 digitos')],
        choices=core_constants.DEP_CHOICES)
    es_icteria_precoz = models.BooleanField('Es Icteria Precoz', default=False)
    alimentacion = models.CharField(
        "alimentacion", max_length=2, null=True, blank=True,
        validators=[RegexValidator(regex='^[0-9]{2}$', message='Número de 2 digitos')],
        choices=core_constants.ALIM_CHOICES)
    grupo_sanguineo = models.CharField(
        "Grupo Sanguineo", max_length=2, null=True, blank=True,
        validators=[RegexValidator(regex='^[0-9]{2}$', message='Número de 2 digitos')],
        choices=core_constants.GRUPOSANG_CHOICES)
    factor_rh = models.CharField(
        "Factor RH", max_length=2, choices=core_constants.SIGNOS_NULL_CHOICES, null=True, blank=True)
    es_tsh = models.NullBooleanField('Es TSH', default=None)
    vdrl_rpr = models.CharField(
        "VDRL / RPR", max_length=2, choices=core_constants.SIGNOS_NULL_CHOICES, null=True, blank=True)
    signos_sintomas_parto = MultiSelectField(
        choices=core_constants.SIGNOS_SINTOMAS_ALERTAS_CHOICES, null=True, blank=True)
    corticoides_antenatales = models.CharField(
        max_length=2, choices=core_constants.CA_CHOICES, null=True, blank=True)
    corticoides_semanas_inicio = models.PositiveSmallIntegerField(
        "Semanas Inicio", null=True, blank=True, validators=[MinValueValidator(28), MaxValueValidator(34)])
    fecha_terminacion_parto = models.DateField('Fecha Terminación Parto', null=True, blank=True)
    terminacion_parto = models.CharField(
        "Terminación", max_length=2, null=True, blank=True,
        validators=[RegexValidator(regex='^[0-9]{2}$', message='Número de 2 digitos')],
        choices=core_constants.CTP_CHOICES)
    indicacion_cie = models.CharField("Indicación", max_length=10, null=True, blank=True)

    tipo_parto = models.CharField(
        "Alumbramiento", max_length=2, null=True, blank=True,
        validators=[RegexValidator(regex='^[0-9]{2}$', message='Número de 2 digitos')],
        choices=core_constants.TP_CHOICES)

    posicion_parto = models.CharField(
        "Posición Parto", max_length=2, null=True, blank=True,
        validators=[RegexValidator(regex='^[0-9]{2}$', message='Número de 2 digitos')],
        choices=core_constants.POSICION_CHOICES)

    es_partograma = models.BooleanField('Es Partograma', default=False)
    es_acompaniante_parto = models.BooleanField('Es Parto Acompañante', default=False)

    condicion_parto = models.CharField(
        "Condición", max_length=2, null=True, blank=True,
        validators=[RegexValidator(regex='^[0-9]{2}$', message='Número de 2 digitos')],
        choices=core_constants.CTP_CHOICES)

    atiende_parto = models.CharField(
        "Responsable Atención", null=True, blank=True,
        max_length=2, validators=[RegexValidator(regex='^[0-9]{2}$', message='Número de 2 digitos')],
        choices=core_constants.AP_CHOICES)

    financiador_parto = models.CharField(
        "Financiador Parto", null=True, blank=True, max_length=2,
        choices=core_constants.FINANCIADOR_CHOICES)
    duracion_semanas_parto = models.PositiveSmallIntegerField(
        "Edad gestacional", validators=[MinValueValidator(22), MaxValueValidator(48)], null=True, blank=True)
    duracion_parto = models.CharField(
        "Duración", max_length=2, null=True, blank=True,
        validators=[RegexValidator(regex='^[0-9]{2}$', message='Número de 2 digitos')],
        choices=core_constants.DURACION_PARTO_CHOICES)
    muerte_intrauterina = models.CharField(
        "Muerte intrauterina", max_length=2, null=True, blank=True, default="01",
        validators=[RegexValidator(regex='^[0-9]{2}$', message='Número de 2 digitos')],
        choices=core_constants.MUERTEINTRA_PARTO_CHOICES)
    es_episiotomia_parto = models.CharField(
        'Es Episiotomía', max_length=2, choices=core_constants.EPISIOTOMIA_PARTO_CHOICES, null=True, blank=True)
    desgarro_parto = models.CharField(
        "Desgarro", max_length=2, null=True, blank=True,
        choices=core_constants.DESGARRO_PARTO_CHOICES)
    alumbramiento_parto = models.CharField(max_length=2, null=True, blank=True)
    placenta_parto = models.CharField(
        max_length=2, validators=[RegexValidator(regex='^[0-9]{2}$', message='Número de 2 digitos')],
        choices=core_constants.PP_CHOICES, null=True, blank=True)

    fecha_egreso = models.DateField("Fecha de Egreso", null=True, blank=True)
    tipo_egreso = models.CharField(
        "Tipo Egreso", max_length=35, null=True, blank=True,
        choices=core_constants.TIPOE_CHOICES)

    establecimiento_traslado = models.CharField(max_length=12, null=True, blank=True)
    patologia_cie = models.CharField("Patología", max_length=10, null=True, blank=True)
    es_necropsia = models.BooleanField('Es Necropsia', default=False)

    es_eess_procedencia = models.BooleanField(default=False)
    eess_procedencia = models.CharField(max_length=20, null=True, blank=True)
    codigo_local = models.CharField(max_length=8, null=True, blank=True)
    tipo_doc_madre = models.CharField(max_length=2, null=True, blank=True, choices=core_constants.TDOC_CHOICES)
    numero_doc_madre = models.CharField(max_length=35, null=True, blank=True)
    primer_apellido_madre = models.CharField(max_length=40, null=True, blank=True)
    segundo_apellido_madre = models.CharField(max_length=40, null=True, blank=True)
    prenombres_madre = models.CharField(max_length=60, null=True, blank=True)

    es_ficha_activa = models.BooleanField(default=True)
    numero_dni_ciudadano = models.CharField(max_length=8, null=True, blank=True)
    codigo_renaes_adscrito = models.CharField(max_length=12, null=True, blank=True)

    ciudadano = models.ForeignKey(Ciudadano, null=True, related_name='rns')

    class Meta:
        verbose_name = "Ciudadano RN"
        verbose_name_plural = "Ciudadanos RN"

    def __str__(self):
        return self.cui

    def save(self, crear_ciudadano=True, *args, **kwargs):
        if crear_ciudadano and self.ciudadano is None:
            self.ciudadano, _ = Ciudadano.objects.get_or_create(
                cui=self.cui, fecha_nacimiento=self.fecha_nacimiento, sexo=self.sexo_nacido, etnia=self.etnia_nacido,
                nombres=self.nombre_nacido, apellido_materno=self.primer_apellido_madre, tipo_documento_minsa='0',
                origen_datos=4)
        return super().save(*args, **kwargs)

    @property
    def nombres(self):
        return self.ciudadano.nombres

    @property
    def uid(self):
        return self.uuid

    @property
    def ciudadano_uuid(self):
        return self.ciudadano.uuid

    @property
    def ciudadano_tipo_doc(self):
        return self.ciudadano.tipo_documento

    @property
    def ciudadano_numero_doc(self):
        return self.ciudadano.numero_documento


class CiudadanoParentesco(models.Model):
    titular = models.CharField(max_length=12, verbose_name="Nro Documento Persona")
    parentesco = models.PositiveSmallIntegerField(choices=PARENTESCO_CHOICES)
    pariente = models.CharField(max_length=12, verbose_name="Nro Documento Pariente")


class AntecedenteCiudadano(BaseModel):
    ciudadano = models.ForeignKey(Ciudadano, blank=True)
    ciex = models.CharField(max_length=8, blank=True, null=True)
    fecha_inicio = models.DateField(blank=True, null=True)
    fecha_fin = models.DateField(blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)
    tipo_antecedente = models.CharField(
        max_length=1, choices=TIPO_ANTECEDENTE_CHOICES, default=TIPO_ANTECEDENTE_PERSONAL, null=True, blank=True)
    anio_diagnostico = models.CharField(max_length=4, blank=True, null=True)
    registro_antecedente = models.CharField(
        max_length=1, choices=REGISTRO_ANTECEDENTE_CHOICES, default=REGISTRO_ANTECEDENTE_POSITIVO)
    grupo_antecedente = models.CharField(
        max_length=1, choices=GRUPO_ANTECEDENTES_CHOICES, default=GRUPO_ANTECEDENTES_PERSONALES)
    subgrupo_antecedente = models.CharField(max_length=1, blank=True, null=True, choices=SUBGRUPO_ANTECEDENTES_CHOICES)
    consulta_paciente = models.UUIDField(blank=True, null=True)
    codigo_antecedente_sugerido = models.CharField(max_length=6, blank=True, null=True)
    nombre_antecedente_sugerido = models.CharField(max_length=255, blank=True, null=True)

    def delete(self, using=None, keep_parents=False):
        self.es_removido = True
        self.save()

    @property
    def ciex_descripcion(self):
        try:
            return CatalogoCIE.objects.get(id_ciex=self.ciex).desc_ciex
        except CatalogoCIE.DoesNotExist:
            return '-'


class AntecedenteFamiliar(BaseModel):
    ciudadano = models.ForeignKey(Ciudadano)
    ciex = models.CharField(max_length=8, blank=True, null=True)
    parentesco = ArrayField(
        models.PositiveSmallIntegerField(choices=PARENTESCO_CHOICES, blank=True, null=True),
        null=True
    )
    fecha_inicio = models.DateField(blank=True, null=True)
    fecha_fin = models.DateField(blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)
    registro_antecedente = models.CharField(
        max_length=1, choices=REGISTRO_ANTECEDENTE_CHOICES, default=REGISTRO_ANTECEDENTE_POSITIVO)
    grupo_antecedente = models.CharField(max_length=1, default=GRUPO_ANTECEDENTES_FAMILIARES)
    subgrupo_antecedente = models.CharField(max_length=1, blank=True, null=True, choices=SUBGRUPO_ANTECEDENTES_CHOICES)
    consulta_paciente = models.UUIDField(blank=True, null=True)
    codigo_antecedente_sugerido = models.CharField(max_length=6, blank=True, null=True)
    nombre_antecedente_sugerido = models.CharField(max_length=255, blank=True, null=True)

    def delete(self, using=None, keep_parents=False):
        self.es_removido = True
        self.save()

    @property
    def ciex_descripcion(self):
        try:
            return CatalogoCIE.objects.get(id_ciex=self.ciex).desc_ciex
        except CatalogoCIE.DoesNotExist:
            return '-'


class AntecedenteMedicacionHabitual(UUIDTimeStampedModel):
    familia_medicamento = models.CharField(max_length=10, blank=True, null=True)
    medicamento = models.CharField(max_length=10)
    dosis = models.CharField(max_length=250)
    frecuencia_horas = models.PositiveSmallIntegerField()
    fecha_inicio = models.DateField(blank=True, null=True)
    anio_inicio = models.CharField(max_length=4, blank=True, null=True)
    consulta_paciente = models.UUIDField()
    ciudadano = models.UUIDField()


class AntecedenteReaccionAdversaMedicamento(BaseModel):
    familia_medicamento = models.CharField(max_length=10)
    medicamento = models.CharField(max_length=10)
    anio_diagnostico = models.CharField(max_length=4, blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)
    registro_antecedente = models.CharField(
        max_length=1, choices=REGISTRO_ANTECEDENTE_CHOICES, default=REGISTRO_ANTECEDENTE_POSITIVO)
    consulta_paciente = models.UUIDField()
    ciudadano = models.UUIDField()


class CiudadanoDatosSIS(UUIDTimeStampedModel):
    codigo_eess = models.CharField(max_length=8)
    contrato = models.CharField(max_length=50, null=True, blank=True)
    correlativo = models.CharField(max_length=50, null=True, blank=True)
    disa = models.CharField(max_length=50, null=True, blank=True)
    estado = models.CharField(max_length=50)
    fecha_afiliacion = models.DateField()
    fecha_caducidad = models.DateField(null=True, blank=True)
    genero = models.CharField(max_length=1, null=True, blank=True)
    id_grupo_poblacional = models.CharField(max_length=50, null=True, blank=True)
    id_numero_registro = models.CharField(max_length=50, null=True, blank=True)
    id_plan = models.CharField(max_length=50, null=True, blank=True)
    id_ubigeo = models.CharField(max_length=10, null=True, blank=True)
    nro_contrato = models.CharField(max_length=50, null=True, blank=True)
    regimen = models.CharField(max_length=50, null=True, blank=True)
    tabla = models.CharField(max_length=1, null=True, blank=True)
    tipo_documento = models.CharField(max_length=2, null=True, blank=True)
    tipo_formato = models.CharField(max_length=50, null=True, blank=True)
    tipo_seguro = models.CharField(max_length=50, null=True, blank=True)
    tipo_seguro_descripcion = models.CharField(max_length=50, null=True, blank=True)

    ciudadano = models.OneToOneField(Ciudadano)

    def __str__(self):
        return self.ciudadano.numero_documento
