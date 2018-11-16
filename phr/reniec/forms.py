from django import forms

from phr.ciudadano.models import CiudadanoRN


class CiudadanoRNForm(forms.ModelForm):
    class Meta:
        model = CiudadanoRN
        fields = (
            'cui', 'tipo_doc_madre', 'numero_doc_madre', 'primer_apellido_madre', 'segundo_apellido_madre',
            'prenombres_madre', 'sexo_nacido', 'fecha_nacimiento', 'hora_nacimiento', 'peso_nacido', 'talla_nacido',
            'apgar_uno_nacido', 'apgar_cinco_nacido', 'numero_nacido_perim_cefalico',
            'numero_nacido_perim_toracico', 'numero_temperatura', 'resultado_examen_fisico', 'edad_examen_fisico',
            'unida_medida_edad', 'duracion_semanas_parto', 'atiende_parto', 'condicion_parto', 'tipo_parto',
            'financiador_parto', 'posicion_parto', 'es_partograma', 'es_acompaniante_parto', 'duracion_parto',
            'es_episiotomia_parto', 'desgarro_parto', 'alumbramiento_parto', 'placenta_parto', 'es_eess_procedencia',
            'eess_procedencia', 'codigo_local', 'codigo_renaes',
        )
