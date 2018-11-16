# coding=utf-8
from rest_framework_json_api import serializers

from phr.ubigeo.models import (
    UbigeoContinente, UbigeoDepartamento, UbigeoDistrito, UbigeoLocalidad, UbigeoPais, UbigeoProvincia,
)


class ListaUbigeoContienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = UbigeoContinente
        fields = ['id', 'cod_ubigeo_reniec_continente', 'cod_ubigeo_inei_continente', 'ubigeo_continente']


class ListaUbigeoPaisSerializer(serializers.ModelSerializer):
    class Meta:
        model = UbigeoPais
        fields = ['id', 'cod_ubigeo_reniec_pais', 'cod_ubigeo_inei_pais', 'ubigeo_pais', 'continente']


class ListaUbigeoDepartamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UbigeoDepartamento
        fields = ['id', 'cod_ubigeo_reniec_departamento', 'cod_ubigeo_inei_departamento', 'ubigeo_departamento',
                  'continente', 'pais']


class ListaUbigeoProvinciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = UbigeoProvincia
        fields = ['id', 'cod_ubigeo_reniec_provincia', 'cod_ubigeo_inei_provincia', 'ubigeo_provincia',
                  'ubigeo_departamento', 'continente', 'pais', 'departamento']


class ListaUbigeoDistritoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UbigeoDistrito
        fields = ['id', 'cod_ubigeo_reniec_distrito', 'cod_ubigeo_inei_distrito', 'ubigeo_distrito',
                  'ubigeo_provincia', 'ubigeo_departamento', 'continente', 'pais', 'departamento', 'provincia']


class ListaUbigeoLocalidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = UbigeoLocalidad
        fields = ['id', 'cod_ubigeo_reniec_localidad', 'cod_ubigeo_inei_localidad', 'ubigeo_localidad',
                  'ubigeo_distrito', 'ubigeo_provincia', 'ubigeo_departamento', 'continente', 'pais', 'departamento',
                  'provincia', 'distrito']


# -- Detalles
class DetalleUbigeoContinenteSerializer(serializers.ModelSerializer):
    class Meta:
        model = UbigeoContinente
        fields = ['id', 'cod_ubigeo_reniec_continente', 'cod_ubigeo_inei_continente', 'ubigeo_continente']


class DetalleUbigeoPaisSerializer(serializers.ModelSerializer):
    class Meta:
        model = UbigeoPais
        fields = ['id', 'cod_ubigeo_reniec_pais', 'cod_ubigeo_inei_pais', 'ubigeo_pais', 'continente']


class DetalleUbigeoDepartamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UbigeoDepartamento
        fields = ['id', 'cod_ubigeo_reniec_departamento', 'cod_ubigeo_inei_departamento', 'ubigeo_departamento',
                  'continente', 'pais']


class DetalleUbigeoProvinciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = UbigeoProvincia
        fields = ['id', 'cod_ubigeo_reniec_provincia', 'cod_ubigeo_inei_provincia', 'ubigeo_provincia', 'continente',
                  'pais', 'departamento']


class DetalleUbigeoDistritoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UbigeoDistrito
        fields = ['id', 'cod_ubigeo_reniec_distrito', 'cod_ubigeo_inei_distrito', 'ubigeo_distrito', 'continente',
                  'pais', 'departamento', 'provincia']


class DetalleUbigeoLocalidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = UbigeoLocalidad
        fields = ['id', 'cod_ubigeo_reniec_localidad', 'cod_ubigeo_inei_localidad', 'ubigeo_localidad',
                  'ubigeo_distrito', 'ubigeo_provincia', 'ubigeo_departamento', 'continente', 'pais', 'departamento',
                  'provincia', 'distrito']
