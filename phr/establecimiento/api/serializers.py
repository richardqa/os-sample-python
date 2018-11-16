from drf_extra_fields.geo_fields import PointField
from rest_framework_json_api import serializers

from phr.establecimiento.models import Diresa, Establecimiento, EstablecimientoSector, Microred, Red, Servicio

ESTABLECIMIENTO_FIELDS = ('id', 'codigo_renaes', 'nombre', 'nombre_microred', 'nombre_ambito', 'ubigeo', 'direccion',
                          'location', 'departamento_nombre', 'provincia_nombre', 'distrito_nombre', 'diresa_nombre',
                          'red_nombre', 'microred_nombre', 'categoria_nombre', 'categoria_nivel', 'sector_codigo',
                          'sector_nombre', 'diresa_codigo', 'red_codigo', 'microred_codigo', 'servicios_estab',
                          'telefono', 'horario_atencion',)


class ListaEstablecimientoSerializer(serializers.ModelSerializer):
    location = PointField(required=False)

    class Meta:
        model = Establecimiento
        fields = ESTABLECIMIENTO_FIELDS


class DetalleEstablecimientoSerializer(serializers.ModelSerializer):
    location = PointField(required=False)

    class Meta:
        model = Establecimiento
        fields = ESTABLECIMIENTO_FIELDS


class ListaEstablecimientoUbigeoSerializer(serializers.ModelSerializer):
    location = PointField(required=False)

    class Meta:
        model = Establecimiento
        fields = ESTABLECIMIENTO_FIELDS


class DiresaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diresa
        fields = ['nombre', 'codigo', 'departamento_nombre', 'departamento_ubigeo_inei', 'departamento_ubigeo_reniec']


class RedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Red
        fields = ['codigo', 'nombre', 'diresa_codigo', 'diresa_nombre']


class MicroredSerializer(serializers.ModelSerializer):
    class Meta:
        model = Microred
        fields = ['codigo', 'nombre', 'diresa_codigo', 'diresa_nombre', 'red_codigo', 'red_nombre']


class ServicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servicio
        fields = '__all__'


class SectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstablecimientoSector
        fields = ['codigo', 'descripcion']
