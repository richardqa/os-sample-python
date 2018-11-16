# coding=utf-8
from django.conf.urls import include, url

from phr.ubigeo.api.views import (
    DetalleUbigeoContinenteAPI, DetalleUbigeoDepartamentoAPI, DetalleUbigeoDistritoAPI, DetalleUbigeoLocalidadAPI,
    DetalleUbigeoPaisAPI, DetalleUbigeoProvinciaAPI, ListaUbigeoContinenteAPI, ListaUbigeoDepartamentoAPI,
    ListaUbigeoDistritoAPI, ListaUbigeoLocalidadAPI, ListaUbigeoPaisAPI, ListaUbigeoProvinciaAPI,
)

urlpatterns = [
    url(r'^v1/', include([
        url(r'^ubigeo/', include([
            url(r'^$', ListaUbigeoContinenteAPI.as_view()),
            url(r'^(?P<cod_continente>\w{1,2})/$', ListaUbigeoPaisAPI.as_view()),
            url(r'^(?P<cod_continente>\w{1,2})/(?P<cod_pais>\w{1,3})/$', ListaUbigeoDepartamentoAPI.as_view()),
            url(r'^(?P<cod_continente>\w{1,2})/(?P<cod_pais>\w{1,3})/(?P<cod_departamento>\w{2})/$',
                ListaUbigeoProvinciaAPI.as_view()),
            url(r'^(?P<cod_continente>\w{1,2})/(?P<cod_pais>\w{1,3})/'
                r'(?P<cod_departamento>\w{2})/(?P<cod_provincia>\d{4})/$', ListaUbigeoDistritoAPI.as_view()),
            url(r'^(?P<cod_continente>\w{1,2})/(?P<cod_pais>\w{1,3})/'
                r'(?P<cod_departamento>\w{2})/(?P<cod_provincia>\d{4})/(?P<cod_distrito>\d{6})/$',
                ListaUbigeoLocalidadAPI.as_view()),
        ], namespace='ubigeo')),
        url(r'^ubigeo/detalle/', include([
            url(r'^(?P<cod_continente>\w{1,2})/$', DetalleUbigeoContinenteAPI.as_view()),
            url(r'^(?P<cod_continente>\w{1,2})/(?P<cod_pais>\w{1,3})/$', DetalleUbigeoPaisAPI.as_view()),
            url(r'^(?P<cod_continente>\w{1,2})/(?P<cod_pais>\w{1,3})/(?P<cod_departamento>\w{2})/$',
                DetalleUbigeoDepartamentoAPI.as_view()),
            url(r'^(?P<cod_continente>\w{1,2})/(?P<cod_pais>\w{1,3})/'
                r'(?P<cod_departamento>\w{2})/(?P<cod_provincia>\d{4})/$', DetalleUbigeoProvinciaAPI.as_view()),
            url(r'^(?P<cod_continente>\w{1,2})/(?P<cod_pais>\w{1,3})/'
                r'(?P<cod_departamento>\w{2})/(?P<cod_provincia>\d{4})/(?P<cod_distrito>\d{6})/$',
                DetalleUbigeoDistritoAPI.as_view()),
            url(r'^(?P<cod_continente>\w{1,2})/(?P<cod_pais>\w{1,3})/(?P<cod_departamento>\w{2})/'
                r'(?P<cod_provincia>\d{4})/(?P<cod_distrito>\d{6})/(?P<cod_localidad>\d{9})/$',
                DetalleUbigeoLocalidadAPI.as_view()),
        ], namespace='ubigeo-detalle')),
    ], namespace='v1')),
]
