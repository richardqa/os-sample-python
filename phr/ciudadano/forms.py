from django import forms

from phr.ciudadano.models import Ciudadano, CiudadanoDatosSIS


class CiudadanoPadronForm(forms.ModelForm):
    class Meta:
        model = Ciudadano
        fields = (
            'cui',
            'apellido_materno',
            'apellido_paterno',
            'etnia',
            'fecha_nacimiento',
            'foto',
            'nombres',
            'numero_documento',
            'sexo',
            'nacimiento_ubigeo',
        )


class CiudadanoDatosSISForm(forms.ModelForm):
    class Meta:
        model = CiudadanoDatosSIS
        fields = (
            'codigo_eess',
            'contrato',
            'correlativo',
            'disa',
            'estado',
            'fecha_afiliacion',
            'fecha_caducidad',
            'genero',
            'id_grupo_poblacional',
            'id_numero_registro',
            'id_plan',
            'id_ubigeo',
            'nro_contrato',
            'regimen',
            'tabla',
            'tipo_documento',
            'tipo_formato',
            'tipo_seguro',
            'tipo_seguro_descripcion',
        )
