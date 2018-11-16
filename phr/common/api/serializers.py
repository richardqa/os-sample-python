from rest_framework import serializers

from phr.common.models import ConfiguracionConexionInternet
from phr.utils.functions import ping_ws_ciudadano


class ConnectionStatusSerializer(serializers.ModelSerializer):
    ping_response = serializers.SerializerMethodField()

    class Meta:
        model = ConfiguracionConexionInternet
        fields = (
            'con_conexion',
            'ping_time',
            'ping_response',
        )

    def get_ping_response(self, obj):
        configuracion = ConfiguracionConexionInternet.objects.first()
        if configuracion and configuracion.con_conexion:
            return ping_ws_ciudadano(configuracion.ping_time)[0]
        return False
