# coding=utf-8
from django.contrib import admin

from import_export import resources
from import_export.admin import ImportExportModelAdmin

from phr.ciudadano.models import Ciudadano, CiudadanoParentesco, CiudadanoRN


class CuidadanoResource(resources.ModelResource):
    class Meta:
        model = Ciudadano
        fields = ('nombres', 'apellido_paterno', 'apellido_materno', 'tipo_documento', 'tipo_documento_minsa',
                  'numero_documento', 'correo', 'telefono', 'celular', 'domicilio_direccion', 'domicilio_referencia',
                  'nacimiento_ubigeo', 'sexo', 'estado_civil', 'etnia', 'lengua', 'tipo_seguro', 'estado',
                  'continente_domicilio', 'departamento_domicilio', 'departamento_nacimiento', 'distrito_domicilio',
                  'distrito_nacimiento', 'localidad_domicilio', 'pais_domicilio', 'provincia_domicilio',
                  'provincia_nacimiento', 'fecha_nacimiento', 'cui', 'grado_instruccion', 'ocupacion')


@admin.register(Ciudadano)
class CuidadanoAdmin(ImportExportModelAdmin):
    resources = CuidadanoResource
    search_fields = ('numero_documento',)
    list_display = ('numero_documento', 'cui', 'tipo_documento', 'apellido_paterno', 'apellido_materno', 'nombres',
                    'sexo', 'fecha_nacimiento', 'estado_civil', 'origen_datos', 'es_removido', 'fecha_modificacion',)
    raw_id_fields = (
        'continente_domicilio', 'pais_domicilio', 'departamento_domicilio', 'provincia_domicilio', 'distrito_domicilio',
        'localidad_domicilio', 'pais_domicilio_actual', 'departamento_domicilio_actual', 'provincia_domicilio_actual',
        'distrito_domicilio_actual', 'localidad_domicilio_actual', 'pais_origen', 'departamento_nacimiento',
        'provincia_nacimiento', 'distrito_nacimiento'
    )


@admin.register(CiudadanoRN)
class CiudadanoRNAdmin(admin.ModelAdmin):
    search_fields = ('cui', 'numero_dni_ciudadano')
    list_display = ('cui', 'numero_dni_ciudadano', 'ciudadano', 'fecha_nacimiento', 'sexo_nacido')


class CiudadanoParentescoAdmin(admin.ModelAdmin):
    list_display = ('titular', 'parentesco', 'pariente')

    class Meta:
        model = CiudadanoParentesco


admin.site.register(CiudadanoParentesco, CiudadanoParentescoAdmin)
