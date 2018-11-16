# coding=utf-8
from django.db.models import Q

from rest_framework.generics import ListAPIView, RetrieveAPIView

from phr.catalogo.api.serializers import (
    DetalleCatalogoAyudaTecnicaSerializer, DetalleCatalogoCIESerializer, DetalleCatalogoDeficienciaSerializer,
    DetalleCatalogoDiscapacidadSerializer, DetalleCatalogoEtniaSerializer, DetalleCatalogoFinanciadorSerializer,
    DetalleCatalogoGradoInstruccionSerializer, DetalleCatalogoProcedimientoSerializer, DetalleCatalogoRazaSerializer,
    ListaCatalogoAyudaTecnicaSerializer, ListaCatalogoCIESerializer, ListaCatalogoDeficienciaSerializer,
    ListaCatalogoDiscapacidadSerializer, ListaCatalogoEtniaSerializer, ListaCatalogoFinanciadorSerializer,
    ListaCatalogoGradoInstruccionSerializer, ListaCatalogoProcedimientoSerializer, ListaCatalogoRazaSerializer,
    MedicamentoAntecedenteSugeridoSerializer, MedicamentoFamiliaAntecedenteSugeridoSerializer,
)
from phr.catalogo.models import (
    CatalogoAyudaTecnica, CatalogoCIE, CatalogoDeficiencia, CatalogoDiscapacidad, CatalogoEtnia, CatalogoFinanciador,
    CatalogoGradoInstruccion, CatalogoProcedimiento, CatalogoRaza, FamiliaMedicamentoAntecedenteSugerido,
    MedicamentoAntecedenteSugerido,
)


class ListaCatalogoCIEAPI(ListAPIView):
    serializer_class = ListaCatalogoCIESerializer

    def get_queryset(self):
        search_param = self.request.GET.get('q', '')
        es_sintoma = self.request.GET.get('es_sintoma', '')
        queryset = CatalogoCIE.objects.all().order_by('id_ciex')
        if es_sintoma:
            queryset = queryset.filter(id_ciex__iregex=r'^R[0-6][0-9]+$').order_by('id_ciex')
        if search_param:
            if len(search_param) >= 3:
                queryset = queryset.filter(
                    Q(id_ciex__icontains=search_param) | Q(desc_ciex__icontains=search_param)).order_by('id_ciex')
        return queryset


class DetalleCatalogoCIEAPI(RetrieveAPIView):
    serializer_class = DetalleCatalogoCIESerializer
    lookup_field = 'id_ciex'
    queryset = CatalogoCIE.objects.filter()


class ListaCatalogoProcedimientoAPI(ListAPIView):
    serializer_class = ListaCatalogoProcedimientoSerializer

    def get_queryset(self):
        search_param = self.request.GET.get('q', '')
        if search_param:
            if len(search_param) >= 3:
                queryset = CatalogoProcedimiento.objects.filter(
                    Q(codigo_cpt__icontains=search_param) |
                    Q(denominacion_procedimiento__icontains=search_param) |
                    Q(nombre_grupo__icontains=search_param) |
                    Q(descripcion_seccion__icontains=search_param) |
                    Q(subdivision_anatomica__icontains=search_param)
                ).order_by('codigo_cpt')
            else:
                queryset = []
        else:
            queryset = CatalogoProcedimiento.objects.all().order_by('codigo_cpt')
        return queryset


class DetalleCatalogoProcedimientoAPI(RetrieveAPIView):
    serializer_class = DetalleCatalogoProcedimientoSerializer
    lookup_field = 'codigo_cpt'
    queryset = CatalogoProcedimiento.objects.filter()


class ListaCatalogoDeficienciaAPI(ListAPIView):
    serializer_class = ListaCatalogoDeficienciaSerializer

    def get_queryset(self):
        nivel = self.request.GET.get('nivel', None)
        search_param = self.request.GET.get('q', '')

        if nivel == '1':
            return CatalogoDeficiencia.objects.filter(Q(categoria_deficiencia__iregex='^[0-9]{1}$') &
                                                      Q(nombre_deficiencia__icontains=search_param))
        if nivel == '2':
            return CatalogoDeficiencia.objects.filter(Q(categoria_deficiencia__iregex='^[0-9]{2}$') &
                                                      Q(nombre_deficiencia__icontains=search_param))
        if nivel == '3':
            return CatalogoDeficiencia.objects.filter(Q(categoria_deficiencia__iregex='^[0-9]{4}$') &
                                                      Q(nombre_deficiencia__icontains=search_param))
        if nivel == '4':
            return CatalogoDeficiencia.objects.filter(Q(categoria_deficiencia__iregex='^[0-9]{5}$') &
                                                      Q(nombre_deficiencia__icontains=search_param))
        if search_param and len(search_param) >= 3:
            return CatalogoDeficiencia.objects.filter(Q(nombre_deficiencia__icontains=search_param))
        return CatalogoDeficiencia.objects.all()


class DetalleCatalogoDeficienciaAPI(RetrieveAPIView):
    serializer_class = DetalleCatalogoDeficienciaSerializer
    lookup_field = 'categoria_deficiencia'
    queryset = CatalogoDeficiencia.objects.filter()


