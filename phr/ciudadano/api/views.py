import datetime
import json
import logging

from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.db.models import Q
from django.http.response import JsonResponse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_exempt

import requests
from dateutil.relativedelta import relativedelta
from rest_framework import generics, status
from rest_framework.exceptions import APIException, NotFound
from rest_framework.generics import (
    CreateAPIView, DestroyAPIView, ListAPIView, RetrieveAPIView, RetrieveUpdateAPIView, get_object_or_404,
)
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, is_success
from rest_framework.views import APIView

from phr.ciudadano.api.functions import (
    ciudadano_verificar_sis, crear_actualizar_ciudadano_migraciones, crear_actualizar_ciudadano_reniec,
)
from phr.ciudadano.api.serializers import (
    AntecedenteCiudadanoSerializer, AntecedenteFamiliarCiudadanoSerializer, AntecedenteMedicacionHabitualSerializer,
    AntecedenteReaccionAdversaMedicamentoSerializer, CiudadanoDataBasicaSerializer, CiudadanoDatosSISSerializer,
    CiudadanoFechaActualizacionSerializer, CiudadanoFichaControlRNSerializer, CiudadanoFichaEgresoRNSerializer,
    CiudadanoFichaPartoRNSerializer, CiudadanoFichaRNSerializer, CiudadanoMadreHijosSerializer,
    CiudadanoNombreSerializer, CiudadanoRNSerializer, CiudadanoSerializer,
)
from phr.ciudadano.forms import CiudadanoPadronForm
from phr.ciudadano.models import (
    AntecedenteCiudadano, AntecedenteFamiliar, AntecedenteMedicacionHabitual, AntecedenteReaccionAdversaMedicamento,
    Ciudadano, CiudadanoDatosSIS, CiudadanoParentesco, CiudadanoRN,
)
from phr.common import constants
from phr.common.constants import TDOC_HISMINSA_DNI, TIPODOC_CARNET_EXTRANJERIA, TIPODOC_DNI, TIPODOC_NO_SE_CONOCE
from phr.common.models import ConfiguracionConexionInternet
from phr.reniec.forms import CiudadanoRNForm
from phr.ubigeo.models import UbigeoDepartamento, UbigeoDistrito, UbigeoLocalidad, UbigeoPais, UbigeoProvincia
from phr.utils.functions import ping_ws_ciudadano

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)
logger = logging.getLogger(__name__)


# =============================================================================
# CIUDADANOS GENERAL |
# -----------------------------------------------------------------------------
@method_decorator(cache_page(CACHE_TTL), name='dispatch')
class CiudadanoBusquedaAPIView(generics.ListAPIView):
    serializer_class = CiudadanoSerializer

    def get_queryset(self):
        q = self.request.query_params.get('q')
        if q:
            return Ciudadano.objects.filter(
                Q(numero_documento__iexact=q) | Q(cui__iexact=q) | Q(uuid__icontains=q) |
                Q(apellido_paterno__icontains=q) | Q(apellido_materno__icontains=q) | Q(nombres__icontains=q)
            ).order_by('numero_documento')
        else:
            return Ciudadano.objects.all()


@method_decorator(cache_page(CACHE_TTL), name='dispatch')
class CiudadanoListarCrearAPIView(generics.ListCreateAPIView):
    serializer_class = CiudadanoSerializer

    def get_queryset(self):
        q = self.request.query_params.get('q')
        if q:
            return Ciudadano.objects.filter(
                Q(numero_documento__iexact=q) | Q(cui__iexact=q) | Q(uuid__icontains=q)).order_by('numero_documento')
        else:
            return Ciudadano.objects.all()

    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        try:
            departamento_domicilio = UbigeoDepartamento.objects.get(
                cod_ubigeo_reniec_departamento=self.request.data.get('departamento_domicilio'))
            provincia_domicilio = UbigeoProvincia.objects.get(
                cod_ubigeo_reniec_provincia=self.request.data.get('provincia_domicilio'))
            distrito_domicilio = UbigeoDistrito.objects.get(
                cod_ubigeo_reniec_distrito=self.request.data.get('distrito_domicilio'))
            data.update({
                'departamento_domicilio': {'id': departamento_domicilio.id, 'type': 'UbigeoDepartamento'},
                'provincia_domicilio': {'id': provincia_domicilio.id, 'type': 'UbigeoProvincia'},
                'distrito_domicilio': {'id': distrito_domicilio.id, 'type': 'UbigeoDistrito'},
            })
        except Exception as e:
            print(e)
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        try:
            departamento_domicilio = UbigeoDepartamento.objects.get(
                cod_ubigeo_reniec_departamento=self.request.POST.get('departamento_domicilio'))
            provincia_domicilio = UbigeoProvincia.objects.get(
                cod_ubigeo_reniec_provincia=self.request.POST.get('provincia_domicilio'))
            distrito_domicilio = UbigeoDistrito.objects.get(
                cod_ubigeo_reniec_distrito=self.request.POST.get('distrito_domicilio'))

            serializer.save(departamento_domicilio=departamento_domicilio, provincia_domicilio=provincia_domicilio,
                            distrito_domicilio=distrito_domicilio)
        except Exception as e:
            serializer.save()


