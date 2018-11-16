# coding=utf-8
from django.conf.urls import include, url

from phr.establecimiento.api.views import (
    DetalleEstablecimientoAPIView, DiresaDetalleAPI, ListaDiresaAPI, ListaEstablecimientoAPI,
    ListaEstablecimientoGrupoAPI, ListaEstablecimientoPorCategoriaAPI, ListaEstablecimientosCercanosAPI,
    ListaEstablecimientosPorSectorAPI, ListaEstablecimientosSectoresAPI, ListaEstablecimientoUbigeoAPI,
    ListaMicroredAPI, ListaRedAPI, MicroredDetalleAPI, RedDetalleAPI, SectorDetalleAPI, SectorRetrieveAPIView,
    ServicioAPI, UbigeoDiresaListAPI, UbigeoMicroredesListAPI, UbigeoRedesListAPI,
)

urlpatterns = [
    url(r'^v1/', include([

        url(r'^establecimiento/', include([
            url(r'^(?P<cod_renaes>[-\w]+)/detalle/$', DetalleEstablecimientoAPIView.as_view()),
            url(r'^(?P<cod_renaes>[-\w]+)/$', DetalleEstablecimientoAPIView.as_view()),
        ], namespace='establecimiento')),

        url(r'^establecimientos/', include([
            url(r'^$', ListaEstablecimientoAPI.as_view()),
            url(r'^sectores/$', ListaEstablecimientosSectoresAPI.as_view()),
            url(r'^sectores/(?P<codigo>\d+)/$', SectorRetrieveAPIView.as_view()),
            url(r'^sector/(?P<pk>\d+)/$', ListaEstablecimientosPorSectorAPI.as_view()),
            url(r'^sector/detalle/(?P<pk>\d+)/$', SectorDetalleAPI.as_view()),
            url(r'^cercanos/$', ListaEstablecimientosCercanosAPI.as_view()),
            url(r'^ubigeo/(?P<cod_ubigeo>\w{2,6})/$', ListaEstablecimientoUbigeoAPI.as_view()),
            url(r'^diresa/(?P<diresa_codigo>\w{1,6})/$',
                ListaEstablecimientoGrupoAPI.as_view()),
            url(r'^diresa/(?P<diresa_codigo>\w{1,6})/red/(?P<red_codigo>\d+)/$',
                ListaEstablecimientoGrupoAPI.as_view()),
            url(r'^diresa/(?P<diresa_codigo>\w{1,6})/red/(?P<red_codigo>\d+)/microred/(?P<microred_codigo>\d+)/$',
                ListaEstablecimientoGrupoAPI.as_view()),
            url(r'^categoria/(?P<nombre_categoria>[\w-]+)/$',
                ListaEstablecimientoPorCategoriaAPI.as_view()),
        ], namespace='establecimientos')),

        url(r'^diresa/', include([
            url(r'^$', ListaDiresaAPI.as_view()),
            url(r'^(?P<diresa_codigo>\d+)/$', DiresaDetalleAPI.as_view()),
            url(r'^(?P<diresa_codigo>\d+)/red/$', ListaRedAPI.as_view()),
            url(r'^(?P<diresa_codigo>\d+)/red/(?P<red_codigo>\d+)/$', RedDetalleAPI.as_view()),
            url(r'^(?P<diresa_codigo>\d+)/red/(?P<red_codigo>\d+)/microred/$', ListaMicroredAPI.as_view()),
            url(r'^(?P<diresa_codigo>\d+)/red/(?P<red_codigo>\d+)/microred/(?P<microred_codigo>\d+)/$',
                MicroredDetalleAPI.as_view()),
        ], namespace='diresa')),

        url(r'^ubigeo/', include([
            url(r'^(?P<cod_ubigeo>\d{2,6})/diresas/$', UbigeoDiresaListAPI.as_view()),
            url(r'^(?P<cod_ubigeo>\d{2,6})/redes/$', UbigeoRedesListAPI.as_view()),
            url(r'^(?P<cod_ubigeo>\d{2,6})/microredes/$', UbigeoMicroredesListAPI.as_view()),
        ], namespace='ubigeo-diresa')),

        url(r'^servicio/', include([
            url(r'^(?P<codigo>\d+)/$', ServicioAPI.as_view()),
        ], namespace='establecimiento-servicio')),

    ], namespace='v1')),
]
