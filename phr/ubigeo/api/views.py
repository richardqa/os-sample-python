# coding=utf-8
from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from phr.common.drf_custom import LargeResultsSetPagination
from phr.ubigeo.api.serializers import (
    DetalleUbigeoContinenteSerializer, DetalleUbigeoDepartamentoSerializer, DetalleUbigeoDistritoSerializer,
    DetalleUbigeoLocalidadSerializer, DetalleUbigeoPaisSerializer, DetalleUbigeoProvinciaSerializer,
    ListaUbigeoContienteSerializer, ListaUbigeoDepartamentoSerializer, ListaUbigeoDistritoSerializer,
    ListaUbigeoLocalidadSerializer, ListaUbigeoPaisSerializer, ListaUbigeoProvinciaSerializer,
)
from phr.ubigeo.models import (
    UbigeoContinente, UbigeoDepartamento, UbigeoDistrito, UbigeoLocalidad, UbigeoPais, UbigeoProvincia,
)


class ListaUbigeoContinenteAPI(ListAPIView):
    serializer_class = ListaUbigeoContienteSerializer
    pagination_class = LargeResultsSetPagination

    def get_queryset(self):
        if self.request.GET.get('provider', 'inei').lower() == 'inei':
            return self.provider_inei()
        else:
            return self.provider_reniec()

    def provider_inei(self):
        return UbigeoContinente.objects.all()

    def provider_reniec(self):
        return UbigeoContinente.objects.all()


class ListaUbigeoPaisAPI(ListAPIView):
    serializer_class = ListaUbigeoPaisSerializer
    pagination_class = LargeResultsSetPagination

    def get_queryset(self):
        if self.request.GET.get('provider', 'inei').lower() == 'inei':
            return self.provider_inei()
        else:
            return self.provider_reniec()

    def provider_inei(self):
        continente = get_object_or_404(UbigeoContinente,
                                       cod_ubigeo_inei_continente=self.kwargs.get('cod_continente', ''))
        return UbigeoPais.objects.filter(continente=continente).order_by('ubigeo_pais')

    def provider_reniec(self):
        continente = get_object_or_404(UbigeoContinente,
                                       cod_ubigeo_reniec_continente=self.kwargs.get('cod_continente', ''))
        return UbigeoPais.objects.filter(continente=continente).order_by('ubigeo_pais')


class ListaUbigeoDepartamentoAPI(ListAPIView):
    serializer_class = ListaUbigeoDepartamentoSerializer
    pagination_class = LargeResultsSetPagination

    def get_queryset(self):
        if self.request.GET.get('provider', 'inei').lower() == 'inei':
            return self.provider_inei()
        else:
            return self.provider_reniec()

    def provider_inei(self):
        continente = get_object_or_404(UbigeoContinente,
                                       cod_ubigeo_inei_continente=self.kwargs.get('cod_continente', ''))
        pais = get_object_or_404(UbigeoPais, cod_ubigeo_inei_pais=self.kwargs.get('cod_pais', ''),
                                 continente=continente)
        return UbigeoDepartamento.objects.filter(continente=continente, pais=pais).order_by(
            'cod_ubigeo_inei_departamento')

    def provider_reniec(self):
        continente = get_object_or_404(UbigeoContinente,
                                       cod_ubigeo_reniec_continente=self.kwargs.get('cod_continente', ''))
        pais = get_object_or_404(UbigeoPais, cod_ubigeo_reniec_pais=self.kwargs.get('cod_pais', ''),
                                 continente=continente)
        return UbigeoDepartamento.objects.filter(continente=continente, pais=pais).order_by(
            'cod_ubigeo_reniec_departamento')


class ListaUbigeoProvinciaAPI(ListAPIView):
    serializer_class = ListaUbigeoProvinciaSerializer
    pagination_class = LargeResultsSetPagination

    def get_queryset(self):
        if self.request.GET.get('provider', 'inei').lower() == 'inei':
            return self.provider_inei()
        else:
            return self.provider_reniec()

    def provider_inei(self):
        continente = get_object_or_404(UbigeoContinente,
                                       cod_ubigeo_inei_continente=self.kwargs.get('cod_continente', ''))
        pais = get_object_or_404(UbigeoPais, cod_ubigeo_inei_pais=self.kwargs.get('cod_pais', ''),
                                 continente=continente)
        departamento = get_object_or_404(UbigeoDepartamento,
                                         cod_ubigeo_inei_departamento=self.kwargs.get('cod_departamento', ''),
                                         continente=continente, pais=pais)
        return UbigeoProvincia.objects.filter(continente=continente, pais=pais, departamento=departamento).order_by(
            'cod_ubigeo_inei_provincia')

    def provider_reniec(self):
        continente = get_object_or_404(UbigeoContinente,
                                       cod_ubigeo_reniec_continente=self.kwargs.get('cod_continente', ''))
        pais = get_object_or_404(UbigeoPais, cod_ubigeo_reniec_pais=self.kwargs.get('cod_pais', ''),
                                 continente=continente)
        departamento = get_object_or_404(UbigeoDepartamento,
                                         cod_ubigeo_reniec_departamento=self.kwargs.get('cod_departamento', ''),
                                         continente=continente, pais=pais)
        return UbigeoProvincia.objects.filter(continente=continente, pais=pais, departamento=departamento).order_by(
            'cod_ubigeo_reniec_provincia')