@method_decorator(cache_page(CACHE_TTL), name='dispatch')
class CiudadanoEditarAPIView(RetrieveModelMixin, UpdateModelMixin, generics.GenericAPIView):
    serializer_class = CiudadanoSerializer
    lookup_field = 'numero_documento'
    queryset = []

    def get_object(self):
        return get_object_or_404(Ciudadano, numero_documento=self.kwargs.get('numero_documento'))

    def get(self, request, *args, **kwargs):
        return self.retrieve(request)

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            data = request.data.copy()
            ubigeo_provider = self.request.data.get('ubigeo_provider', 'inei').lower()
            update_domicilio = False
            if ubigeo_provider == 'inei':
                departamento_domicilio = UbigeoDepartamento.objects.get(
                    cod_ubigeo_inei_departamento=self.request.data.get('departamento_domicilio'))
                provincia_domicilio = UbigeoProvincia.objects.get(
                    cod_ubigeo_inei_provincia=self.request.data.get('provincia_domicilio'))
                distrito_domicilio = UbigeoDistrito.objects.get(
                    cod_ubigeo_inei_distrito=self.request.data.get('distrito_domicilio'))
                update_domicilio = True
            elif ubigeo_provider == 'reniec':
                departamento_domicilio = UbigeoDepartamento.objects.get(
                    cod_ubigeo_reniec_departamento=self.request.data.get('departamento_domicilio'))
                provincia_domicilio = UbigeoProvincia.objects.get(
                    cod_ubigeo_reniec_provincia=self.request.data.get('provincia_domicilio'))
                distrito_domicilio = UbigeoDistrito.objects.get(
                    cod_ubigeo_reniec_distrito=self.request.data.get('distrito_domicilio'))
                update_domicilio = True
            else:
                departamento_domicilio = UbigeoDepartamento.objects.none()
                provincia_domicilio = UbigeoProvincia.objects.none()
                distrito_domicilio = UbigeoDistrito.objects.none()
            if update_domicilio:
                data.update({
                    'departamento_domicilio': {'id': departamento_domicilio.id, 'type': 'UbigeoDepartamento'},
                    'provincia_domicilio': {'id': provincia_domicilio.id, 'type': 'UbigeoProvincia'},
                    'distrito_domicilio': {'id': distrito_domicilio.id, 'type': 'UbigeoDistrito'},
                })
        except Exception as ex:
            data = request.data
        serializer = self.get_serializer(instance, data=data, partial=False)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class CiudadanoDatosSISAPIView(RetrieveAPIView, CreateAPIView):
    """
    Obtiene datos de SIS del ciudadano, si cuenta con SIS, permite registrar datos manualmente si el sistema se
    encuentra configurado para trabajar en modo off-line
    """
    serializer_class = CiudadanoDatosSISSerializer
    queryset = []

    def get_ciudadano(self):
        tipo_documento = self.kwargs.get('tipo_documento', TIPODOC_DNI)
        numero_documento = self.kwargs.get('numero_documento')
        uuid = self.kwargs.get('uuid')
        if uuid:
            ciudadano = get_object_or_404(Ciudadano, uuid=uuid)
        else:
            ciudadano = get_object_or_404(Ciudadano, tipo_documento=tipo_documento, numero_documento=numero_documento)
        return ciudadano

    def get_object(self):
        ciudadano = self.get_ciudadano()
        try:
            datos_sis = CiudadanoDatosSIS.objects.get(
                ciudadano=ciudadano, modified__date=timezone.datetime.now().date())
            return datos_sis
        except CiudadanoDatosSIS.DoesNotExist:
            return None

    def get(self, request, *args, **kwargs):
        datos_sis = self.get_object()
        if datos_sis:
            serializer = CiudadanoDatosSISSerializer(instance=datos_sis)
            return Response(serializer.data)
        conexion_sis = False
        conexion_internet = ConfiguracionConexionInternet.objects.first()
        if conexion_internet and conexion_internet.con_conexion:
            try:
                ping_ws_ciudadano(conexion_internet.ping_time)
                conexion_sis = True
            except Exception:
                conexion_sis = False
        return Response({'conexion_internet': conexion_sis, 'datos_sis': 'No registra'}, status=HTTP_404_NOT_FOUND)

    def post(self, request, *args, **kwargs):
        conexion_internet = ConfiguracionConexionInternet.objects.first()
        if conexion_internet and conexion_internet.con_conexion:
            raise APIException(
                "El sistema está configurado para conectarse a SIS, no puede registrar datos manualmente")
        ciudadano = self.get_ciudadano()
        try:
            datos_sis = CiudadanoDatosSIS.objects.get(ciudadano=ciudadano)
        except CiudadanoDatosSIS.DoesNotExist:
            datos_sis = None
        serializer = CiudadanoDatosSISSerializer(data=request.data, instance=datos_sis)
        if serializer.is_valid():
            serializer.save(ciudadano=ciudadano)
            return Response(serializer.validated_data, status=HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class CiudadanoDataAPIView(RetrieveUpdateAPIView):
    """
    Devuelve o actualiza datos de ciudadano, integra consulta con RENIEC, MIGRACIONES y SIS
    """
    serializer_class = CiudadanoSerializer
    queryset = []

    def get_ciudadano(self, consulta_reniec=True, consulta_sis=True):
        tipo_documento = self.kwargs.get('tipo_documento', TIPODOC_DNI)
        numero_documento = self.kwargs.get('numero_documento')
        actualizar_sis = bool(int(self.request.GET.get('actualizar_sis', 0)))
        uuid = self.kwargs.get('uuid')
        ciudadano = None
        if uuid:
            ciudadano = get_object_or_404(Ciudadano, uuid=uuid)
        else:
            try:
                ciudadano = Ciudadano.objects.get(tipo_documento=tipo_documento, numero_documento=numero_documento)
            except Ciudadano.DoesNotExist:
                if tipo_documento in (TIPODOC_DNI, TDOC_HISMINSA_DNI) and consulta_reniec:
                    ciudadano = crear_actualizar_ciudadano_reniec(numero_documento)
                elif tipo_documento == TIPODOC_CARNET_EXTRANJERIA:
                    ciudadano = crear_actualizar_ciudadano_migraciones(numero_documento)
        if ciudadano:
            if (ciudadano.tiempo_desde_ultima_actualizacion.days > settings.ACTUALIZAR_DATOS_RENIEC_CADA_DIAS
                    or ciudadano.tiempo_desde_ultima_actualizacion.months > 0
                    or ciudadano.tiempo_desde_ultima_actualizacion.years > 0) and consulta_reniec:
                if ciudadano.tipo_documento == TIPODOC_DNI:
                    ciudadano = crear_actualizar_ciudadano_reniec(ciudadano.numero_documento, ciudadano.uuid)
                elif ciudadano.tipo_documento == TIPODOC_CARNET_EXTRANJERIA:
                    ciudadano = crear_actualizar_ciudadano_migraciones(ciudadano.numero_documento, ciudadano.uuid)
            if ciudadano and ciudadano.tipo_documento in (TIPODOC_DNI, TIPODOC_CARNET_EXTRANJERIA) and consulta_sis:
                ciudadano_verificar_sis(ciudadano, actualizar_sis)
            return ciudadano
        raise NotFound

    def get_object(self):
        return self.get_ciudadano(consulta_reniec=True, consulta_sis=True)

    def patch(self, request, *args, **kwargs):
        ciudadano = self.get_ciudadano(consulta_reniec=False, consulta_sis=False)
        data = self.request.data.copy()
        ubigeo_provider = data.get('ubigeo_provider', 'inei')
        filtro_base = 'cod_ubigeo_{provider}_{division}'
        pais_origen = self.obtener_pais_origen(ciudadano, data, filtro_base, ubigeo_provider)
        self.datos_ubigeo_nacimiento(ciudadano, data.get('nacimiento_ubigeo'), ubigeo_provider, filtro_base)
        (pais_domicilio, departamento_domicilio, provincia_domicilio, distrito_domicilio,
         localidad_domicilio) = self.obtener_datos_domicilio(ciudadano, data, filtro_base, ubigeo_provider)
        (pais_domicilio_actual, departamento_domicilio_actual, provincia_domicilio_actual, distrito_domicilio_actual,
         localidad_domicilio_actual) = self.obtener_datos_domicilio_actual(ciudadano, data, filtro_base,
                                                                           ubigeo_provider)
        try:
            data.update({
                'tipo_documento': data.get('tipo_documento') or ciudadano.tipo_documento,
                'numero_documento': data.get('numero_documento') or ciudadano.numero_documento,
            })
            serializer = CiudadanoSerializer(data=data, instance=ciudadano)
            if serializer.is_valid():
                serializer.save(
                    pais_origen=pais_origen,
                    pais_domicilio=pais_domicilio,
                    departamento_domicilio=departamento_domicilio,
                    provincia_domicilio=provincia_domicilio,
                    distrito_domicilio=distrito_domicilio,
                    localidad_domicilio=localidad_domicilio,
                    pais_domicilio_actual=pais_domicilio_actual,
                    departamento_domicilio_actual=departamento_domicilio_actual,
                    provincia_domicilio_actual=provincia_domicilio_actual,
                    distrito_domicilio_actual=distrito_domicilio_actual,
                    localidad_domicilio_actual=localidad_domicilio_actual,
                )
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
        except Exception as ex:
            return Response({'errors': [{'detail': str(ex)}]}, HTTP_400_BAD_REQUEST)

    def obtener_pais_origen(self, ciudadano, data, filtro_base, ubigeo_provider):
        try:
            filtro_pais = {
                filtro_base.format(
                    provider=ubigeo_provider, division='pais'): data.pop('pais_domicilio')[0]
            }
            return UbigeoPais.objects.get(**filtro_pais)
        except (UbigeoPais.DoesNotExist, KeyError):
            return ciudadano.pais_origen

    def datos_ubigeo_nacimiento(self, ciudadano, nacimiento_ubigeo, ubigeo_provider, filtro_base):
        if nacimiento_ubigeo and len(nacimiento_ubigeo) == 6:
            filtro_distrito = {
                filtro_base.format(provider=ubigeo_provider, division='distrito'): nacimiento_ubigeo
            }
            try:
                distrito_nacimiento = UbigeoDistrito.objects.get(**filtro_distrito)
                ciudadano.distrito_nacimiento = distrito_nacimiento
                ciudadano.provincia_nacimiento = distrito_nacimiento.provincia
                ciudadano.departamento_nacimiento = distrito_nacimiento.departamento
                ciudadano.save()
            except UbigeoDistrito.DoesNotExist:
                pass

    def obtener_datos_domicilio(self, ciudadano, data, filtro_base, provider):
        try:
            filtro_pais = {
                filtro_base.format(provider=provider, division='pais'): data.pop('pais_domicilio')[0]
            }
            pais = UbigeoPais.objects.get(**filtro_pais)
        except (UbigeoPais.DoesNotExist, KeyError):
            pais = ciudadano.pais_domicilio
        try:
            filtro_dep = {
                filtro_base.format(provider=provider, division='departamento'): data.pop('departamento_domicilio')[0]
            }
            departamento = UbigeoDepartamento.objects.get(**filtro_dep)
        except (UbigeoDepartamento.DoesNotExist, KeyError):
            departamento = ciudadano.departamento_domicilio
        try:
            filtro_prov = {
                filtro_base.format(provider=provider, division='provincia'): data.pop('provincia_domicilio')[0]
            }
            provincia = UbigeoProvincia.objects.get(**filtro_prov)
        except (UbigeoProvincia.DoesNotExist, KeyError):
            provincia = ciudadano.provincia_domicilio
        try:
            filtro_dist = {
                filtro_base.format(provider=provider, division='distrito'): data.pop('distrito_domicilio')[0]
            }
            distrito = UbigeoDistrito.objects.get(**filtro_dist)
        except (UbigeoDistrito.DoesNotExist, KeyError):
            distrito = ciudadano.distrito_domicilio
        try:
            filtro_localidad = {
                filtro_base.format(provider=provider, division='localidad'): data.pop('localidad_domicilio')[0]
            }
            localidad = UbigeoLocalidad.objects.get(**filtro_localidad)
        except (UbigeoLocalidad.DoesNotExist, UbigeoLocalidad.MultipleObjectsReturned, KeyError):
            localidad = ciudadano.localidad_domicilio

        return pais, departamento, provincia, distrito, localidad

    def obtener_datos_domicilio_actual(self, ciudadano, data, filtro_base, provider):
        try:
            filtro_pais = {
                filtro_base.format(provider=provider, division='pais'): data.pop('pais_domicilio_actual')[0]
            }
            pais = UbigeoPais.objects.get(**filtro_pais)
        except (UbigeoPais.DoesNotExist, KeyError):
            pais = ciudadano.pais_domicilio_actual
        try:
            filtro_dep = {
                filtro_base.format(
                    provider=provider, division='departamento'): data.pop('departamento_domicilio_actual')[0]
            }
            departamento = UbigeoDepartamento.objects.get(**filtro_dep)
        except (UbigeoDepartamento.DoesNotExist, KeyError):
            departamento = ciudadano.departamento_domicilio_actual
        try:
            filtro_prov = {
                filtro_base.format(provider=provider, division='provincia'): data.pop('provincia_domicilio_actual')[0]
            }
            provincia = UbigeoProvincia.objects.get(**filtro_prov)
        except (UbigeoProvincia.DoesNotExist, KeyError):
            provincia = ciudadano.provincia_domicilio_actual
        try:
            filtro_dist = {
                filtro_base.format(provider=provider, division='distrito'): data.pop('distrito_domicilio_actual')[0]
            }
            distrito = UbigeoDistrito.objects.get(**filtro_dist)
        except (UbigeoDistrito.DoesNotExist, KeyError):
            distrito = ciudadano.distrito_domicilio_actual
        try:
            filtro_localidad = {
                filtro_base.format(provider=provider, division='localidad'): data.pop('localidad_domicilio_actual')[0]
            }
            localidad = UbigeoLocalidad.objects.get(**filtro_localidad)
        except (UbigeoLocalidad.DoesNotExist, UbigeoLocalidad.MultipleObjectsReturned, KeyError):
            localidad = ciudadano.localidad_domicilio_actual

        return pais, departamento, provincia, distrito, localidad


class CiudadanoBuscarDNIAPIView(ListAPIView):
    """
    Busca entre los ciudadanos indocumentados cualquier coincidencia con un registro obtenido de RENIEC con el
    número de documento enviado en el parámetro de búsqueda,  de encontrar varias coincidencias,  devuelve una
    lista, de encontrar una sola coincidencia, asigna el DNI al resultado encontrado y actualiza datos con los
    obtenidos en la consulta a RENIEC.
    """
    serializer_class = CiudadanoSerializer

    def get_queryset(self):
        if self.queryset is None:
            dni = self.kwargs.get('nro_doc')
            ciudadano = Ciudadano.objects.filter(numero_documento=dni)
            if len(ciudadano) == 1:
                return ciudadano

            url = '{host}/api/v1/ciudadanos/{tipo_documento}/{numero_documento}/'.format(
                host=settings.MPI_CENTRAL_HOST,
                tipo_documento=TIPODOC_DNI,
                numero_documento=dni
            )
            headers = {'Authorization': 'Bearer {token}'.format(token=settings.MPI_CENTRAL_TOKEN)}
            response = requests.get(url, **{'headers': headers})
            if is_success(response.status_code):
                data = response.json()
                apellido_paterno = data.get('apellido_paterno')
                apellido_materno = data.get('apellido_materno')
                nombres = data.get('nombres')
                fecha_nacimiento = datetime.datetime.strptime(data.get('fecha_nacimiento'), '%d/%m/%Y').date()
                sexo = data.get('sexo')
                filtro = {
                    'apellido_paterno': apellido_paterno, 'apellido_materno': apellido_materno,
                    'nombres': nombres, 'fecha_nacimiento': fecha_nacimiento, 'sexo': sexo,
                    'tipo_documento': TIPODOC_NO_SE_CONOCE
                }
                ciudadanos = Ciudadano.objects.filter(**filtro)
                if len(ciudadanos) == 1:
                    self.queryset = [crear_actualizar_ciudadano_reniec(dni, ciudadanos.first().uuid)]
                else:
                    self.queryset = ciudadanos
        return self.queryset


class CiudadanoBuscarDataAPIView(ListAPIView):
    """
    Busca ciudadanos que coincidan con el parámtero de búsqueda enviado.

    Parámetros aceptados:
    `apellido_paterno`,
    `apellido_materno`,
    `nombres`,
    `numero_documento`,

    Ejemplo de envío de parámetros:
    `/api/v1/ciudadano/buscar/?apellido_paterno=PEREZ&nombres=PEPITO`
    """
    serializer_class = CiudadanoDataBasicaSerializer

    def get_queryset(self):
        ap_paterno = self.request.GET.get('ap_paterno')
        ap_materno = self.request.GET.get('ap_materno')
        nombres = self.request.GET.get('nombres')
        dni = self.request.GET.get('dni')
        filtro = {}
        if ap_paterno:
            filtro.update({'apellido_paterno__icontains': ap_paterno})
        if ap_materno:
            filtro.update({'apellido_materno__icontains': ap_materno})
        if nombres:
            filtro.update({'nombres__icontains': nombres})
        if dni:
            filtro.update({'numero_documento__icontains': dni})
        if filtro:
            return Ciudadano.objects.filter(**filtro).order_by('numero_documento')
        else:
            return Ciudadano.objects.none()


class CiudadanoCrearDataAPIView(CreateAPIView):
    serializer_class = CiudadanoSerializer
    queryset = Ciudadano.objects.none()

    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        ubigeo_provider = data.get('ubigeo_provider', 'inei')
        filtro_base = 'cod_ubigeo_{provider}_{division}'
        pais_origen = self.obtener_pais_origen(data, filtro_base, ubigeo_provider)
        (pais_domicilio, departamento_domicilio, provincia_domicilio, distrito_domicilio,
         localidad_domicilio) = self.obtener_datos_domicilio(data, filtro_base, ubigeo_provider)
        (pais_domicilio_actual, departamento_domicilio_actual, provincia_domicilio_actual, distrito_domicilio_actual,
         localidad_domicilio_actual) = self.obtener_datos_domicilio_actual(data, filtro_base, ubigeo_provider)
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.save(
                pais_origen=pais_origen,
                pais_domicilio=pais_domicilio,
                departamento_domicilio=departamento_domicilio,
                provincia_domicilio=provincia_domicilio,
                distrito_domicilio=distrito_domicilio,
                localidad_domicilio=localidad_domicilio,
                pais_domicilio_actual=pais_domicilio_actual,
                departamento_domicilio_actual=departamento_domicilio_actual,
                provincia_domicilio_actual=provincia_domicilio_actual,
                distrito_domicilio_actual=distrito_domicilio_actual,
                localidad_domicilio_actual=localidad_domicilio_actual,
            )
            headers = self.get_success_headers(serializer.data)
            nuevo_ciudadano = Ciudadano.objects.get(uuid=serializer.data.get('uuid'))
            self.guardar_datos_ubigeo_nacimiento(
                nuevo_ciudadano, serializer.data.get('nacimiento_ubigeo'), ubigeo_provider, filtro_base)
            serializer_data = serializer.data.copy()
            serializer_data['numero_documento'] = nuevo_ciudadano.numero_documento
            return Response(serializer_data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def obtener_pais_origen(self, data, filtro_base, ubigeo_provider):
        try:
            filtro_pais = {
                filtro_base.format(
                    provider=ubigeo_provider, division='pais'): data.pop('pais_origen')[0]
            }
            return UbigeoPais.objects.get(**filtro_pais)
        except (UbigeoPais.DoesNotExist, KeyError):
            return None

    def obtener_datos_domicilio(self, data, filtro_base, provider):
        try:
            filtro_pais = {
                filtro_base.format(provider=provider, division='pais'): data.pop('pais_domicilio')[0]
            }
            pais = UbigeoPais.objects.get(**filtro_pais)
        except (UbigeoPais.DoesNotExist, KeyError):
            pais = None
        try:
            filtro_dep = {
                filtro_base.format(provider=provider, division='departamento'): data.pop('departamento_domicilio')[0]
            }
            departamento = UbigeoDepartamento.objects.get(**filtro_dep)
        except (UbigeoDepartamento.DoesNotExist, KeyError):
            departamento = None
        try:
            filtro_prov = {
                filtro_base.format(provider=provider, division='provincia'): data.pop('provincia_domicilio')[0]
            }
            provincia = UbigeoProvincia.objects.get(**filtro_prov)
        except (UbigeoProvincia.DoesNotExist, KeyError):
            provincia = None
        try:
            filtro_dist = {
                filtro_base.format(provider=provider, division='distrito'): data.pop('distrito_domicilio')[0]
            }
            distrito = UbigeoDistrito.objects.get(**filtro_dist)
        except (UbigeoDistrito.DoesNotExist, KeyError):
            distrito = None
        try:
            filtro_localidad = {
                filtro_base.format(provider=provider, division='localidad'): data.pop('localidad_domicilio')[0]
            }
            localidad = UbigeoLocalidad.objects.get(**filtro_localidad)
        except (UbigeoLocalidad.DoesNotExist, UbigeoLocalidad.MultipleObjectsReturned, KeyError):
            localidad = None

        return pais, departamento, provincia, distrito, localidad

    def obtener_datos_domicilio_actual(self, data, filtro_base, provider):
        try:
            filtro_pais = {
                filtro_base.format(provider=provider, division='pais'): data.pop('pais_domicilio_actual')[0]
            }
            pais = UbigeoPais.objects.get(**filtro_pais)
        except (UbigeoPais.DoesNotExist, KeyError):
            pais = None
        try:
            filtro_dep = {
                filtro_base.format(
                    provider=provider, division='departamento'): data.pop('departamento_domicilio_actual')[0]
            }
            departamento = UbigeoDepartamento.objects.get(**filtro_dep)
        except (UbigeoDepartamento.DoesNotExist, KeyError):
            departamento = None
        try:
            filtro_prov = {
                filtro_base.format(provider=provider, division='provincia'): data.pop('provincia_domicilio_actual')[0]
            }
            provincia = UbigeoProvincia.objects.get(**filtro_prov)
        except (UbigeoProvincia.DoesNotExist, KeyError):
            provincia = None
        try:
            filtro_dist = {
                filtro_base.format(provider=provider, division='distrito'): data.pop('distrito_domicilio_actual')[0]
            }
            distrito = UbigeoDistrito.objects.get(**filtro_dist)
        except (UbigeoDistrito.DoesNotExist, KeyError):
            distrito = None
        try:
            filtro_localidad = {
                filtro_base.format(provider=provider, division='localidad'): data.pop('localidad_domicilio_actual')[0]
            }
            localidad = UbigeoLocalidad.objects.get(**filtro_localidad)
        except (UbigeoLocalidad.DoesNotExist, UbigeoLocalidad.MultipleObjectsReturned, KeyError):
            localidad = None

        return pais, departamento, provincia, distrito, localidad

    def guardar_datos_ubigeo_nacimiento(self, ciudadano, nacimiento_ubigeo, ubigeo_provider, filtro_base):
        if nacimiento_ubigeo and len(nacimiento_ubigeo) == 6:
            filtro_distrito = {
                filtro_base.format(provider=ubigeo_provider, division='distrito'): nacimiento_ubigeo
            }
            try:
                distrito_nacimiento = UbigeoDistrito.objects.get(**filtro_distrito)
                ciudadano.distrito_nacimiento = distrito_nacimiento
                ciudadano.provincia_nacimiento = distrito_nacimiento.provincia
                ciudadano.departamento_nacimiento = distrito_nacimiento.departamento
                ciudadano.save()
            except UbigeoDistrito.DoesNotExist:
                pass


@method_decorator(cache_page(CACHE_TTL), name='dispatch')
class CiudadanoVerNombresAPIView(RetrieveAPIView):
    serializer_class = CiudadanoNombreSerializer

    def get_object(self):
        try:
            numero_documento = self.kwargs.get('numero_documento', '')
            if numero_documento:
                return Ciudadano.objects.get(tipo_documento=TIPODOC_DNI, numero_documento=numero_documento)
        except Ciudadano.DoesNotExist:
            raise NotFound


class CiudadanoAntecedenteListarAPIView(ListAPIView):
    """
    Lista antecedentes personales de ciudadano
    """
    serializer_class = AntecedenteCiudadanoSerializer

    def get_queryset(self):
        tipo_doc = "{:02}".format(int(self.kwargs.get('tipo_doc')))
        nro_doc = self.kwargs.get('nro_doc')
        ciudadano = get_object_or_404(Ciudadano, tipo_documento=tipo_doc, numero_documento=nro_doc)
        return AntecedenteCiudadano.objects.filter(ciudadano=ciudadano).order_by('-fecha_inicio')


class CiudadanoAntecedenteCrearActualizarAPIView(APIView):
    """
    Registra y/o Actualiza antecedendes personales de ciudadano.

    Trama de ejemplo de entrada:

    ```
    {
        "anio_diagnostico": 2005,
        "ciex": "E669",
        "codigo_antecedente_sugerido": "ASP012",
        "codigo_ciex": "E669",
        "consulta_paciente": "aaaaaaaa-ffff-4444-9999-4321abcdef44",
        "grupo_antecedente": "1",
        "nombre_antecedente_sugerido": "Obesidad",
        "numero_documento": "44332211",
        "observaciones": "Observaciones antecedentes",
        "registro_antecedente": "1",
        "subgrupo_antecedente": "1",
        "tipo_documento": "01"
    }
    ```
    """

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body.decode())
        tipo_doc = data.get('tipo_documento')
        nro_doc = data.get('numero_documento')
        ciex = data.get('ciex')
        codigo_antecedente_sugerido = data.get('codigo_antecedente_sugerido')
        ciudadano = get_object_or_404(Ciudadano, tipo_documento=tipo_doc, numero_documento=nro_doc)
        data.update({'ciudadano': {'type': 'Ciudadano', 'id': ciudadano.pk}})
        antecedente, _ = AntecedenteCiudadano.objects.get_or_create(
            ciudadano=ciudadano,
            ciex=ciex,
            codigo_antecedente_sugerido=codigo_antecedente_sugerido,
            consulta_paciente=data.get('consulta_paciente'),
            es_removido=False
        )
        serializer = AntecedenteCiudadanoSerializer(instance=antecedente, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'data': serializer.data})
        else:
            return JsonResponse({'errors': serializer.errors}, status=400)


