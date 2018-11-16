from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from dal import autocomplete
from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.metadata import SimpleMetadata
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.parsers import JSONParser
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer

from phr.ciudadano.models import Ciudadano
from phr.establecimiento.models import Establecimiento
from phr.personal.models import Personal

from .serializers import PersonalSerializer

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


@method_decorator(cache_page(CACHE_TTL), name='dispatch')
class CiudadanoAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return Ciudadano.objects.none()
        qs = Ciudadano.objects.none()
        if self.q:
            if len(self.q) >= 5:
                qs = Ciudadano.objects.filter(
                    Q(nombres__istartswith=self.q) | Q(apellido_paterno=self.q) |
                    Q(apellido_materno=self.q) | Q(numero_documento=self.q)
                )[:20]
        return qs


@method_decorator(cache_page(CACHE_TTL), name='dispatch')
class PersonalView(generics.RetrieveAPIView):
    serializer_class = PersonalSerializer
    renderer_classes = (JSONRenderer, BrowsableAPIRenderer)
    queryset = Personal.objects.all()
    parser_classes = (JSONParser,)
    metadata_class = SimpleMetadata
    pagination_class = LimitOffsetPagination
    lookup_field = 'cmp'


@method_decorator(cache_page(CACHE_TTL), name='dispatch')
class PersonalEstablecimiento(generics.ListAPIView):
    serializer_class = PersonalSerializer
    renderer_classes = (JSONRenderer, BrowsableAPIRenderer)
    parser_classes = (JSONParser,)
    metadata_class = SimpleMetadata
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        establecimiento = get_object_or_404(Establecimiento, codigo_renaes=self.kwargs.get('renaes'))
        self.queryset = establecimiento.personal_set.all()
        return self.queryset


@method_decorator(cache_page(CACHE_TTL), name='dispatch')
class PersonalCiudadanoView(generics.RetrieveUpdateAPIView):
    serializer_class = PersonalSerializer
    renderer_classes = (JSONRenderer, BrowsableAPIRenderer)
    parser_classes = (JSONParser,)

    def get_object(self):
        cmp = self.kwargs.get('cmp')
        dni = self.kwargs.get('dni')
        ciudadano = get_object_or_404(Ciudadano, numero_documento=dni, tipo_documento='01')
        personal, _ = Personal.objects.get_or_create(ciudadano=ciudadano)
        if personal.cmp is None or personal.cmp == '':
            personal.cmp = cmp
            personal.save()
        return personal


@method_decorator(cache_page(CACHE_TTL), name='dispatch')
class CiudadanoPersonalView(generics.RetrieveAPIView):
    serializer_class = PersonalSerializer
    renderer_classes = (JSONRenderer, BrowsableAPIRenderer)
    parser_classes = (JSONParser,)

    def get_object(self):
        ciudadano = get_object_or_404(Ciudadano, numero_documento=self.kwargs.get('dni'))
        personal = get_object_or_404(Personal, ciudadano=ciudadano)
        return personal
