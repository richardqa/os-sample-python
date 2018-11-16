# coding=utf-8
import re

from django.conf import settings
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from rest_framework.generics import ListAPIView, RetrieveAPIView, get_object_or_404
from rest_framework.metadata import SimpleMetadata
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.parsers import JSONParser
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer

from phr.common.drf_custom import StandardResultsSetPagination
from phr.establecimiento.api.serializers import (
    DetalleEstablecimientoSerializer, DiresaSerializer, ListaEstablecimientoSerializer,
    ListaEstablecimientoUbigeoSerializer, MicroredSerializer, RedSerializer, SectorSerializer, ServicioSerializer,
)
from phr.establecimiento.models import (
    Diresa, Establecimiento, EstablecimientoCategoria, EstablecimientoSector, Microred, Red, Servicio,
)
from phr.ubigeo.models import UbigeoDepartamento, UbigeoDistrito, UbigeoProvincia

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


@method_decorator(cache_page(CACHE_TTL), name='dispatch')
class ListaEstablecimientoAPI(ListAPIView):
    serializer_class = ListaEstablecimientoSerializer
    queryset = []

    def get_queryset(self):
        search_param = self.request.GET.get('q', '')
        categoria = self.request.GET.get('categoria')
        if len(search_param) >= 3 and not categoria:
            queryset = Establecimiento.objects.filter(
                Q(codigo_renaes__icontains=search_param) | Q(nombre__icontains=search_param)
            ).order_by('nombre')
        elif categoria and not search_param:
            queryset = Establecimiento.objects.filter(
                categoria__nombre_categoria=categoria).order_by('nombre')
        elif categoria and search_param:
            queryset = Establecimiento.objects.filter(
                Q(codigo_renaes__icontains=search_param) | Q(nombre__icontains=search_param),
                categoria__nombre_categoria=categoria).order_by('nombre')
        else:
            queryset = Establecimiento.objects.all().order_by('nombre')
        sector_param = self.request.GET.get('sector', '')
        queryset = establecimientos_sector(queryset, sector_param)
        return queryset


@method_decorator(cache_page(CACHE_TTL), name='dispatch')
class ListaEstablecimientosSectoresAPI(ListAPIView):
    serializer_class = SectorSerializer
    queryset = EstablecimientoSector.objects.all().order_by('codigo')


@method_decorator(cache_page(CACHE_TTL), name='dispatch')
class SectorDetalleAPI(RetrieveAPIView):
    serializer_class = SectorSerializer
    queryset = EstablecimientoSector.objects.all()


@method_decorator(cache_page(CACHE_TTL), name='dispatch')
class SectorRetrieveAPIView(RetrieveAPIView):
    serializer_class = SectorSerializer
    queryset = EstablecimientoSector.objects.all()
    lookup_url_kwarg = 'codigo'


@method_decorator(cache_page(CACHE_TTL), name='dispatch')
class ListaEstablecimientosPorSectorAPI(ListAPIView):
    serializer_class = ListaEstablecimientoSerializer
    queryset = Establecimiento.objects.all()

    def get_queryset(self):
        return Establecimiento.objects.filter(sector__pk=self.kwargs.get("pk"))


@method_decorator(cache_page(CACHE_TTL), name='dispatch')
class ListaEstablecimientosCercanosAPI(ListAPIView):
    serializer_class = ListaEstablecimientoSerializer
    queryset = []

    def get_queryset(self):
        qs = Establecimiento.objects.all()
        sector_param = self.request.GET.get('sector', '')
        banco_sangre = self.request.GET.get('banco_sangre', '')
        qs = establecimientos_sector(qs, sector_param)
        try:
            lon = float(self.request.query_params.get('lon'))
            lat = float(self.request.query_params.get('lat'))
            distance = float(self.request.query_params.get('distancia', 5))
            point = Point(lon, lat, srid=4326)
            filtro = {
                'location__distance_lte': (point, D(km=distance)),
            }
            if banco_sangre:
                filtro.update({'es_banco_sangre': True})
            qs = qs.annotate(
                distancia=Distance('location', point)
            ).filter(
                **filtro
            ).order_by('distancia')
        except (ValueError, TypeError) as ex:
            print(ex)
            return []
        return qs


