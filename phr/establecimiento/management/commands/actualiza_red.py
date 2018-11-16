import csv

from django.core.management import BaseCommand

from phr.establecimiento.models import Diresa, Red


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open('redes.csv') as f:
            """La estructura del .csv debe ser codigo_red, nombre_red, codigo disa."""
            rows = csv.reader(f)
            total = 0
            creados = 0
            actualizados = 0
            for row in rows:
                total += 1
                diresa = None
                try:
                    diresa = Diresa.objects.get(codigo=row[2])
                except Diresa.DoesNotExist:
                    self.stdout.write('No existe la Diresa con código: {}'.format(row[2]))
                except Diresa.MultipleObjectsReturned:
                    self.stdout.write('Múltiples coincidencias para la Diresa con código: {}'.format(row[2]))
                if not diresa:
                    continue
                try:
                    red = Red.objects.get(codigo=row[0], diresa=diresa)
                    red.nombre = row[1]
                    red.diresa = diresa
                    red.save()
                    actualizados += 1
                except Red.DoesNotExist:
                    Red.objects.create(
                        codigo=row[0],
                        nombre=row[1],
                        diresa=diresa
                    )
                    creados += 1
                    self.stdout.write('Creando red: {} {} {}'.format(row[0], row[1], row[2]))
            self.stdout.write('Total: {}'.format(total))
            self.stdout.write('Creados: {}'.format(creados))
            self.stdout.write('Actualizados: {}'.format(actualizados))