class CiudadanoAntecedenteEliminarAPIView(DestroyAPIView):
    """
    Elimina registro de antecedente personal de ciudadano.

    Se debe enviar el parámetro `?consulta` en la URL para realizar validación de consistencia del antecedente
    antes de eliminarlo
    """
    serializer_class = AntecedenteCiudadanoSerializer

    def get_object(self):
        consulta = self.request.GET.get('consulta')
        antecedente_uuid = self.kwargs.get('antecedente_uuid')
        antecedente = get_object_or_404(AntecedenteCiudadano, uuid=antecedente_uuid)
        if str(antecedente.consulta_paciente) == consulta:
            return antecedente
        raise NotFound


class CiudadanoAntecedenteFamListarAPIView(ListAPIView):
    """
    Lista antecedentes de familiares de ciudadano
    """
    serializer_class = AntecedenteFamiliarCiudadanoSerializer

    def get_queryset(self):
        tipo_doc = "{:02}".format(int(self.kwargs.get('tipo_doc')))
        nro_doc = self.kwargs.get('nro_doc')
        ciudadano = get_object_or_404(Ciudadano, tipo_documento=tipo_doc, numero_documento=nro_doc)
        return AntecedenteFamiliar.objects.filter(ciudadano=ciudadano).order_by('-fecha_inicio')