@method_decorator(cache_page(CACHE_TTL), name='dispatch')
class DetalleEstablecimientoAPIView(RetrieveAPIView):
    """Detalle de un establecimiento"""
    serializer_class = DetalleEstablecimientoSerializer
    queryset = []

    def get_object(self):
        try:
            return get_object_or_404(
                Establecimiento, codigo_renaes=str(int(self.kwargs.get('cod_renaes', 0))))
        except:
            return get_object_or_404(
                Establecimiento, codigo_renaes=self.kwargs.get('cod_renaes', 0))


def establecimientos_sector(establecimientos, sector_param):
    if sector_param:
        if sector_param == 'all':
            return establecimientos.order_by('nombre')
        else:
            if sector_param == '1':
                return establecimientos.filter(sector__codigo__in=['1', '7', '14']).order_by('nombre')
            else:
                return establecimientos.filter(sector__codigo=sector_param).order_by('nombre')
    else:
        return establecimientos.order_by('nombre')


@method_decorator(cache_page(CACHE_TTL), name='dispatch')
class ListaEstablecimientoUbigeoAPI(ListAPIView):
    serializer_class = ListaEstablecimientoUbigeoSerializer
    pagination_class = StandardResultsSetPagination
    queryset = []

    def get_queryset(self):
        cod_ubigeo = self.kwargs.get('cod_ubigeo', '')
        categorias = []
        if self.request.GET.get('nivel'):
            niveles = self.request.GET.get('nivel').split(',')
            categorias = self.get_categorias(niveles)
        elif self.request.GET.get('categoria'):
            if self.request.GET.get('categoria') == '00':
                categorias = EstablecimientoCategoria.objects.all()
            else:
                categorias = [EstablecimientoCategoria.objects.get(nombre_categoria=self.request.GET.get('categoria'))]

        establecimientos = []
        if len(cod_ubigeo) == 2 and cod_ubigeo == '00':
            establecimientos = self.get_establecimientos_todos(categorias)
        elif len(cod_ubigeo) == 2:
            establecimientos = self.get_establecimientos_departamento(cod_ubigeo, categorias)
        elif len(cod_ubigeo) == 4:
            establecimientos = self.get_establecimientos_provincia(cod_ubigeo, categorias)
        elif len(cod_ubigeo) == 6:
            establecimientos = self.get_establecimientos_distrito(cod_ubigeo, categorias)

        search_param = self.request.GET.get('q')
        if search_param:
            establecimientos = establecimientos.filter(
                Q(codigo_renaes__icontains=search_param) | Q(nombre__icontains=search_param))
        sector_param = self.request.GET.get('sector')
        establecimientos = establecimientos_sector(establecimientos, sector_param)
        influenza = self.request.GET.get('influenza')
        if influenza:
            establecimientos = self.establecimientos_influenza(establecimientos, influenza)
        anemia = self.request.GET.get('anemia')
        if anemia:
            establecimientos = self.establecimientos_anemia(establecimientos, anemia)
        return establecimientos

    @staticmethod
    def establecimientos_influenza(establecimientos, influenza):
        return establecimientos.filter(tiene_influenza=influenza)

    @staticmethod
    def establecimientos_anemia(establecimientos, influenza):
        return establecimientos.filter(es_para_anemia=influenza)

    @staticmethod
    def get_categorias(niveles):
        categorias = []
        for nivel in niveles:
            if nivel == '1':
                categoria_i = ['I-1', 'I-2', 'I-3', 'I-4']
                categorias_est = EstablecimientoCategoria.objects.filter(nombre_categoria__in=categoria_i)
                for categoria_e in categorias_est:
                    categorias.append(categoria_e.id)
            if nivel == '2':
                categoria_i = ['II-1', 'II-2', 'II-E']
                categorias_est = EstablecimientoCategoria.objects.filter(nombre_categoria__in=categoria_i)
                for categoria_e in categorias_est:
                    categorias.append(categoria_e.id)
            if nivel == '3':
                categoria_i = ['III-1', 'III-2', 'III-E']
                categorias_est = EstablecimientoCategoria.objects.filter(nombre_categoria__in=categoria_i)
                for categoria_e in categorias_est:
                    categorias.append(categoria_e.id)
        return categorias

    def get_establecimientos_distrito(self, cod_ubigeo, categorias):
        if self.request.GET.get('provider', '') == 'reniec':
            distrito = get_object_or_404(UbigeoDistrito, cod_ubigeo_reniec_distrito=cod_ubigeo)
        else:
            distrito = get_object_or_404(UbigeoDistrito, cod_ubigeo_inei_distrito=cod_ubigeo)

        if categorias:
            establecimientos = Establecimiento.objects.filter(
                distrito=distrito, categoria__in=categorias).order_by('ubigeo')
            return establecimientos
        return Establecimiento.objects.filter(distrito=distrito).order_by('ubigeo')

    def get_establecimientos_provincia(self, cod_ubigeo, categorias):
        if self.request.GET.get('provider', '') == 'reniec':
            provincia = get_object_or_404(UbigeoProvincia, cod_ubigeo_reniec_provincia=cod_ubigeo)
        else:
            provincia = get_object_or_404(UbigeoProvincia, cod_ubigeo_inei_provincia=cod_ubigeo)

        if categorias:
            establecimientos = Establecimiento.objects.filter(
                provincia=provincia, categoria__in=categorias).order_by('ubigeo')
            return establecimientos
        return Establecimiento.objects.filter(provincia=provincia).order_by('ubigeo')

    def get_establecimientos_departamento(self, cod_ubigeo, categorias):
        if self.request.GET.get('provider', '') == 'reniec':
            departamento = get_object_or_404(UbigeoDepartamento, cod_ubigeo_reniec_departamento=cod_ubigeo)
        else:
            departamento = get_object_or_404(UbigeoDepartamento, cod_ubigeo_inei_departamento=cod_ubigeo)

        if categorias:
            establecimientos = Establecimiento.objects.filter(
                departamento=departamento, categoria__in=categorias).order_by('ubigeo')
            return establecimientos
        return Establecimiento.objects.filter(departamento=departamento).order_by('ubigeo')

    def get_establecimientos_todos(self, categorias):
        if categorias:
            establecimientos = Establecimiento.objects.filter(categoria__in=categorias).order_by('ubigeo')
            return establecimientos
        return Establecimiento.objects.all().order_by('ubigeo')