class ListaUbigeoDistritoAPI(ListAPIView):
    serializer_class = ListaUbigeoDistritoSerializer
    pagination_class = LargeResultsSetPagination

    def get_queryset(self):
        if self.request.GET.get('provider', 'inei').lower() == 'inei':
            return self.provider_inei()
        else:
            return self.provider_reniec()

    def provider_inei(self):
        continente = get_object_or_404(UbigeoContinente,
                                       cod_ubigeo_inei_continente=self.kwargs.get('cod_continente', ''))
        pais = get_object_or_404(UbigeoPais, cod_ubigeo_inei_pais=self.kwargs.get('cod_pais', ''),
                                 continente=continente)
        departamento = get_object_or_404(UbigeoDepartamento,
                                         cod_ubigeo_inei_departamento=self.kwargs.get('cod_departamento', ''),
                                         continente=continente, pais=pais)
        provincia = get_object_or_404(UbigeoProvincia,
                                      cod_ubigeo_inei_provincia=self.kwargs.get('cod_provincia', ''),
                                      continente=continente, pais=pais, departamento=departamento)

        return UbigeoDistrito.objects.filter(continente=continente, pais=pais, departamento=departamento,
                                             provincia=provincia).order_by('cod_ubigeo_inei_distrito')

    def provider_reniec(self):
        continente = get_object_or_404(UbigeoContinente,
                                       cod_ubigeo_reniec_continente=self.kwargs.get('cod_continente', ''))
        pais = get_object_or_404(UbigeoPais, cod_ubigeo_reniec_pais=self.kwargs.get('cod_pais', ''),
                                 continente=continente)
        departamento = get_object_or_404(UbigeoDepartamento,
                                         cod_ubigeo_reniec_departamento=self.kwargs.get('cod_departamento', ''),
                                         continente=continente, pais=pais)
        provincia = get_object_or_404(UbigeoProvincia,
                                      cod_ubigeo_reniec_provincia=self.kwargs.get('cod_provincia', ''),
                                      continente=continente, pais=pais, departamento=departamento)

        return UbigeoDistrito.objects.filter(continente=continente, pais=pais, departamento=departamento,
                                             provincia=provincia).order_by('cod_ubigeo_reniec_distrito')


class ListaUbigeoLocalidadAPI(ListAPIView):
    serializer_class = ListaUbigeoLocalidadSerializer
    pagination_class = LargeResultsSetPagination

    def get_queryset(self):
        if self.request.GET.get('provider', 'inei').lower() == 'inei':
            return self.provider_inei()
        else:
            return self.provider_reniec()

    def provider_inei(self):
        continente = get_object_or_404(UbigeoContinente,
                                       cod_ubigeo_inei_continente=self.kwargs.get('cod_continente', ''))
        pais = get_object_or_404(UbigeoPais, cod_ubigeo_inei_pais=self.kwargs.get('cod_pais', ''),
                                 continente=continente)
        departamento = get_object_or_404(UbigeoDepartamento,
                                         cod_ubigeo_inei_departamento=self.kwargs.get('cod_departamento', ''),
                                         continente=continente, pais=pais)
        provincia = get_object_or_404(UbigeoProvincia,
                                      cod_ubigeo_inei_provincia=self.kwargs.get('cod_provincia', ''),
                                      continente=continente, pais=pais, departamento=departamento)
        distrito = get_object_or_404(UbigeoDistrito,
                                     cod_ubigeo_inei_distrito=self.kwargs.get('cod_distrito', ''),
                                     provincia=provincia, continente=continente, pais=pais, departamento=departamento)

        return UbigeoLocalidad.objects.filter(
            continente=continente, pais=pais, departamento=departamento, provincia=provincia,
            distrito=distrito).order_by('cod_ubigeo_inei_localidad')

    def provider_reniec(self):
        continente = get_object_or_404(UbigeoContinente,
                                       cod_ubigeo_reniec_continente=self.kwargs.get('cod_continente', ''))
        pais = get_object_or_404(UbigeoPais, cod_ubigeo_reniec_pais=self.kwargs.get('cod_pais', ''),
                                 continente=continente)
        departamento = get_object_or_404(UbigeoDepartamento,
                                         cod_ubigeo_reniec_departamento=self.kwargs.get('cod_departamento', ''),
                                         continente=continente, pais=pais)
        provincia = get_object_or_404(UbigeoProvincia,
                                      cod_ubigeo_reniec_provincia=self.kwargs.get('cod_provincia', ''),
                                      continente=continente, pais=pais, departamento=departamento)
        distrito = get_object_or_404(UbigeoDistrito,
                                     cod_ubigeo_reniec_distrito=self.kwargs.get('cod_distrito', ''),
                                     provincia=provincia, continente=continente, pais=pais, departamento=departamento)

        return UbigeoLocalidad.objects.filter(
            continente=continente, pais=pais, departamento=departamento, provincia=provincia,
            distrito=distrito).order_by('cod_ubigeo_reniec_localidad', 'cod_ubigeo_reniec_localidad')


