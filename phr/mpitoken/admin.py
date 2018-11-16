from django.contrib import admin

from phr.mpitoken.models import AuthToken


class AuthTokenAdmin(admin.ModelAdmin):
    list_display = ('app_identifier', 'app_name', 'allowed_ips', 'token')
    search_fields = ('app_identifier', 'app_name', 'allowed_ips')

    class Meta:
        model = AuthToken


admin.site.register(AuthToken, AuthTokenAdmin)