class UbigeoDiresaListAPI(ListAPIView):
    serializer_class = DiresaSerializer

    def get_queryset(self):
        if not self.queryset:
            filtro = {}
            cod_ubigeo = self.kwargs.get('cod_ubigeo')
            if re.match(r'^\d{2}$', cod_ubigeo):
                departamento = get_object_or_404(UbigeoDepartamento, cod_ubigeo_inei_departamento=cod_ubigeo)
                filtro = {'departamento': departamento}
            elif re.match(r'^\d{4}$', cod_ubigeo):
                provincia = get_object_or_404(UbigeoProvincia, cod_ubigeo_inei_provincia=cod_ubigeo)
                filtro = {'provincia': provincia}
            elif re.match(r'^\d{6}$', cod_ubigeo):
                distrito = get_object_or_404(UbigeoDistrito, cod_ubigeo_inei_distrito=cod_ubigeo)
                filtro = {'distrito': distrito}
            diresas_id = Establecimiento.objects.values_list('diresa').filter(**filtro).distinct('diresa')
            self.queryset = Diresa.objects.filter(
                id__in=[diresa_id[0] for diresa_id in diresas_id]).exclude(codigo='').order_by('codigo')
        return self.queryset


class UbigeoRedesListAPI(ListAPIView):
    serializer_class = RedSerializer

    def get_queryset(self):
        if not self.queryset:
            filtro = {}
            cod_ubigeo = self.kwargs.get('cod_ubigeo')
            if re.match(r'^\d{2}$', cod_ubigeo):
                departamento = get_object_or_404(UbigeoDepartamento, cod_ubigeo_inei_departamento=cod_ubigeo)
                filtro = {'departamento': departamento}
            elif re.match(r'^\d{4}$', cod_ubigeo):
                provincia = get_object_or_404(UbigeoProvincia, cod_ubigeo_inei_provincia=cod_ubigeo)
                filtro = {'provincia': provincia}
            elif re.match(r'^\d{6}$', cod_ubigeo):
                distrito = get_object_or_404(UbigeoDistrito, cod_ubigeo_inei_distrito=cod_ubigeo)
                filtro = {'distrito': distrito}
            redes_id = Establecimiento.objects.values_list('red').filter(**filtro).distinct('red')
            self.queryset = Red.objects.filter(
                id__in=[red_id[0] for red_id in redes_id]).exclude(codigo='').order_by('codigo')
        return self.queryset