# -- Detalles
class DetalleUbigeoContinenteAPI(APIView):
    def get(self, request, format=None, **kwargs):
        if self.request.GET.get('provider', 'inei').lower() == 'inei':
            return self.provider_inei()
        else:
            return self.provider_reniec()

    def provider_inei(self):
        obj = UbigeoContinente.objects.get(
            cod_ubigeo_inei_continente=self.kwargs.get('cod_continente'))
        serializer = DetalleUbigeoContinenteSerializer(obj, many=False)
        return Response(serializer.data)

    def provider_reniec(self):
        obj = UbigeoContinente.objects.get(
            cod_ubigeo_reniec_continente=self.kwargs.get('cod_continente'))
        serializer = DetalleUbigeoContinenteSerializer(obj, many=False)
        return Response(serializer.data)


class DetalleUbigeoPaisAPI(APIView):
    def get(self, request, format=None, **kwargs):
        if self.request.GET.get('provider', 'inei').lower() == 'inei':
            return self.provider_inei()
        else:
            return self.provider_reniec()

    def provider_inei(self):
        obj = UbigeoPais.objects.get(
            continente__cod_ubigeo_inei_continente=self.kwargs.get('cod_continente'),
            cod_ubigeo_inei_pais=self.kwargs.get('cod_pais'))
        serializer = DetalleUbigeoPaisSerializer(obj, many=False)
        return Response(serializer.data)

    def provider_reniec(self):
        obj = UbigeoPais.objects.get(
            continente__cod_ubigeo_reniec_continente=self.kwargs.get('cod_continente'),
            cod_ubigeo_reniec_pais=self.kwargs.get('cod_pais'))
        serializer = DetalleUbigeoPaisSerializer(obj, many=False)
        return Response(serializer.data)


class DetalleUbigeoDepartamentoAPI(APIView):
    def get(self, request, format=None, **kwargs):
        if self.request.GET.get('provider', 'inei').lower() == 'inei':
            return self.provider_inei()
        else:
            return self.provider_reniec()

    def provider_inei(self):
        departamento = UbigeoDepartamento.objects.get(
            continente__cod_ubigeo_inei_continente=self.kwargs.get('cod_continente'),
            pais__cod_ubigeo_inei_pais=self.kwargs.get('cod_pais'),
            cod_ubigeo_inei_departamento=self.kwargs.get('cod_departamento'))
        serializer = DetalleUbigeoDepartamentoSerializer(departamento, many=False)
        return Response(serializer.data)

    def provider_reniec(self):
        departamento = UbigeoDepartamento.objects.get(
            continente__cod_ubigeo_reniec_continente=self.kwargs.get('cod_continente'),
            pais__cod_ubigeo_reniec_pais=self.kwargs.get('cod_pais'),
            cod_ubigeo_reniec_departamento=self.kwargs.get('cod_departamento'))
        serializer = DetalleUbigeoDepartamentoSerializer(departamento, many=False)
        return Response(serializer.data)