class CiudadanoAntecedenteFamCrearActualizarAPIView(APIView):
    """
    Registra y/o Actualiza antecedendes de familiares de ciudadano.

    Trama de ejemplo de entrada:

    ```
    payload = {
        'tipo_documento': '01',
        'numero_documento': '44332211',
        'codigo_ciex': 'M610',
        'fecha_inicio': '2017-04-15',
        'fecha_fin': '2017-04-26',
        'observaciones': '',
        'grupo_antecedente': '2',
        'subgrupo_antecedente': '1',
        'parentesco': '1',
        'observaciones': 'observación de mañana',
        'registro_antecedente': '1',
        'consulta_paciente': 'aaaaaaaa-ffff-4444-9999-4321abcdef44',
    }
    ```
    """

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body.decode())
        tipo_doc = data.get('tipo_documento')
        nro_doc = data.get('numero_documento')
        ciex = data.get('codigo_ciex')
        codigo_antecedente_sugerido = data.get('codigo_antecedente_sugerido')
        ciudadano = get_object_or_404(Ciudadano, tipo_documento=tipo_doc, numero_documento=nro_doc)
        data.update({
            'ciudadano': {'type': 'Ciudadano', 'id': ciudadano.pk},
        })
        antecedente, _ = AntecedenteFamiliar.objects.get_or_create(
            ciudadano=ciudadano,
            ciex=ciex,
            codigo_antecedente_sugerido=codigo_antecedente_sugerido,
            consulta_paciente=data.get('consulta_paciente'),
            es_removido=False
        )
        serializer = AntecedenteFamiliarCiudadanoSerializer(instance=antecedente, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'data': 'ok'})
        else:
            return JsonResponse({'errors': serializer.errors}, status=400)


