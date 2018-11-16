from django.db.models.query_utils import Q

from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateAPIView

from phr.insteducativa.api.serializers import InstEducativaSerializer
from phr.insteducativa.models import InstitucionEducativa


class InstEducativaListAPIView(ListAPIView):
    serializer_class = InstEducativaSerializer

    def get_queryset(self):
        if not self.queryset:
            search_param = self.request.GET.get('q', [])
            if len(search_param) > 3:
                self.queryset = InstitucionEducativa.objects.filter(
                    Q(nombre__icontains=search_param))
            else:
                self.queryset = InstitucionEducativa.objects.all().order_by('ubigeo', 'nombre')
        return self.queryset


class InstEducativaUbigeoAPIView(ListAPIView):
    serializer_class = InstEducativaSerializer

    def get_queryset(self):
        if not self.queryset:
            ubigeo = self.kwargs.get('ubigeo')
            self.queryset = []
            search_param = self.request.GET.get('q', '')
            filtro = {'ubigeo__startswith': ubigeo}
            if search_param:
                filtro.update({'nombre__icontains': search_param})
            self.queryset = InstitucionEducativa.objects.filter(**filtro).order_by('nombre')
        return self.queryset


class InstEducativaDataAPIView(RetrieveUpdateAPIView):
    serializer_class = InstEducativaSerializer
    lookup_url_kwarg = 'codigo_modular'
    lookup_field = 'codigo_modular'
    queryset = InstitucionEducativa.objects.all()


class InstEducativaCrearAPIView(CreateAPIView):
    serializer_class = InstEducativaSerializer
    queryset = InstitucionEducativa.objects.all()
