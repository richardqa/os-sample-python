from rest_framework import serializers

from phr.ciudadano.models import Ciudadano
from phr.establecimiento.models import Establecimiento
from phr.personal.models import Personal, TipoPersonal


class EstablecimientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Establecimiento
        fields = '__all__'


class CiudadanoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ciudadano
        fields = '__all__'


class TipoPersonalSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoPersonal
        fields = '__all__'


class PersonalSerializer(serializers.ModelSerializer):
    ciudadano = CiudadanoSerializer()
    tipo_personal = TipoPersonalSerializer()
    establecimientos = EstablecimientoSerializer(many=True)

    class Meta:
        model = Personal
        fields = '__all__'