class ListaCatalogoDiscapacidadAPI(ListAPIView):
    serializer_class = ListaCatalogoDiscapacidadSerializer

    queryset = CatalogoDiscapacidad.objects.all()


class DetalleCatalogoDiscapacidadAPI(RetrieveAPIView):
    serializer_class = DetalleCatalogoDiscapacidadSerializer
    lookup_field = 'categoria_discapacidad'
    queryset = CatalogoDiscapacidad.objects.filter()


class ListaCatalogoRazaAPI(ListAPIView):
    serializer_class = ListaCatalogoRazaSerializer

    def get_queryset(self):
        search_param = self.request.GET.get('q', '')
        if search_param:
            if len(search_param) >= 3:
                queryset = CatalogoRaza.objects.filter(descripcion__icontains=search_param)
            else:
                queryset = []
        else:
            queryset = CatalogoRaza.objects.all()
        return queryset


class DetalleCatalogoRazaAPI(RetrieveAPIView):
    serializer_class = DetalleCatalogoRazaSerializer
    queryset = CatalogoRaza.objects.filter()


class ListaCatalogoEtniaAPI(ListAPIView):
    serializer_class = ListaCatalogoEtniaSerializer

    def get_queryset(self):
        search_param = self.request.GET.get('q', '')
        if search_param:
            if len(search_param) >= 3:
                queryset = CatalogoEtnia.objects.filter(Q(descripcion__icontains=search_param) |
                                                        Q(id_etnia=search_param))
            else:
                queryset = []
        else:
            queryset = CatalogoEtnia.objects.all()
        return queryset


class DetalleCatalogoEtniaAPI(RetrieveAPIView):
    serializer_class = DetalleCatalogoEtniaSerializer
    lookup_field = 'id_etnia'
    queryset = CatalogoEtnia.objects.filter()


class ListaCatalogoFinanciadorAPI(ListAPIView):
    serializer_class = ListaCatalogoFinanciadorSerializer

    def get_queryset(self):
        search_param = self.request.GET.get('q', '')
        if search_param:
            if len(search_param) >= 3:
                queryset = CatalogoFinanciador.objects.filter(Q(codigo__icontains=search_param) |
                                                              Q(descripcion__icontains=search_param))
            else:
                queryset = []
        else:
            queryset = CatalogoFinanciador.objects.all()
        return queryset


class DetalleCatalogoFinanciadorAPI(RetrieveAPIView):
    serializer_class = DetalleCatalogoFinanciadorSerializer
    lookup_field = 'codigo'
    queryset = CatalogoFinanciador.objects.filter()


class ListaCatalogoAyudaTecnicaAPI(ListAPIView):
    serializer_class = ListaCatalogoAyudaTecnicaSerializer

    def get_queryset(self):
        search_param = self.request.GET.get('q', '')
        if search_param:
            if len(search_param) >= 3:
                queryset = CatalogoAyudaTecnica.objects.filter(Q(codigo__icontains=search_param) |
                                                               Q(descripcion__icontains=search_param))
            else:
                queryset = []
        else:
            queryset = CatalogoAyudaTecnica.objects.all()
        return queryset


class DetalleCatalogoAyudaTecnicaAPI(RetrieveAPIView):
    serializer_class = DetalleCatalogoAyudaTecnicaSerializer
    lookup_field = 'codigo'
    queryset = CatalogoAyudaTecnica.objects.filter()


class ListaCatalogoGradoInstruccionAPI(ListAPIView):
    serializer_class = ListaCatalogoGradoInstruccionSerializer

    def get_queryset(self):
        search_param = self.request.GET.get('q', '')
        if search_param:
            if len(search_param) >= 3:
                queryset = CatalogoGradoInstruccion.objects.filter(Q(codigo__icontains=search_param) |
                                                                   Q(descripcion__icontains=search_param))
            else:
                queryset = []
        else:
            queryset = CatalogoGradoInstruccion.objects.all()
        return queryset


class DetalleCatalogoGradoInstruccionAPI(RetrieveAPIView):
    serializer_class = DetalleCatalogoGradoInstruccionSerializer
    lookup_field = 'codigo'
    queryset = CatalogoGradoInstruccion.objects.filter()


class MedicamentoFamiliasAntecedenteSugeridoAPIListView(ListAPIView):
    serializer_class = MedicamentoFamiliaAntecedenteSugeridoSerializer

    def get_queryset(self):
        search_param = self.request.GET.get('q')
        if search_param:
            familias = FamiliaMedicamentoAntecedenteSugerido.objects.filter(
                nombre__icontains=search_param).order_by('codigo')
        else:
            familias = FamiliaMedicamentoAntecedenteSugerido.objects.all().order_by('codigo')
        return familias


class MedicamentosAntecedenteSugeridoAPIListView(ListAPIView):
    serializer_class = MedicamentoAntecedenteSugeridoSerializer

    def get_queryset(self):
        search_param = self.request.GET.get('q')
        familia = self.request.GET.get('familia')
        params = {'es_activo': True}
        if search_param:
            params.update({'nombre__icontains': search_param})
        if familia:
            params.update({'familia__codigo': familia})
        medicamentos = MedicamentoAntecedenteSugerido.objects.filter(**params).order_by('codigo')
        return medicamentos