class CiudadanoAntecedenteFamiliarEliminarAPIView(DestroyAPIView):
    """
    Elimina registro de antecedente familiar de ciudadano.

    Se debe enviar el parámetro `?consulta` en la URL para realizar validación de consistencia del antecedente
    antes de eliminarlo
    """
    serializer_class = AntecedenteFamiliarCiudadanoSerializer

    def get_object(self):
        consulta = self.request.GET.get('consulta')
        antecedente_uuid = self.kwargs.get('antecedente_uuid')
        antecedente = get_object_or_404(AntecedenteFamiliar, uuid=antecedente_uuid)
        if str(antecedente.consulta_paciente) == consulta:
            return antecedente
        raise NotFound


class CiudadanoAntecedenteMedicacionCrearAPIView(CreateAPIView):
    """
    Registra antecedende de medicación habitual de ciudadano.

    Trama de ejemplo de entrada:

    ```
    payload = {
        'familia_medicamento': 'F001',
        'medicamento': 'M0004',
        'dosis': 5,
        'frecuencia_horas': 8,
        'fecha_inicio': '2017-04-15',
        'consulta_paciente': 'aaaaaaaa-ffff-4444-9999-4321abcdef44',
        'ciudadano': 'aaaabbbb-ffff-4466-0000-1234abcdef22',
    }
    ```
    """
    serializer_class = AntecedenteMedicacionHabitualSerializer