class DetalleUbigeoProvinciaAPI(APIView):
    def get(self, request, format=None, **kwargs):
        if self.request.GET.get('provider', 'inei').lower() == 'inei':
            return self.provider_inei()
        else:
            return self.provider_reniec()

    def provider_inei(self):
        obj = UbigeoProvincia.objects.get(
            continente__cod_ubigeo_inei_continente=self.kwargs.get('cod_continente'),
            pais__cod_ubigeo_inei_pais=self.kwargs.get('cod_pais'),
            departamento__cod_ubigeo_inei_departamento=self.kwargs.get('cod_departamento'),
            cod_ubigeo_inei_provincia=self.kwargs.get('cod_provincia'))
        serializer = DetalleUbigeoProvinciaSerializer(obj, many=False)
        return Response(serializer.data)

    def provider_reniec(self):
        obj = UbigeoProvincia.objects.get(
            continente__cod_ubigeo_reniec_continente=self.kwargs.get('cod_continente'),
            pais__cod_ubigeo_reniec_pais=self.kwargs.get('cod_pais'),
            departamento__cod_ubigeo_reniec_departamento=self.kwargs.get('cod_departamento'),
            cod_ubigeo_reniec_provincia=self.kwargs.get('cod_provincia'))
        serializer = DetalleUbigeoProvinciaSerializer(obj, many=False)
        return Response(serializer.data)


class DetalleUbigeoDistritoAPI(APIView):
    def get(self, request, format=None, **kwargs):
        if self.request.GET.get('provider', 'inei').lower() == 'inei':
            return self.provider_inei()
        else:
            return self.provider_reniec()

    def provider_inei(self):
        obj = UbigeoDistrito.objects.get(
            continente__cod_ubigeo_inei_continente=self.kwargs.get('cod_continente'),
            pais__cod_ubigeo_inei_pais=self.kwargs.get('cod_pais'),
            departamento__cod_ubigeo_inei_departamento=self.kwargs.get('cod_departamento'),
            provincia__cod_ubigeo_inei_provincia=self.kwargs.get('cod_provincia'),
            cod_ubigeo_inei_distrito=self.kwargs.get('cod_distrito'))
        serializer = DetalleUbigeoDistritoSerializer(obj, many=False)
        return Response(serializer.data)

    def provider_reniec(self):
        obj = UbigeoDistrito.objects.get(
            continente__cod_ubigeo_reniec_continente=self.kwargs.get('cod_continente'),
            pais__cod_ubigeo_reniec_pais=self.kwargs.get('cod_pais'),
            departamento__cod_ubigeo_reniec_departamento=self.kwargs.get('cod_departamento'),
            provincia__cod_ubigeo_reniec_provincia=self.kwargs.get('cod_provincia'),
            cod_ubigeo_reniec_distrito=self.kwargs.get('cod_distrito'))
        serializer = DetalleUbigeoDistritoSerializer(obj, many=False)
        return Response(serializer.data)


class DetalleUbigeoLocalidadAPI(APIView):
    def get(self, request, format=None, **kwargs):
        if self.request.GET.get('provider', 'inei').lower() == 'inei':
            return self.provider_inei()
        else:
            return self.provider_reniec()

    def provider_inei(self):
        obj = UbigeoLocalidad.objects.get(
            continente__cod_ubigeo_inei_continente=self.kwargs.get('cod_continente'),
            pais__cod_ubigeo_inei_pais=self.kwargs.get('cod_pais'),
            departamento__cod_ubigeo_inei_departamento=self.kwargs.get('cod_departamento'),
            provincia__cod_ubigeo_inei_provincia=self.kwargs.get('cod_provincia'),
            distrito__cod_ubigeo_inei_distrito=self.kwargs.get('cod_distrito'),
            cod_ubigeo_inei_localidad=self.kwargs.get('cod_localidad'))
        serializer = DetalleUbigeoLocalidadSerializer(obj, many=False)
        return Response(serializer.data)

    def provider_reniec(self):
        obj = UbigeoLocalidad.objects.get(
            continente__cod_ubigeo_reniec_continente=self.kwargs.get('cod_continente'),
            pais__cod_ubigeo_reniec_pais=self.kwargs.get('cod_pais'),
            departamento__cod_ubigeo_reniec_departamento=self.kwargs.get('cod_departamento'),
            provincia__cod_ubigeo_reniec_provincia=self.kwargs.get('cod_provincia'),
            cod_ubigeo_reniec_distrito=self.kwargs.get('cod_distrito'),
            cod_ubigeo_reniec_localidad=self.kwargs.get('cod_localidad'))
        serializer = DetalleUbigeoLocalidadSerializer(obj, many=False)
        return Response(serializer.data)