class UbigeoMicroredesListAPI(ListAPIView):
    serializer_class = MicroredSerializer

    def get_queryset(self):
        if not self.queryset:
            filtro = {}
            cod_ubigeo = self.kwargs.get('cod_ubigeo')
            if re.match(r'^\d{2}$', cod_ubigeo):
                departamento = get_object_or_404(UbigeoDepartamento, cod_ubigeo_inei_departamento=cod_ubigeo)
                filtro = {'departamento': departamento}
            elif re.match(r'^\d{4}$', cod_ubigeo):
                provincia = get_object_or_404(UbigeoProvincia, cod_ubigeo_inei_provincia=cod_ubigeo)
                filtro = {'provincia': provincia}
            elif re.match(r'^\d{6}$', cod_ubigeo):
                distrito = get_object_or_404(UbigeoDistrito, cod_ubigeo_inei_distrito=cod_ubigeo)
                filtro = {'distrito': distrito}
            microredes_id = Establecimiento.objects.values_list('microred').filter(**filtro).distinct('microred')
            self.queryset = Microred.objects.filter(
                id__in=[microred_id[0] for microred_id in microredes_id]).exclude(codigo='').order_by('codigo')
        return self.queryset


@method_decorator(cache_page(CACHE_TTL), name='dispatch')
class ListaEstablecimientoPorCategoriaAPI(ListAPIView):
    serializer_class = ListaEstablecimientoSerializer

    def get_queryset(self):
        nombre_categoria = self.kwargs.get('nombre_categoria', None)
        if nombre_categoria:
            categoria = get_object_or_404(EstablecimientoCategoria, nombre_categoria=nombre_categoria)
            establecimientos = Establecimiento.objects.filter(categoria=categoria)
            return establecimientos
        return []


@method_decorator(cache_page(CACHE_TTL), name='dispatch')
class ListaDiresaAPI(ListAPIView):
    serializer_class = DiresaSerializer

    def get_queryset(self):
        es_activo = bool(self.request.query_params.get('es_activo'))
        if es_activo:
            return Diresa.objects.filter(es_activo=True).order_by('nombre')
        return Diresa.objects.all().order_by('nombre')


@method_decorator(cache_page(CACHE_TTL), name='dispatch')
class ListaRedAPI(ListAPIView):
    serializer_class = RedSerializer

    def get_queryset(self):
        diris_activa = bool(self.request.query_params.get('diris_activa'))
        if diris_activa:
            return Red.objects.filter(
                diresa__codigo=self.kwargs.get('diresa_codigo'),
                diresa__es_activo=True).order_by('codigo')
        return Red.objects.filter(diresa__codigo=self.kwargs.get('diresa_codigo')).order_by('codigo')


@method_decorator(cache_page(CACHE_TTL), name='dispatch')
class ListaMicroredAPI(ListAPIView):
    serializer_class = MicroredSerializer

    def get_queryset(self):
        diris_activa = bool(self.request.query_params.get('diris_activa'))
        if diris_activa:
            return Microred.objects.filter(
                diresa__codigo=self.kwargs.get('diresa_codigo'),
                diresa__es_activo=True,
                red__codigo=self.kwargs.get('red_codigo')).order_by('codigo')
        return Microred.objects.filter(
            diresa__codigo=self.kwargs.get('diresa_codigo'),
            red__codigo=self.kwargs.get('red_codigo')).order_by('codigo')


