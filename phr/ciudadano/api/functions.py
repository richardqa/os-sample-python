"""
Funciones para API de Ciudadano
"""
import datetime
import logging

from django.conf import settings
from django.utils import timezone

import requests
from rest_framework.exceptions import APIException, ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.status import is_success

from phr.ciudadano.forms import CiudadanoDatosSISForm
from phr.ciudadano.models import Ciudadano, CiudadanoDatosSIS
from phr.common.constants import (
    ESTADO_CIVIL_SOLTERO, FINANCIADOR_NO_SE_CONOCE, FINANCIADOR_SIS, FINANCIADOR_USUARIO, ORIGEN_DATA_MIGRACIONES,
    ORIGEN_DATA_RENIEC, SIS_ESTADO_ACTIVO, TIPODOC_CARNET_EXTRANJERIA, TIPODOC_DNI,
)
from phr.common.models import ConfiguracionConexionInternet
from phr.ubigeo.models import UbigeoDistrito
from phr.utils.functions import ping_ws_ciudadano

logger = logging.getLogger(__name__)


def registrar_ciudadano(tipo_documento, numero_documento, origen_datos, uuid=None):
    """
    Registra ciudadano con datos obtenidos de MPICentral

    :param tipo_documento:   Tipo de documento de ciudadano
    :param numero_documento: Número de documento de ciudadano
    :param origen_datos:     Origen de datos de ciudadano
    :param uuid:             UUID de ciudadano si existe previamente

    :return: Instancia de `Ciudadano` creado o actualizado
    """
    url = '{host}/api/v1/ciudadanos/{tipo_documento}/{numero_documento}/'.format(
        host=settings.MPI_CENTRAL_HOST,
        tipo_documento=tipo_documento,
        numero_documento=numero_documento
    )
    headers = {'Authorization': 'Bearer {token}'.format(token=settings.MPI_CENTRAL_TOKEN)}
    try:
        response = requests.get(url, **{'headers': headers})
    except Exception:
        mensaje = 'Error al conectarse al servidor MPICentral',
        logger.warning(mensaje, exc_info=True)
        raise APIException(mensaje)

    if is_success(response.status_code):
        data = response.json()
    else:
        raise ValidationError(response.reason, code=response.status_code)
    try:
        distrito = UbigeoDistrito.objects.get(cod_ubigeo_reniec_distrito=data.get('domicilio_ubigeo', ''))
        provincia = distrito.provincia
        departamento = provincia.departamento
        pais = departamento.pais
        continente = pais.continente
    except (UbigeoDistrito.DoesNotExist, UbigeoDistrito.MultipleObjectsReturned):
        continente = None
        pais = None
        departamento = None
        provincia = None
        distrito = None
    try:
        distrito_nac = UbigeoDistrito.objects.get(cod_ubigeo_reniec_distrito=data.get('nacimiento_ubigeo', ''))
        provincia_nac = distrito_nac.provincia
        departamento_nac = provincia_nac.departamento
    except (UbigeoDistrito.DoesNotExist, UbigeoDistrito.MultipleObjectsReturned):
        departamento_nac = None
        provincia_nac = None
        distrito_nac = None
    if uuid:
        ciudadano = get_object_or_404(Ciudadano, uuid=uuid)
        is_new = True
    else:
        ciudadano, is_new = Ciudadano.objects.get_or_create(
            tipo_documento=tipo_documento,
            numero_documento=numero_documento,
            uuid=data.get('uuid'),
            origen_datos=origen_datos
        )
    if is_new:
        ciudadano.tipo_documento = tipo_documento
        ciudadano.numero_documento = numero_documento
        ciudadano.apellido_paterno = data.get('apellido_paterno', '')
        apellido_materno = data.get('apellido_materno', '') or ''
        apellido_casada = data.get('apellido_casada', '') or ''
        apellido_materno_casada = '{} {}'.format(
            apellido_materno, apellido_casada).replace('SIN DATOS', '').replace('null', '')
        ciudadano.apellido_materno = apellido_materno_casada.strip()
        ciudadano.nombres = data.get('nombres', '')
        try:
            ciudadano.fecha_nacimiento = datetime.datetime.strptime(data.get('fecha_nacimiento'), '%Y-%m-%d').date()
        except (IndexError, ValueError, TypeError):
            ciudadano.fecha_nacimiento = None
        ciudadano.sexo = data.get('sexo')
        ciudadano.continente_domicilio = continente
        ciudadano.pais_domicilio = pais
        ciudadano.departamento_domicilio = departamento
        ciudadano.provincia_domicilio = provincia
        ciudadano.distrito_domicilio = distrito
        ciudadano.domicilio_direccion = data.get('domicilio_direccion')
        ciudadano.estado_civil = data.get('estado_civil', ESTADO_CIVIL_SOLTERO)
        ciudadano.departamento_nacimiento = departamento_nac
        ciudadano.provincia_nacimiento = provincia_nac
        ciudadano.distrito_nacimiento = distrito_nac
        ciudadano.nacimiento_ubigeo = data.get('nacimiento_ubigeo')
        ciudadano.foto = data.get('foto')
        ciudadano.origen_datos = origen_datos
        ciudadano.es_persona_viva = data.get('es_persona_viva')
        ciudadano.uuid = data.get('uuid') if not ciudadano.uuid else ciudadano.uuid
        ciudadano.save()
    return ciudadano


