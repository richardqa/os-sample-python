from django import forms

from dal import autocomplete

from phr.ciudadano.models import Ciudadano

from .models import Personal


class PersonalForm(forms.ModelForm):
    ciudadano = forms.ModelChoiceField(
        queryset=Ciudadano.objects.all(),
        widget=autocomplete.ModelSelect2(url='api-phr-personal:ciudadano_autocomplete')
    )

    class Meta:
        model = Personal
        fields = '__all__'