class CiudadanoAntecedenteMedicacionListarAPIView(ListAPIView):
    """
    Lista antecedendes de medicación habitual de ciudadano.
    """
    serializer_class = AntecedenteMedicacionHabitualSerializer

    def get_queryset(self):
        tipo_doc = self.kwargs.get('tipo_doc')
        nro_doc = self.kwargs.get('nro_doc')
        ciudadano = get_object_or_404(Ciudadano, tipo_documento=tipo_doc, numero_documento=nro_doc)
        return AntecedenteMedicacionHabitual.objects.filter(ciudadano=ciudadano.uuid).order_by('fecha_inicio')


class CiudadanoAntecedenteMedicacionEliminarAPIView(DestroyAPIView):
    """
    Elimina registro de antecedente de medicación habitual de ciudadano.

    Se debe enviar el parámetro `?consulta` en la URL para realizar validación de consistencia del antecedente
    antes de eliminarlo
    """
    serializer_class = AntecedenteMedicacionHabitualSerializer

    def get_object(self):
        consulta = self.request.GET.get('consulta')
        antecedente_pk = self.kwargs.get('pk')
        antecedente = get_object_or_404(AntecedenteMedicacionHabitual, pk=antecedente_pk)
        if str(antecedente.consulta_paciente) == consulta:
            return antecedente
        raise NotFound


