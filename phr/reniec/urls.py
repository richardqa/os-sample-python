# coding=utf-8
from django.conf.urls import url

from phr.reniec.views import CrearCiudadanoRN, VerActualizarEliminarCiudadanoRN

urlpatterns = [
    url(r'^cnv/$', CrearCiudadanoRN.as_view()),
    url(r'^cnv/(?P<cui>\d+)/$', VerActualizarEliminarCiudadanoRN.as_view()),
]
