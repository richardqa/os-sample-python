"""
Funciones útiles para el proyecto
"""
import re
import subprocess
from urllib.parse import urlparse

from django.conf import settings


def ping_to_site(host_to_ping, host_name, latency):
    """
    Comprueba ping a un host y verificar su tiempo de latencia

    :param host_to_ping: HOST a hacer ping para probar conectividad
    :param host_name: Nombre del HOST a hacer ping
    :param latency: Tiempo de latencia en ms, necesario para asegurar
                    conexión al HOST
    :return: Tupla (bool, int) si se cumplen condiciones de ping, o
             excepción según problemas encontrados
    """
    if host_to_ping:
        ping_result = subprocess.run(["ping", host_to_ping, "-c", "1", "-W", "2"], stdout=subprocess.PIPE)
        if ping_result.returncode == 0:
            result = ping_result.stdout.decode()
            ping_time = float(re.findall(r'time=([0-9.]+)', result)[0])
            if ping_time < latency:
                return True, ping_time
            raise Exception("La conexión con {host_name} es demasiado lenta".format(host_name=host_name))
        raise Exception("No se puede establecer conexión con el servidor {host_name}".format(host_name=host_name))
    raise Exception("Debe ingresar un dominio para poder hacer PING")


def ping_ws_ciudadano(latency):
    """
    Comprueba ping hacia WS de consulta a MPI Central para poder obtener
    datos de ciudadanos

    :param latency: Tiempo de latencia en ms, necesario para asegurar
                    conexión al servidor de MPI Central
    """
    ciudadano_ws_domain = urlparse(settings.MPI_CENTRAL_HOST).netloc
    return ping_to_site(ciudadano_ws_domain, "MINSA-Central", latency)
