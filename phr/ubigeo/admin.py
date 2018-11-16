from django.contrib import admin

from phr.ubigeo.models import (
    UbigeoContinente, UbigeoDepartamento, UbigeoDistrito, UbigeoLocalidad, UbigeoPais, UbigeoProvincia,
)


@admin.register(UbigeoContinente)
class UbigeoContinenteAdmin(admin.ModelAdmin):
    ordering = ['ubigeo_continente']
    search_fields = ['ubigeo_continente']
    pass


@admin.register(UbigeoPais)
class UbigeoPaisAdmin(admin.ModelAdmin):
    ordering = ['ubigeo_pais']
    search_fields = ['ubigeo_pais']
    pass


@admin.register(UbigeoDepartamento)
class UbigeoDepartamentoAdmin(admin.ModelAdmin):
    ordering = ['ubigeo_departamento']
    search_fields = ['ubigeo_departamento']
    pass


@admin.register(UbigeoProvincia)
class UbigeoProvinciaAdmin(admin.ModelAdmin):
    ordering = ['ubigeo_provincia']
    search_fields = ['ubigeo_provincia']
    pass


@admin.register(UbigeoDistrito)
class UbigeoDistritoAdmin(admin.ModelAdmin):
    ordering = ['ubigeo_distrito']
    search_fields = ['ubigeo_distrito']
    pass


@admin.register(UbigeoLocalidad)
class UbigeoLocalidadAdmin(admin.ModelAdmin):
    ordering = ['ubigeo_localidad']
    search_fields = ['ubigeo_localidad']
    pass
