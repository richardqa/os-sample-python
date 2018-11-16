# Register your models here.
from django.contrib import admin

from phr.insteducativa.models import InstitucionEducativa


class IntEducativaAdmin(admin.ModelAdmin):
    list_display = ['codigo_colegio', 'codigo_modular', 'nombre', 'tipo', 'nivel']
    search_fields = ['codigo_colegio', 'codigo_modular', 'nombre', 'tipo', 'nivel']

    class Meta:
        model = InstitucionEducativa


admin.site.register(InstitucionEducativa, IntEducativaAdmin)