class CiudadanoAntecedenteReaccionAdversaMedicamentoListarAPIVew(ListAPIView):
    """
    Lista antecedentes de reacciones adversas a medicamento de ciudadano
    """
    serializer_class = AntecedenteReaccionAdversaMedicamentoSerializer
    queryset = None

    def get_queryset(self):
        antecedentes = AntecedenteReaccionAdversaMedicamento.objects.filter(
            ciudadano=self.kwargs.get('ciudadano_uuid')
        ).order_by('medicamento')
        return antecedentes


class CiudadanoAntecedenteReaccionAdversaMedicamentoCrearActualizarAPIVew(APIView):
    """
    Registra y/o actualiza antecedendes de reacciones adversas a medicamentos de ciudadano.

    Trama de ejemplo de entrada:

    ```
    payload = {
        'familia_medicamento': 'F005'
        'medicamento': 'M0014',
        'anio_diagnostico': 2011,
        'observaciones': 'Foo bar foobar barfoo',
        'registro_antecedente': '1',
        'consulta_paciente': 'aaaaaaaa-ffff-4444-9999-4321abcdef44',
        'ciudadano': 'aaaabbbb-ffff-4466-0000-1234abcdef22'
    }
    ```
    """

    def post(self, request, *args, **kwargs):
        ciudadano = get_object_or_404(Ciudadano, uuid=self.request.data.get('ciudadano'))
        antecedente, _ = AntecedenteReaccionAdversaMedicamento.objects.get_or_create(
            medicamento=self.request.data.get('medicamento'),
            familia_medicamento=self.request.data.get('familia_medicamento'),
            ciudadano=ciudadano.uuid,
            consulta_paciente=self.request.data.get('consulta_paciente'),
        )
        serializer = AntecedenteReaccionAdversaMedicamentoSerializer(instance=antecedente, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data})
        else:
            return Response({'errors': serializer.errors}, status=HTTP_400_BAD_REQUEST)


class CiudadanoAntecedenteReaccionAdversaMedicamentoQuitarAPIVew(DestroyAPIView):
    """
    Elimina registro de antecedente de reacción adversa a medicamento de ciudadano.

    Se debe enviar el parámetro `?consulta` en la URL para realizar validación de consistencia del antecedente
    antes de eliminarlo
    """
    serializer_class = AntecedenteReaccionAdversaMedicamentoSerializer

    def get_object(self):
        consulta = self.request.GET.get('consulta')
        antecedente_pk = self.kwargs.get('pk')
        antecedente = get_object_or_404(AntecedenteReaccionAdversaMedicamento, uuid=antecedente_pk)
        if str(antecedente.consulta_paciente) == consulta:
            return antecedente
        raise NotFound


# =============================================================================
# CNV - RN |
# -----------------------------------------------------------------------------
@method_decorator(cache_page(CACHE_TTL), name='dispatch')
class BuscarCiudadanoRN(ListAPIView):
    serializer_class = CiudadanoRNSerializer

    def get_queryset(self):
        param_search = self.request.GET.get('q', '')
        if param_search:
            if len(param_search) == 10:
                return CiudadanoRN.objects.filter(cui=param_search)
            else:
                return CiudadanoRN.objects.filter(ciudadano__numero_documento=param_search)
        return []


@method_decorator(cache_page(CACHE_TTL), name='dispatch')
class VerCiudadanoRN(RetrieveAPIView):
    serializer_class = CiudadanoRNSerializer
    queryset = []

    def get_object(self):
        return get_object_or_404(CiudadanoRN, cui=self.kwargs.get('cui', ''))


class CrearCiudadanoRN(CreateAPIView):
    permission_classes = []
    serializer_class = CiudadanoRNSerializer
    queryset = []

    def perform_create(self, serializer):
        serializer.save()


class ActualizarDatosRNAPIView(APIView):
    serializer = None

    def get_object(self, cui):
        return get_object_or_404(CiudadanoRN, cui=cui)

    def post(self, request, *args, **kwargs):
        ciudadano_rn = self.get_object(self.kwargs.get('cui'))
        serializer = self.serializer(ciudadano_rn, data=self.request.POST)
        if serializer.is_valid():
            serializer.save()
            self.save_parto_data(request.POST, ciudadano_rn)
            return Response(serializer.data)
        else:
            print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def save_parto_data(data, ciudadano_rn):
        nombres = data.get('nombres')
        sintomas = data.getlist('signos_sintomas_parto')
        if sintomas or nombres:
            if sintomas:
                ciudadano_rn.signos_sintomas_parto = sintomas
            if nombres:
                ciudadano_rn.ciudadano.nombres = nombres
                ciudadano_rn.ciudadano.apellido_materno = ciudadano_rn.primer_apellido_madre
            ciudadano_rn.ciudadano.save()


class ActualizarFichaRN(ActualizarDatosRNAPIView):
    serializer = CiudadanoFichaRNSerializer


class ActualizarControlRN(ActualizarDatosRNAPIView):
    serializer = CiudadanoFichaControlRNSerializer


class ActualizarPartoRN(ActualizarDatosRNAPIView):
    serializer = CiudadanoFichaPartoRNSerializer


class ActualizarEgresoRN(ActualizarDatosRNAPIView):
    serializer = CiudadanoFichaEgresoRNSerializer


