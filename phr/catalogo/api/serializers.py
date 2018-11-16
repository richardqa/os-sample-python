# coding=utf-8
from rest_framework import serializers

from phr.catalogo.models import (
    CatalogoAyudaTecnica, CatalogoCIE, CatalogoDeficiencia, CatalogoDiscapacidad, CatalogoEtnia, CatalogoFinanciador,
    CatalogoGradoInstruccion, CatalogoProcedimiento, CatalogoRaza, FamiliaMedicamentoAntecedenteSugerido,
    MedicamentoAntecedenteSugerido,
)


class ListaCatalogoCIESerializer(serializers.ModelSerializer):
    class Meta:
        model = CatalogoCIE
        exclude = []


class DetalleCatalogoCIESerializer(serializers.ModelSerializer):
    class Meta:
        model = CatalogoCIE
        exclude = []


class ListaCatalogoProcedimientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CatalogoProcedimiento
        exclude = []


class DetalleCatalogoProcedimientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CatalogoProcedimiento
        exclude = []


class ListaCatalogoDeficienciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = CatalogoDeficiencia
        exclude = []


class DetalleCatalogoDeficienciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = CatalogoDeficiencia
        fields = ['id', 'categoria_deficiencia', 'nombre_deficiencia', 'get_deficiencia_subnivel']


class ListaCatalogoDiscapacidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = CatalogoDiscapacidad
        exclude = []


class DetalleCatalogoDiscapacidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = CatalogoDiscapacidad
        exclude = []


class ListaCatalogoRazaSerializer(serializers.ModelSerializer):
    class Meta:
        model = CatalogoRaza
        exclude = []


class DetalleCatalogoRazaSerializer(serializers.ModelSerializer):
    class Meta:
        model = CatalogoRaza
        fields = ['descripcion', 'get_etnias']
        exclude = []


class ListaCatalogoEtniaSerializer(serializers.ModelSerializer):
    class Meta:
        model = CatalogoEtnia
        exclude = []


class DetalleCatalogoEtniaSerializer(serializers.ModelSerializer):
    class Meta:
        model = CatalogoEtnia
        exclude = []


class ListaCatalogoFinanciadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = CatalogoFinanciador
        exclude = []


class DetalleCatalogoFinanciadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = CatalogoFinanciador
        exclude = []


class ListaCatalogoAyudaTecnicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = CatalogoAyudaTecnica
        exclude = []


class DetalleCatalogoAyudaTecnicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = CatalogoAyudaTecnica
        exclude = []


class ListaCatalogoGradoInstruccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CatalogoGradoInstruccion
        exclude = []


class DetalleCatalogoGradoInstruccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CatalogoAyudaTecnica
        exclude = []


class MedicamentoFamiliaAntecedenteSugeridoSerializer(serializers.ModelSerializer):
    class Meta:
        model = FamiliaMedicamentoAntecedenteSugerido
        fields = ('codigo', 'nombre',)


class MedicamentoAntecedenteSugeridoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicamentoAntecedenteSugerido
        fields = ('codigo', 'nombre',)
