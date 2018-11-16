from django.contrib import admin

from phr.establecimiento import forms
from phr.establecimiento.models import (
    Diresa, Establecimiento, EstablecimientoCategoria, EstablecimientoSector, Microred, Red,
)


@admin.register(Diresa)
class DiresaAdmin(admin.ModelAdmin):
    ordering = ('nombre',)
    search_fields = ('nombre',)
    list_display = ('nombre', 'codigo', 'departamento', 'es_activo')


@admin.register(Red)
class RedAdmin(admin.ModelAdmin):
    ordering = ('nombre',)
    search_fields = ('nombre',)
    list_display = ('nombre', 'codigo')


@admin.register(Microred)
class MicroredAdmin(admin.ModelAdmin):
    ordering = ('nombre',)
    search_fields = ('nombre',)
    list_display = ('nombre', 'codigo')


@admin.register(Establecimiento)
class EstablecimientoAdmin(admin.ModelAdmin):
    form = forms.LocationForm
    ordering = ('nombre', 'codigo_renaes')
    search_fields = ('nombre', 'codigo_renaes')
    list_display = ('codigo_renaes', 'nombre')
    raw_id_fields = ('continente', 'pais', 'departamento', 'provincia', 'distrito', 'diresa', 'red', 'microred')


@admin.register(EstablecimientoCategoria)
class EstablecimientoCategoriaAdmin(admin.ModelAdmin):
    ordering = ('nombre_categoria',)
    search_field = ('nombre_categoria',)


@admin.register(EstablecimientoSector)
class EstabSectorAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'descripcion')
