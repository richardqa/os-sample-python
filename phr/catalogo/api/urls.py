# coding=utf-8
from django.conf.urls import include, url

from phr.catalogo.api.views import (
    DetalleCatalogoAyudaTecnicaAPI, DetalleCatalogoCIEAPI, DetalleCatalogoDeficienciaAPI,
    DetalleCatalogoDiscapacidadAPI, DetalleCatalogoEtniaAPI, DetalleCatalogoFinanciadorAPI,
    DetalleCatalogoGradoInstruccionAPI, DetalleCatalogoProcedimientoAPI, DetalleCatalogoRazaAPI,
    ListaCatalogoAyudaTecnicaAPI, ListaCatalogoCIEAPI, ListaCatalogoDeficienciaAPI, ListaCatalogoDiscapacidadAPI,
    ListaCatalogoEtniaAPI, ListaCatalogoFinanciadorAPI, ListaCatalogoGradoInstruccionAPI, ListaCatalogoProcedimientoAPI,
    ListaCatalogoRazaAPI, MedicamentoFamiliasAntecedenteSugeridoAPIListView, MedicamentosAntecedenteSugeridoAPIListView,
)

urlpatterns = [
    url(r'^v1/', include([
        url(r'^catalogo/', include([
            url(r'^cie/lista/$', ListaCatalogoCIEAPI.as_view()),
            url(r'^cie/detalle/(?P<id_ciex>\w+)/$', DetalleCatalogoCIEAPI.as_view()),
            url(r'^procedimiento/lista/$', ListaCatalogoProcedimientoAPI.as_view()),
            url(r'^procedimiento/detalle/(?P<codigo_cpt>[\w.]+)/$', DetalleCatalogoProcedimientoAPI.as_view()),
            url(r'^deficiencia/lista/$', ListaCatalogoDeficienciaAPI.as_view()),
            url(r'^deficiencia/detalle/(?P<categoria_deficiencia>[a-zA-Z0-9.]+)/$',
                DetalleCatalogoDeficienciaAPI.as_view()),
            url(r'^discapacidad/lista/$', ListaCatalogoDiscapacidadAPI.as_view()),
            url(r'^discapacidad/detalle/(?P<categoria_discapacidad>\w+)/$',
                DetalleCatalogoDiscapacidadAPI.as_view()),
            url(r'^raza/lista/$', ListaCatalogoRazaAPI.as_view()),
            url(r'^raza/detalle/(?P<pk>\d+)/$', DetalleCatalogoRazaAPI.as_view()),
            url(r'^etnia/lista/$', ListaCatalogoEtniaAPI.as_view()),
            url(r'^etnia/detalle/(?P<id_etnia>\w+)/$', DetalleCatalogoEtniaAPI.as_view()),
            url(r'^financiador/lista/$', ListaCatalogoFinanciadorAPI.as_view()),
            url(r'^financiador/detalle/(?P<codigo>\w+)/$', DetalleCatalogoFinanciadorAPI.as_view()),
            url(r'^ayudatecnica/lista/$', ListaCatalogoAyudaTecnicaAPI.as_view()),
            url(r'^ayudatecnica/detalle/(?P<codigo>\w+)/$', DetalleCatalogoAyudaTecnicaAPI.as_view()),
            url(r'^gradoinstruccion/lista/$', ListaCatalogoGradoInstruccionAPI.as_view()),
            url(r'^gradoinstruccion/detalle/(?P<codigo>\w+)/$', DetalleCatalogoGradoInstruccionAPI.as_view()),
            # Medicamentos para antecedentes sugeridos de medicación habitual
            url(r'^familiamedicamentos/$', MedicamentoFamiliasAntecedenteSugeridoAPIListView.as_view()),
            url(r'^medicamentos/$', MedicamentosAntecedenteSugeridoAPIListView.as_view()),
        ], namespace='catalogo')),
    ], namespace='v1')),

]
