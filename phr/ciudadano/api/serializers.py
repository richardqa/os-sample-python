import re

from django.utils import timezone

from rest_framework_json_api import serializers

from phr.catalogo.models import FamiliaMedicamentoAntecedenteSugerido, MedicamentoAntecedenteSugerido
from phr.ciudadano.models import (
    AntecedenteCiudadano, AntecedenteFamiliar, AntecedenteMedicacionHabitual, AntecedenteReaccionAdversaMedicamento,
    Ciudadano, CiudadanoDatosSIS, CiudadanoRN,
)
from phr.common.constants import PARENTESCO_CHOICES_DICT
from phr.common.models import ConfiguracionConexionInternet
from phr.utils.functions import ping_ws_ciudadano


# ********************************* CIUDADANO *********************************
class CiudadanoSerializer(serializers.ModelSerializer):
    departamento_domicilio_actual_nombre = serializers.SerializerMethodField()
    departamento_domicilio_actual_codigo = serializers.SerializerMethodField()
    provincia_domicilio_actual_nombre = serializers.SerializerMethodField()
    provincia_domicilio_actual_codigo = serializers.SerializerMethodField()
    distrito_domicilio_actual_nombre = serializers.SerializerMethodField()
    distrito_domicilio_actual_codigo = serializers.SerializerMethodField()
    localidad_domicilio_actual_nombre = serializers.SerializerMethodField()
    localidad_domicilio_actual_codigo = serializers.SerializerMethodField()
    domicilio_historial = serializers.SerializerMethodField()
    pais_origen = serializers.SerializerMethodField()
    pais_origen_nombre = serializers.SerializerMethodField()
    pais_domicilio = serializers.SerializerMethodField()
    pais_domicilio_nombre = serializers.SerializerMethodField()
    pais_domicilio_actual = serializers.SerializerMethodField()
    pais_domicilio_actual_nombre = serializers.SerializerMethodField()

    def get_departamento_domicilio_actual_nombre(self, obj):
        return obj.departamento_domicilio_actual.ubigeo_departamento if obj.departamento_domicilio_actual else ''

    def get_departamento_domicilio_actual_codigo(self, obj):
        return (obj.departamento_domicilio_actual.cod_ubigeo_reniec_departamento
                if obj.departamento_domicilio_actual else '')

    def get_provincia_domicilio_actual_nombre(self, obj):
        return obj.provincia_domicilio_actual.ubigeo_provincia if obj.provincia_domicilio_actual else ''

    def get_provincia_domicilio_actual_codigo(self, obj):
        return obj.provincia_domicilio_actual.cod_ubigeo_reniec_provincia if obj.provincia_domicilio_actual else ''

    def get_distrito_domicilio_actual_nombre(self, obj):
        return obj.distrito_domicilio_actual.ubigeo_distrito if obj.distrito_domicilio_actual else ''

    def get_distrito_domicilio_actual_codigo(self, obj):
        return obj.distrito_domicilio_actual.cod_ubigeo_reniec_distrito if obj.distrito_domicilio_actual else ''

    def get_localidad_domicilio_actual_nombre(self, obj):
        return obj.localidad_domicilio_actual.ubigeo_localidad if obj.localidad_domicilio_actual else ''

    def get_localidad_domicilio_actual_codigo(self, obj):
        return obj.localidad_domicilio_actual.cod_ubigeo_reniec_localidad if obj.localidad_domicilio_actual else ''

    def get_domicilio_historial(self, obj):
        historial = []
        for obj in obj.domiciliociudadanohistorial_set.all().order_by('fecha_registro'):
            historial.append({
                'domicilio_direccion': obj.domicilio_direccion or '',
                'domicilio_referencia': obj.domicilio_referencia or '',
                'pais_domicilio_ubigeo_reniec': (obj.pais_domicilio.cod_ubigeo_reniec_pais
                                                 if obj.pais_domicilio else ''),
                'pais_domicilio': obj.pais_domicilio.ubigeo_pais if obj.pais_domicilio else '',
                'departamento_domicilio_ubigeo_reniec': (obj.departamento_domicilio.cod_ubigeo_reniec_departamento
                                                         if obj.departamento_domicilio else ''),
                'departamento_domicilio': (obj.departamento_domicilio.ubigeo_departamento
                                           if obj.departamento_domicilio else ''),
                'provincia_domicilio_ubigeo_reniec': (obj.provincia_domicilio.cod_ubigeo_reniec_provincia
                                                      if obj.provincia_domicilio else ''),
                'provincia_domicilio': obj.provincia_domicilio.ubigeo_provincia if obj.provincia_domicilio else '',
                'distrito_domicilio_ubigeo_reniec': (obj.distrito_domicilio.cod_ubigeo_reniec_distrito
                                                     if obj.distrito_domicilio else ''),
                'distrito_domicilio': obj.distrito_domicilio.ubigeo_distrito if obj.distrito_domicilio else '',
                'fecha_registro': obj.fecha_registro.strftime("%Y-%m-%d"),
            })
        return historial

    def get_pais_origen(self, obj):
        return obj.pais_origen.pk if obj.pais_origen else None

    def get_pais_origen_nombre(self, obj):
        return obj.pais_origen.ubigeo_pais if obj.pais_origen else None

    def get_pais_domicilio(self, obj):
        return obj.pais_domicilio.pk if obj.pais_domicilio else None

    def get_pais_domicilio_nombre(self, obj):
        return obj.pais_domicilio.ubigeo_pais if obj.pais_domicilio else None

    def get_pais_domicilio_actual(self, obj):
        return obj.pais_domicilio_actual.pk if obj.pais_domicilio_actual else None

    def get_pais_domicilio_actual_nombre(self, obj):
        return obj.pais_domicilio_actual.ubigeo_pais if obj.pais_domicilio_actual else None

    class Meta:
        model = Ciudadano
        fields = (
            'uuid',
            'uid',
            'cui',
            'origen_datos',
            'tipo_documento',
            'tipo_documento_minsa',
            'numero_documento',
            'nombres',
            'apellido_paterno',
            'apellido_materno',
            'sexo',
            'fecha_nacimiento',
            'edad_str',
            'edad_anios',
            'edad_meses',
            'edad_dias',
            'estado_civil',
            'grado_instruccion',
            'ocupacion',
            'correo',
            'telefono',
            'celular',
            'nacimiento_ubigeo',
            'pais_origen',
            'pais_origen_nombre',
            'domicilio_direccion',
            'domicilio_referencia',
            'departamento_domicilio',
            'provincia_domicilio',
            'distrito_domicilio',
            'pais_domicilio',
            'pais_domicilio_nombre',
            'etnia',
            'tipo_seguro',
            'domicilio_direccion_actual',
            'etnia_descripcion',
            'codigo_asegurado',
            'es_persona_viva',
            'domicilio_referencia_actual',
            'departamento_domicilio_actual_nombre',
            'departamento_domicilio_actual_codigo',
            'provincia_domicilio_actual_nombre',
            'provincia_domicilio_actual_codigo',
            'pais_domicilio_actual',
            'pais_domicilio_actual_nombre',
            'distrito_domicilio_actual_nombre',
            'distrito_domicilio_actual_codigo',
            'localidad_domicilio_actual_nombre',
            'localidad_domicilio_actual_codigo',
            'departamento_domicilio_actual',
            'provincia_domicilio_actual',
            'distrito_domicilio_actual',
            'localidad_domicilio_actual',
            'domicilio_historial',
            'get_departamento_domicilio_ubigeo_reniec',
            'get_provincia_domicilio_ubigeo_reniec',
            'get_distrito_domicilio_ubigeo_reniec',
            'get_departamento_domicilio_ubigeo_inei',
            'get_provincia_domicilio_ubigeo_inei',
            'get_distrito_domicilio_ubigeo_inei',
            'get_departamento_domicilio_nombre',
            'get_provincia_domicilio_nombre',
            'get_distrito_domicilio_nombre',
            'get_ubigeo_nacimiento',
            'fecha_modificacion',
            'foto',
        )

        def validate_cui(self, value):
            if Ciudadano.objects.filter(cui=value).exists():
                raise serializers.ValidationError('CUI ya registrado')
            return value

        def validate_numero_documento(self, value):
            if not re.match(r"^\d{6,15}$", value):
                raise serializers.ValidationError("El número de documento debe ser numérico entre 6 y 15 caracteres.")
            return value


