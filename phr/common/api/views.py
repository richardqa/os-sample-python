from rest_framework.exceptions import NotFound
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from phr.common.api.serializers import ConnectionStatusSerializer
from phr.common.models import ConfiguracionConexionInternet


class ConnectionStatusAPI(APIView):
    """
    Permite visualizar la configuración de la conexión a WS externos
    """
    renderer_classes = JSONRenderer, BrowsableAPIRenderer

    def get(self, request, *args, **kwargs):
        configuracion_internet = ConfiguracionConexionInternet.objects.first()
        if configuracion_internet:
            serializer = ConnectionStatusSerializer(instance=configuracion_internet)
            return Response(serializer.data)
        raise NotFound
