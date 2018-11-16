from django.contrib import admin

from .forms import PersonalForm
from .models import Personal, TipoPersonal


@admin.register(Personal)
class PersonalAdmin(admin.ModelAdmin):
    form = PersonalForm


@admin.register(TipoPersonal)
class TipoPersonalAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('tipo_personal', )}