class CiudadanoDatosSISSerializer(serializers.ModelSerializer):
    conexion_internet = serializers.SerializerMethodField()

    class Meta:
        model = CiudadanoDatosSIS
        fields = (
            'codigo_eess',
            'contrato',
            'correlativo',
            'disa',
            'estado',
            'fecha_afiliacion',
            'fecha_caducidad',
            'genero',
            'id_grupo_poblacional',
            'id_numero_registro',
            'id_plan',
            'id_ubigeo',
            'nro_contrato',
            'regimen',
            'tabla',
            'tipo_documento',
            'tipo_formato',
            'tipo_seguro',
            'tipo_seguro_descripcion',
            'conexion_internet',
            'modified',
        )

    def get_conexion_internet(self, obj):
        conexion_internet = ConfiguracionConexionInternet.objects.first()
        if conexion_internet and conexion_internet.con_conexion:
            try:
                ping_ws_ciudadano(conexion_internet.ping_time)
                return True
            except Exception:
                return False
        return None


class CiudadanoNombreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ciudadano
        fields = ['nombres', 'apellido_paterno', 'apellido_materno']


class CiudadanoDataBasicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ciudadano
        fields = ['uuid', 'nombres', 'apellido_paterno', 'apellido_materno', 'sexo', 'correo', 'telefono', 'celular',
                  'tipo_documento', 'numero_documento', 'fecha_nacimiento', 'edad_str']


class CiudadanoMadreHijosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ciudadano
        fields = ['uuid', 'numero_documento', 'nombres', 'apellido_paterno', 'apellido_materno', 'sexo',
                  'fecha_nacimiento', 'edad_str', 'edad_anios', 'edad_meses', 'edad_dias', 'sexo',
                  'get_departamento_nacimiento_nombre', 'get_provincia_nacimiento_nombre',
                  'get_distrito_nacimiento_nombre', 'get_ubigeo_nacimiento']


class AntecedenteCiudadanoSerializer(serializers.ModelSerializer):
    fecha_inicio = serializers.DateField(read_only=True)
    fecha_fin = serializers.DateField(read_only=True)

    class Meta:
        model = AntecedenteCiudadano
        fields = (
            'uuid',
            'anio_diagnostico',
            'ciex',
            'ciex_descripcion',
            'ciudadano',
            'codigo_antecedente_sugerido',
            'consulta_paciente',
            'es_removido',
            'fecha_fin',
            'fecha_inicio',
            'grupo_antecedente',
            'nombre_antecedente_sugerido',
            'observaciones',
            'registro_antecedente',
            'subgrupo_antecedente',
            'tipo_antecedente',
        )


class AntecedenteFamiliarCiudadanoSerializer(serializers.ModelSerializer):
    parentesco = serializers.ListField()
    parentesco_display = serializers.SerializerMethodField()

    class Meta:
        model = AntecedenteFamiliar
        fields = (
            'uuid',
            'ciex',
            'ciex_descripcion',
            'ciudadano',
            'codigo_antecedente_sugerido',
            'consulta_paciente',
            'es_removido',
            'fecha_fin',
            'fecha_inicio',
            'grupo_antecedente',
            'nombre_antecedente_sugerido',
            'observaciones',
            'parentesco',
            'parentesco_display',
            'registro_antecedente',
            'subgrupo_antecedente',
        )

    def get_parentesco_display(self, obj):
        parentescos = []
        for parentesco in obj.parentesco:
            parentescos.append(PARENTESCO_CHOICES_DICT.get(str(parentesco)))
        return parentescos


