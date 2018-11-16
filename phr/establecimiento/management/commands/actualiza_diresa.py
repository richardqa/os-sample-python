import csv

from django.core.management import BaseCommand

from phr.establecimiento.models import Diresa
from phr.ubigeo.models import UbigeoDepartamento


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open('diresas.csv') as f:
            """La estructura del .csv debe ser codigo_diresa, nombre_diresa, ubigeo_inei_departamento."""
            rows = csv.reader(f)
            total = 0
            creados = 0
            actualizados = 0
            for row in rows:
                total += 1
                departamento = None
                try:
                    departamento = UbigeoDepartamento.objects.get(cod_ubigeo_inei_departamento=row[2])
                except UbigeoDepartamento.DoesNotExist:
                    self.stdout.write('No existe el departamento con ubigeo: {}'.format(row[2]))
                except UbigeoDepartamento.MultipleObjectsReturned:
                    self.stdout.write('Múltiples coincidencias para el departamento con ubigeo: {}'.format(row[2]))
                if not departamento:
                    continue
                try:
                    diresa = Diresa.objects.get(codigo=row[0])
                    diresa.nombre = row[1]
                    diresa.departamento = departamento
                    diresa.es_activo = True
                    diresa.save()
                    actualizados += 1
                except Diresa.DoesNotExist:
                    Diresa.objects.create(
                        codigo=row[0],
                        nombre=row[1],
                        departamento=departamento,
                        es_activo=True
                    )
                    creados += 1
                    self.stdout.write('Creando diresa: {} {}'.format(row[0], row[1]))
            self.stdout.write('Total: {}'.format(total))
            self.stdout.write('Creados: {}'.format(creados))
            self.stdout.write('Actualizados: {}'.format(actualizados))
