from django.contrib import admin, messages

from phr.common.models import ConfiguracionConexionInternet


class ConexionInternetAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'con_conexion', 'ping_time')

    class Meta:
        model = ConfiguracionConexionInternet

    def save_model(self, request, obj, form, change):
        if ConfiguracionConexionInternet.objects.exclude(id=obj.id).exists():
            messages.error(request, "Ya existe una configuración previa, no puede agregar una nueva.")
            return None
        super().save_model(request, obj, form, change)


admin.site.register(ConfiguracionConexionInternet, ConexionInternetAdmin)