class AntecedenteReaccionAdversaMedicamentoSerializer(serializers.ModelSerializer):
    familia_medicamento_nombre = serializers.SerializerMethodField()
    medicamento_nombre = serializers.SerializerMethodField()

    class Meta:
        model = AntecedenteReaccionAdversaMedicamento
        fields = (
            'uuid',
            'familia_medicamento',
            'familia_medicamento_nombre',
            'medicamento',
            'medicamento_nombre',
            'anio_diagnostico',
            'observaciones',
            'registro_antecedente',
            'consulta_paciente',
            'ciudadano',
        )

    def get_familia_medicamento_nombre(self, obj):
        # Obtener el nombre de la familia del medicamento, previamente cargado del fixture correspondiente
        return FamiliaMedicamentoAntecedenteSugerido.objects.get(codigo=obj.familia_medicamento).nombre

    def get_medicamento_nombre(self, obj):
        # Obtener el nombre del medicamento, previamente cargado del fixture correspondiente
        return MedicamentoAntecedenteSugerido.objects.get(codigo=obj.medicamento).nombre


class AntecedenteMedicacionHabitualSerializer(serializers.ModelSerializer):
    familia_medicamento_nombre = serializers.SerializerMethodField()
    medicamento_nombre = serializers.SerializerMethodField()

    class Meta:
        model = AntecedenteMedicacionHabitual
        fields = (
            'familia_medicamento',
            'medicamento',
            'dosis',
            'frecuencia_horas',
            'fecha_inicio',
            'anio_inicio',
            'consulta_paciente',
            'ciudadano',
            'familia_medicamento_nombre',
            'medicamento_nombre',
        )

    def validate_ciudadano(self, ciudadano):
        try:
            Ciudadano.objects.get(uuid=ciudadano)
            return ciudadano
        except Ciudadano.DoesNotExist:
            raise serializers.ValidationError('El ciudadano ingresado no existe.')

    def validate_fecha_inicio(self, fecha_inicio):
        if fecha_inicio > timezone.now().date():
            raise serializers.ValidationError('La fecha ingresada no puede ser mayor a la fecha actual.')
        else:
            return fecha_inicio

    def validate_anio_actual(self, anio_actual):
        if anio_actual > timezone.now().date().year:
            raise serializers.ValidationError('El año de inicio no puede ser mayor al año actual')
        return anio_actual

    def validate_familia_medicamento(self, familia_medicamento):
        try:
            FamiliaMedicamentoAntecedenteSugerido.objects.get(pk=familia_medicamento)
            return familia_medicamento
        except FamiliaMedicamentoAntecedenteSugerido.DoesNotExist:
            raise serializers.ValidationError('La familia de medicamentos no existe.')

    def validate_medicamento(self, medicamento):
        try:
            MedicamentoAntecedenteSugerido.objects.get(pk=medicamento)
            return medicamento
        except MedicamentoAntecedenteSugerido.DoesNotExist:
            raise serializers.ValidationError('El medicamento ingresado no existe.')

    def validate(self, data):
        ciudadano = data.get('ciudadano')
        medicamento = data.get('medicamento')
        try:
            AntecedenteMedicacionHabitual.objects.get(ciudadano=ciudadano, medicamento=medicamento)
            raise serializers.ValidationError(
                {'error': 'Ya existe antecedente registrado con el mismo medicamento.'})
        except AntecedenteMedicacionHabitual.DoesNotExist:
            return data

    def get_familia_medicamento_nombre(self, obj):
        try:
            return FamiliaMedicamentoAntecedenteSugerido.objects.get(pk=obj.familia_medicamento).nombre
        except FamiliaMedicamentoAntecedenteSugerido.DoesNotExist:
            return ''

    def get_medicamento_nombre(self, obj):
        return MedicamentoAntecedenteSugerido.objects.get(pk=obj.medicamento).nombre


