from drf_extra_fields.geo_fields import PointField
from rest_framework import serializers

from phr.insteducativa.models import InstitucionEducativa
from phr.ubigeo.models import UbigeoDepartamento, UbigeoDistrito, UbigeoProvincia


class InstEducativaSerializer(serializers.ModelSerializer):
    ubicacion = PointField(required=False)
    departamento_nombre = serializers.SerializerMethodField()
    provincia_nombre = serializers.SerializerMethodField()
    distrito_nombre = serializers.SerializerMethodField()

    class Meta:
        model = InstitucionEducativa
        fields = ('codigo_colegio', 'codigo_modular', 'nombre', 'ubigeo', 'direccion', 'nivel', 'nivel_descripcion',
                  'tipo', 'tipo_descripcion', 'nombre_ugel', 'establecimiento_renaes', 'establecimiento_nombre',
                  'ubicacion', 'departamento_nombre', 'provincia_nombre', 'distrito_nombre',)

    def get_departamento_nombre(self, obj):
        if obj.ubigeo:
            try:
                departamento = UbigeoDepartamento.objects.get(cod_ubigeo_inei_departamento=obj.ubigeo[:2])
                return departamento.ubigeo_departamento
            except UbigeoDepartamento.DoesNotExist:
                return ''

    def get_provincia_nombre(self, obj):
        if obj.ubigeo:
            try:
                provincia = UbigeoProvincia.objects.get(cod_ubigeo_inei_provincia=obj.ubigeo[:4])
                return provincia.ubigeo_provincia
            except UbigeoProvincia.DoesNotExist:
                return ''

    def get_distrito_nombre(self, obj):
        if obj.ubigeo:
            try:
                distrito = UbigeoDistrito.objects.get(cod_ubigeo_inei_distrito=obj.ubigeo)
                return distrito.ubigeo_distrito
            except UbigeoDistrito.DoesNotExist:
                return ''
