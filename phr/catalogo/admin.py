# coding=utf-8
from django.contrib import admin

from import_export import resources
from import_export.admin import ImportExportModelAdmin

from phr.catalogo.models import (
    CatalogoAyudaTecnica, CatalogoCIE, CatalogoDeficiencia, CatalogoDiscapacidad, CatalogoEtnia, CatalogoFinanciador,
    CatalogoGradoInstruccion, CatalogoProcedimiento, CatalogoRaza, FamiliaMedicamentoAntecedenteSugerido,
    MedicamentoAntecedenteSugerido,
)


@admin.register(CatalogoCIE)
class CatalogCIEAdmin(admin.ModelAdmin):
    list_display = ['id_ciex', 'desc_ciex']


class DeficienciaResource(resources.ModelResource):
    class Meta:
        model = CatalogoDeficiencia


@admin.register(CatalogoDeficiencia)
class CatalogoDeficienciaAdmin(ImportExportModelAdmin):
    resource_class = DeficienciaResource
    list_display = ['categoria_deficiencia', 'nombre_deficiencia']


@admin.register(CatalogoDiscapacidad)
class CatalogDiscapacidadAdmin(admin.ModelAdmin):
    pass


class CatalogoRazaResource(resources.ModelResource):
    class Meta:
        model = CatalogoRaza


@admin.register(CatalogoRaza)
class CatalogRazaAdmin(ImportExportModelAdmin):
    resource_class = CatalogoRazaResource


class CatalogoEtniaResource(resources.ModelResource):
    class Meta:
        model = CatalogoEtnia


@admin.register(CatalogoEtnia)
class CatalogEtniaAdmin(ImportExportModelAdmin):
    resource_class = CatalogoEtniaResource


class FinanciadorResource(resources.ModelResource):
    class Meta:
        model = CatalogoFinanciador


@admin.register(CatalogoFinanciador)
class CatalogFinancierAdmin(ImportExportModelAdmin):
    resource_class = FinanciadorResource


class ProcedimientoResource(resources.ModelResource):
    class Meta:
        model = CatalogoProcedimiento


@admin.register(CatalogoProcedimiento)
class CatalogProcedureAdmin(ImportExportModelAdmin):
    resource_class = ProcedimientoResource


class AyudaTecnicaResource(resources.ModelResource):
    class Meta:
        model = CatalogoAyudaTecnica
        fields = ['id', 'codigo', 'descripcion']


@admin.register(CatalogoAyudaTecnica)
class CatalogoAyudaTecnicaAdmin(ImportExportModelAdmin):
    resource_class = AyudaTecnicaResource


class GradoInstruccionResource(resources.ModelResource):
    class Meta:
        model = CatalogoGradoInstruccion
        fields = ['codigo', 'descripcion']
        exclude = ['id']


@admin.register(CatalogoGradoInstruccion)
class CatalogoGradoInstruccionAdmin(ImportExportModelAdmin):
    resources = GradoInstruccionResource


@admin.register(MedicamentoAntecedenteSugerido)
class MedicamentoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre', 'familia', 'es_activo')
    search_fields = ('codigo', 'nombre')

    class Meta:
        model = MedicamentoAntecedenteSugerido


@admin.register(FamiliaMedicamentoAntecedenteSugerido)
class MedicamentoFamiliaAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre',)
    search_fields = ('codigo', 'nombre',)

    class Meta:
        model = FamiliaMedicamentoAntecedenteSugerido