def verificar_conexion_internet():
    """
    Verifica que exista una conexión a Internet
    """
    conexion_internet = ConfiguracionConexionInternet.objects.first()
    if conexion_internet:
        if not conexion_internet.con_conexion:
            raise APIException('El sistema está configurado para funcionar sin conexión a Internet')
        ping_ws_ciudadano(conexion_internet.ping_time)
    else:
        raise APIException(
            'El sistema no tiene una configuración de conexión a internet, contáctese con el administrador')


def crear_actualizar_ciudadano_migraciones(numero_documento, uuid=None):
    """
    Obtiene datos de ciudadano desde Migraciones

    :param numero_documento: Número de documento a consultar en RENIEC
    :param uuid: UUID de ciudadano a actualizar
    :return: ciudadano
    """
    verificar_conexion_internet()

    ciudadano = registrar_ciudadano(TIPODOC_CARNET_EXTRANJERIA, numero_documento, ORIGEN_DATA_MIGRACIONES, uuid)
    return ciudadano


def crear_actualizar_ciudadano_reniec(numero_documento, uuid=None):
    """
    Obtiene datos de ciudadano desde RENIEC

    :param numero_documento: Número de documento a consultar en RENIEC
    :param uuid: UUID de ciudadano a actualizar
    :return: ciudadano
    """
    verificar_conexion_internet()

    ciudadano = registrar_ciudadano(TIPODOC_DNI, numero_documento, ORIGEN_DATA_RENIEC, uuid)
    return ciudadano


def consultar_ws_sis_dni(ciudadano):
    """
    Consulta a MPI Central por datos de SIS de ciudadano.

    :param ciudadano: Ciudadano del que se requiere consultar los datos
    :return: Diccionario con datos obtenidos de consulta de SIS.
    :rtype: dict
    """
    verificar_conexion_internet()

    url = '{host}/api/v1/ciudadanos/sis/{tipo_documento}/{numero_documento}/'.format(
        host=settings.MPI_CENTRAL_HOST,
        tipo_documento=ciudadano.tipo_documento,
        numero_documento=ciudadano.numero_documento
    )
    headers = {'Authorization': 'Bearer {token}'.format(token=settings.MPI_CENTRAL_TOKEN)}
    try:
        response = requests.get(url, **{'headers': headers})
        if is_success(response.status_code):
            return response.json()
    except Exception:
        logger.warning('Error al obtener datos de SIS', exc_info=True)
    return None


def ciudadano_verificar_sis(ciudadano, actualizar_sis=False):
    """
    Verificar si ciudadano cuenta con SIS

    :param ciudadano: Ciudadano a verificar si cuenta con SIS
    :param actualizar_sis: Booleano que fuerza verificación de SIS
    """
    try:
        datos_ciudadano_sis = None
        if ciudadano.ultima_actualizacion_tipo_seguro:
            if actualizar_sis or ciudadano.ultima_actualizacion_tipo_seguro < timezone.now().date():
                datos_ciudadano_sis = consultar_ws_sis_dni(ciudadano)
        else:
            datos_ciudadano_sis = consultar_ws_sis_dni(ciudadano)
        if datos_ciudadano_sis is not None:
            if datos_ciudadano_sis.get('estado') == SIS_ESTADO_ACTIVO:
                ciudadano.tipo_seguro = FINANCIADOR_SIS
                try:
                    ciudadano_datos_sis = CiudadanoDatosSIS.objects.get(ciudadano=ciudadano)
                except CiudadanoDatosSIS.DoesNotExist:
                    ciudadano_datos_sis = None
                ciudadano_datos_sis_form = CiudadanoDatosSISForm(datos_ciudadano_sis, instance=ciudadano_datos_sis)
                if ciudadano_datos_sis_form.is_valid():
                    ciudadano_datos_sis = ciudadano_datos_sis_form.save(commit=False)
                    ciudadano_datos_sis.ciudadano = ciudadano
                    ciudadano_datos_sis.save()
            elif ciudadano.tipo_seguro == FINANCIADOR_SIS:
                ciudadano.tipo_seguro = FINANCIADOR_NO_SE_CONOCE
        else:
            if actualizar_sis:
                ciudadano.tipo_seguro = FINANCIADOR_USUARIO
        ciudadano.ultima_actualizacion_tipo_seguro = timezone.now().date()
        ciudadano.save()
    except Exception:
        logger.warning('Error al obtener datos de SIS', exc_info=True)
