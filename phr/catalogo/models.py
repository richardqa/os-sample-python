# coding=utf-8
from django.db import models


class CatalogoCIE(models.Model):
    id_ciex = models.CharField(max_length=10, unique=True)
    desc_ciex = models.TextField(null=False, blank=False)
    id_sexo = models.CharField(max_length=20, null=True, blank=True)
    id_tipedad_min = models.CharField(max_length=10, null=True, blank=True)
    min_edad = models.CharField(max_length=10, null=True, blank=True)
    id_tipedad_max = models.CharField(max_length=10, null=True, blank=True)
    max_edad = models.CharField(max_length=10, null=True, blank=True)
    fg_tipdiag = models.CharField(max_length=10, null=True, blank=True)
    clase1 = models.CharField(max_length=10, null=True, blank=True)
    lab1 = models.CharField(max_length=10, null=True, blank=True)
    lab2 = models.CharField(max_length=10, null=True, blank=True)
    lab3 = models.CharField(max_length=10, null=True, blank=True)
    lab4 = models.CharField(max_length=10, null=True, blank=True)
    lab5 = models.CharField(max_length=10, null=True, blank=True)
    id_ciex_and = models.CharField(max_length=10, null=True, blank=True)
    id_ciex_or = models.CharField(max_length=10, null=True, blank=True)
    fg_ciex = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return '{codigo} - {nombre}'.format(codigo=self.id_ciex, nombre=self.desc_ciex)

    @property
    def get_ciex_codesc(self):
        return self.__str__()


class CatalogoProcedimiento(models.Model):
    codigo_grupo = models.CharField(max_length=10, null=True, blank=True)
    nombre_grupo = models.CharField(max_length=200, null=True, blank=True)
    codigo_seccion = models.CharField(max_length=10, null=True, blank=True)
    descripcion_seccion = models.CharField(max_length=200, null=True, blank=True)
    codigo_subseccion = models.CharField(max_length=10, null=True, blank=True)
    subdivision_anatomica = models.CharField(max_length=200, null=True, blank=True)
    codigo_cpt = models.CharField(max_length=20, null=False, blank=False)
    denominacion_procedimiento = models.TextField(null=False, blank=False)

    def __str__(self):
        return '{} - {}'.format(self.codigo_cpt, self.denominacion_procedimiento)


class CatalogoDeficiencia(models.Model):
    categoria_deficiencia = models.CharField(
        max_length=10, null=False, blank=False)
    nombre_deficiencia = models.CharField(
        max_length=200, null=False, blank=False)

    def __str__(self):
        return '{} - {}'.format(self.categoria_deficiencia, self.nombre_deficiencia)

    @property
    def get_deficiencia_subnivel(self):
        sub_deficiencias = CatalogoDeficiencia.objects.filter(
            categoria_deficiencia__startswith=self.categoria_deficiencia)
        return [{'categoria_deficiencia': deficiencia.categoria_deficiencia,
                 'nombre_deficiencia': deficiencia.nombre_deficiencia} for deficiencia in sub_deficiencias]


class CatalogoDiscapacidad(models.Model):
    categoria_discapacidad = models.CharField(
        max_length=10, null=False, blank=False)
    nombre_discapacidad = models.CharField(
        max_length=200, null=False, blank=False)

    def __str__(self):
        return self.nombre_discapacidad


class CatalogoRaza(models.Model):
    descripcion = models.CharField(max_length=60)

    def __str__(self):
        return self.descripcion

    @property
    def get_etnias(self):
        return [{'id_etnia': etnia.id_etnia, 'descripcion': etnia.descripcion} for etnia in
                CatalogoEtnia.objects.filter(raza=self)]


class CatalogoEtnia(models.Model):
    id_etnia = models.CharField(max_length=2)
    descripcion = models.CharField(max_length=200, null=False, blank=False)
    raza = models.ForeignKey(CatalogoRaza, null=True)

    def __str__(self):
        return self.descripcion


class CatalogoFinanciador(models.Model):
    codigo = models.CharField(
        max_length=10, unique=True, null=False, blank=False)
    descripcion = models.CharField(max_length=20, null=False, blank=False)

    def __str__(self):
        return self.descripcion


class CatalogoAyudaTecnica(models.Model):
    codigo = models.CharField(
        max_length=10, unique=True, null=False, blank=False)
    descripcion = models.CharField(max_length=200, null=False, blank=False)

    def __str__(self):
        return self.descripcion


class CatalogoGradoInstruccion(models.Model):
    codigo = models.CharField(
        max_length=10, unique=True, null=False, blank=False)
    descripcion = models.CharField(max_length=200, null=False, blank=False)

    def __str__(self):
        return self.descripcion


class FamiliaMedicamentoAntecedenteSugerido(models.Model):
    """ Familia de medicamentos para antecedentes de medicación habitual sugeridos """
    codigo = models.CharField(max_length=10, primary_key=True)
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class MedicamentoAntecedenteSugerido(models.Model):
    """ Medicamentos para antecedentes de medicación habitual sugeridos """
    codigo = models.CharField(max_length=10, primary_key=True)
    nombre = models.CharField(max_length=100)
    es_activo = models.BooleanField(default=True)

    familia = models.ForeignKey(FamiliaMedicamentoAntecedenteSugerido)

    def __str__(self):
        return self.nombre