@method_decorator(cache_page(CACHE_TTL), name='dispatch')
class CiudadanoMadreHijos(ListAPIView):
    serializer_class = CiudadanoMadreHijosSerializer

    def get_queryset(self):
        dni_madre = self.kwargs.get('dni_madre')
        parientes_obj = CiudadanoParentesco.objects.filter(titular=dni_madre, parentesco=2)
        parientes_list = []
        parientes = Ciudadano.objects.filter(
            numero_documento__in=[pariente.pariente for pariente in parientes_obj]).order_by('numero_documento')
        for pariente in parientes:
            parientes_list.append(pariente)

        return parientes_list


class ListaCiudadanoRNMadre(ListAPIView):
    serializer_class = CiudadanoRNSerializer

    def get_queryset(self):
        numero_doc_madre = self.kwargs.get('numero_doc_madre')
        tipo_doc_madre = self.kwargs.get('tipo_doc_madre')
        return CiudadanoRN.objects.filter(tipo_doc_madre=tipo_doc_madre,
                                          numero_doc_madre=numero_doc_madre).order_by('cui')


class ActualizarPadron(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        post_ciudadano = json.loads(request.body.decode())
        form_ciudadano = CiudadanoPadronForm(post_ciudadano)
        form_ciudadano_rn = CiudadanoRNForm(post_ciudadano)
        cui = post_ciudadano.get('cui')
        ciudadano_rn = CiudadanoRN()
        if cui:
            try:
                ciudadano_rn = CiudadanoRN.objects.get(cui=cui)
            except CiudadanoRN.DoesNotExist:
                if form_ciudadano_rn.is_valid():
                    ciudadano_rn = form_ciudadano_rn.save(commit=False)
                    ciudadano_rn.numero_dni_ciudadano = post_ciudadano.get('numero_documento', '')
                    ciudadano_rn.save(crear_ciudadano=False)
                else:
                    return JsonResponse({'errors': form_ciudadano_rn.errors})
        if form_ciudadano.is_valid():
            post_ciudadano.update({'origen_datos': 4, 'tipo_documento': '01'})
            nuevo_ciudadano = False
            try:
                ciudadano = Ciudadano.objects.get(numero_documento=form_ciudadano.cleaned_data.get('numero_documento'),
                                                  tipo_documento='01')
                ciudadano = CiudadanoPadronForm(data=post_ciudadano, instance=ciudadano).save()
            except Ciudadano.DoesNotExist:
                ciudadano = CiudadanoPadronForm(data=post_ciudadano).save()
                nuevo_ciudadano = True
            if form_ciudadano.cleaned_data.get('nacimiento_ubigeo'):
                ubigeo = form_ciudadano.cleaned_data.get('nacimiento_ubigeo')
                departamento_nacimiento = UbigeoDepartamento.objects.get(cod_ubigeo_inei_departamento=ubigeo[:2])
                provincia_nacimiento = UbigeoProvincia.objects.get(cod_ubigeo_inei_provincia=ubigeo[:4])
                distrito_nacimiento = UbigeoDistrito.objects.get(cod_ubigeo_inei_distrito=ubigeo)
                ciudadano.departamento_nacimiento = departamento_nacimiento
                ciudadano.provincia_nacimiento = provincia_nacimiento
                ciudadano.distrito_nacimiento = distrito_nacimiento
                ciudadano.save()
            if nuevo_ciudadano and ciudadano_rn.ciudadano is not None:
                ciudadano_rn.ciudadano.es_removido = True
                ciudadano_rn.ciudadano.save()
            ciudadano_rn.ciudadano = ciudadano
            ciudadano_rn.save()
            return JsonResponse({'ciudadano': ciudadano.numero_documento})
        else:
            return JsonResponse({'errors': form_ciudadano.errors})


class ValidarNumeroDNI(APIView):
    """
    Permite validar el número de un DNI y su código de verificación.


    Ejemplo de trama de envío:
    ```
    payload = {
        'numero_documento': '44332211',
        'codigo_verificacion': '8',
    }
    ```

    :return: Diccionario con respuesta Verdadero/Falso según sea el caso
        ```
        response = {'datos_correctos': true}
        ```
        ó:
        ```
        response = {'datos_correctos': false}
        ```
    :rtype: dict
    """

    def post(self, request, *args, **kwargs):
        datos_correctos = False
        try:
            numero_documento = self.request.data.get('numero_documento')
            codigo_verificacion = self.request.data.get('codigo_verificacion')
            url = '{host}/api/v1/ciudadanos/{tipo_documento}/{numero_documento}/'.format(
                host=settings.MPI_CENTRAL_HOST,
                tipo_documento=TIPODOC_DNI,
                numero_documento=numero_documento
            )
            headers = {'Authorization': 'Bearer {token}'.format(token=settings.MPI_CENTRAL_TOKEN)}
            response = requests.get(url, **{'headers': headers})
            if is_success(response.status_code):
                data = response.json()
                datos_correctos = data.get('codigo_verificacion') == codigo_verificacion
        except Exception as ex:
            logger.warning('Error al conectarse a RENIEC', exc_info=True, extra={
                'errors': str(ex),
            })
            return Response({'error': str(ex)}, status=HTTP_400_BAD_REQUEST)

        return Response({'datos_correctos': datos_correctos})


class BuscarEESSRecienNacido(ListAPIView):
    serializer_class = CiudadanoRNSerializer

    def get_queryset(self):
        codigo_renaes = self.kwargs.get('codigo_renaes')
        fecha_inicio = timezone.now() - relativedelta(months=constants.MESES_LIMITE_CONSULTA_NACIDOS)
        filtro = {
            'codigo_renaes_adscrito': codigo_renaes,
            'fecha_nacimiento__gte': fecha_inicio.date()
        }
        return CiudadanoRN.objects.filter(**filtro).order_by('cui')


class FechaActualizacionCiudadanoView(RetrieveAPIView):
    serializer_class = CiudadanoFechaActualizacionSerializer
    renderer_classes = JSONRenderer, BrowsableAPIRenderer

    def get_object(self):
        return get_object_or_404(Ciudadano, uuid=self.kwargs.get('uuid'))