@method_decorator(cache_page(CACHE_TTL), name='dispatch')
class ListaEstablecimientoGrupoAPI(ListAPIView):
    serializer_class = ListaEstablecimientoSerializer

    def get_queryset(self, *args, **kwargs):
        diresa_codigo = self.kwargs.get('diresa_codigo')
        red_codigo = self.kwargs.get('red_codigo')
        microred_codigo = self.kwargs.get('microred_codigo')
        if diresa_codigo and red_codigo and microred_codigo:
            establecimientos = Establecimiento.objects.filter(
                diresa__codigo=diresa_codigo, red__codigo=red_codigo, microred__codigo=microred_codigo)
        elif diresa_codigo and red_codigo:
            establecimientos = Establecimiento.objects.filter(diresa__codigo=diresa_codigo, red__codigo=red_codigo)
        elif diresa_codigo:
            establecimientos = Establecimiento.objects.filter(diresa__codigo=diresa_codigo)
        else:
            return []

        search_param = self.request.GET.get('q')
        if search_param:
            establecimientos = establecimientos.filter(
                Q(codigo_renaes__icontains=search_param) | Q(nombre__icontains=search_param))
        sector_param = self.request.GET.get('sector')
        establecimientos = establecimientos_sector(establecimientos, sector_param)
        return establecimientos


@method_decorator(cache_page(CACHE_TTL), name='dispatch')
class ServicioAPI(RetrieveAPIView):
    serializer_class = ServicioSerializer
    renderer_classes = (JSONRenderer, BrowsableAPIRenderer)
    parser_classes = (JSONParser,)
    metadata_class = SimpleMetadata
    pagination_class = LimitOffsetPagination
    queryset = Servicio.objects.all()
    lookup_field = 'codigo'


@method_decorator(cache_page(CACHE_TTL), name='dispatch')
class DiresaDetalleAPI(RetrieveAPIView):
    serializer_class = DiresaSerializer
    lookup_field = 'diresa_codigo'
    queryset = []

    def get_object(self):
        es_activo = bool(self.request.query_params.get('es_activo'))
        if es_activo:
            return get_object_or_404(
                Diresa, codigo=self.kwargs.get(self.lookup_field), es_activo=True)
        return get_object_or_404(Diresa, codigo=self.kwargs.get(self.lookup_field))


@method_decorator(cache_page(CACHE_TTL), name='dispatch')
class RedDetalleAPI(RetrieveAPIView):
    serializer_class = RedSerializer
    lookup_field = 'red_codigo'
    queryset = []

    def get_object(self):
        diris_activa = bool(self.request.query_params.get('diris_activa'))
        if diris_activa:
            return get_object_or_404(Red,
                                     codigo=self.kwargs.get(self.lookup_field),
                                     diresa__codigo=self.kwargs.get('diresa_codigo'),
                                     diresa__es_activo=True)
        return get_object_or_404(Red,
                                 codigo=self.kwargs.get(self.lookup_field),
                                 diresa__codigo=self.kwargs.get('diresa_codigo'))


@method_decorator(cache_page(CACHE_TTL), name='dispatch')
class MicroredDetalleAPI(RetrieveAPIView):
    serializer_class = MicroredSerializer
    lookup_field = 'microred_codigo'
    queryset = []

    def get_object(self):
        diris_activa = bool(self.request.query_params.get('diris_activa'))
        if diris_activa:
            return get_object_or_404(Microred,
                                     codigo=self.kwargs.get(self.lookup_field),
                                     red__codigo=self.kwargs.get('red_codigo'),
                                     diresa__codigo=self.kwargs.get('diresa_codigo'),
                                     diresa__es_activo=True)
        return get_object_or_404(Microred,
                                 codigo=self.kwargs.get(self.lookup_field),
                                 red__codigo=self.kwargs.get('red_codigo'),
                                 diresa__codigo=self.kwargs.get('diresa_codigo'))
