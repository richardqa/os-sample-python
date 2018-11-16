import csv

from django.core.management import BaseCommand

from phr.establecimiento.models import Microred, Red


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open('microredes.csv') as f:
            """La estructura del .csv debe ser codigo_microred, nombre_microred, codigo_red, codigo_diresa."""
            rows = csv.reader(f)
            total = 0
            creados = 0
            actualizados = 0
            for row in rows:
                total += 1
                red = None
                try:
                    red = Red.objects.get(codigo=row[2], diresa__codigo=row[3])
                except Red.DoesNotExist:
                    self.stdout.write('No existe la Red con código: {}'.format(row[2]))
                except Red.MultipleObjectsReturned:
                    self.stdout.write('Múltiples coincidencias para la Red con código: {}'.format(row[2]))
                except Exception as ex:
                    self.stdout.write(str(ex))
                if not red:
                    continue
                try:
                    microred = Microred.objects.get(codigo=row[0], red=red, diresa=red.diresa)
                    microred.nombre = row[1]
                    microred.save()
                    actualizados += 1
                except Microred.DoesNotExist:
                    Microred.objects.create(
                        codigo=row[0],
                        nombre=row[1],
                        red=red,
                        diresa=red.diresa
                    )
                    creados += 1
                    self.stdout.write('Creando microred: {} {} {}'.format(row[0], row[1], row[2]))
                except Exception as ex:
                    self.stdout.write(str(ex))
            self.stdout.write('Total: {}'.format(total))
            self.stdout.write('Creados: {}'.format(creados))
            self.stdout.write('Actualizados: {}'.format(actualizados))