# ********************************* CNV FORM *********************************
class CiudadanoRNSerializer(serializers.ModelSerializer):
    dni_ciudadano = serializers.SerializerMethodField('get_dni')
    nombres_ciudadano = serializers.SerializerMethodField('get_nombres')
    apellido_paterno_ciudadano = serializers.SerializerMethodField('get_apellido_paterno')
    apellido_materno_ciudadano = serializers.SerializerMethodField('get_apellido_materno')

    class Meta:
        model = CiudadanoRN
        fields = ['uuid', 'uid', 'cui', 'tipo_doc_madre', 'numero_doc_madre', 'primer_apellido_madre',
                  'segundo_apellido_madre', 'prenombres_madre', 'sexo_nacido', 'fecha_nacimiento', 'hora_nacimiento',
                  'peso_nacido', 'talla_nacido', 'apgar_uno_nacido', 'apgar_cinco_nacido',
                  'numero_nacido_perim_cefalico', 'numero_nacido_perim_toracico', 'numero_temperatura',
                  'resultado_examen_fisico', 'edad_examen_fisico', 'unida_medida_edad', 'duracion_parto',
                  'atiende_parto', 'condicion_parto', 'tipo_parto', 'financiador_parto', 'posicion_parto',
                  'es_partograma', 'duracion_parto', 'es_episiotomia_parto', 'alumbramiento_parto', 'desgarro_parto',
                  'placenta_parto', 'es_eess_procedencia', 'eess_procedencia', 'etnia_nacido', 'dni_ciudadano',
                  'nombres_ciudadano', 'apellido_paterno_ciudadano', 'apellido_materno_ciudadano', 'codigo_local',
                  'codigo_renaes', 'ciudadano_uuid', 'ciudadano_tipo_doc', 'ciudadano_numero_doc', 'es_ficha_activa',
                  'codigo_renaes_adscrito', 'duracion_semanas_parto']

    def get_dni(self, obj):
        num_doc = obj.ciudadano.numero_documento
        return num_doc

    def get_nombres(self, obj):
        nombres = obj.ciudadano.nombres
        return nombres

    def get_apellido_paterno(self, obj):
        apellido_paterno = obj.ciudadano.apellido_paterno
        return apellido_paterno

    def get_apellido_materno(self, obj):
        apellido_materno = obj.ciudadano.apellido_materno
        return apellido_materno


class CiudadanoFichaRNSerializer(serializers.ModelSerializer):
    class Meta:
        model = CiudadanoRN
        fields = ['sexo_nacido', 'peso_nacido', 'talla_nacido', 'numero_temperatura', 'numero_nacido_perim_cefalico',
                  'numero_nacido_perim_toracico', 'edad_examen_fisico', 'apgar_uno_nacido', 'apgar_cinco_nacido',
                  'reanimacion_respiratoria', 'es_medicacion_reanimacion', 'resultado_examen_fisico',
                  'es_hospitalizacion', 'es_profilaxis_ocular', 'es_vitamina_k', 'es_contacto_piel_a_piel',
                  'es_alojamiento_conjunto', ]


class CiudadanoFichaControlRNSerializer(serializers.ModelSerializer):
    class Meta:
        model = CiudadanoRN
        fields = ['deposiciones', 'es_icteria_precoz', 'alimentacion', 'grupo_sanguineo', 'factor_rh', 'es_tsh',
                  'vdrl_rpr']


class CiudadanoFichaEgresoRNSerializer(serializers.ModelSerializer):
    class Meta:
        model = CiudadanoRN
        fields = ['fecha_egreso', 'tipo_egreso', 'establecimiento_traslado', 'patologia_cie', 'es_necropsia']


class CiudadanoFichaPartoRNSerializer(serializers.ModelSerializer):
    class Meta:
        model = CiudadanoRN
        fields = ['signos_sintomas_parto', 'corticoides_antenatales', 'corticoides_semanas_inicio',
                  'fecha_terminacion_parto', 'terminacion_parto', 'indicacion_cie', 'tipo_parto', 'posicion_parto',
                  'es_partograma', 'es_acompaniante_parto', 'duracion_parto', 'muerte_intrauterina',
                  'es_episiotomia_parto', 'desgarro_parto', ]


class CiudadanoFechaActualizacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ciudadano
        fields = ('fecha_modificacion',)
