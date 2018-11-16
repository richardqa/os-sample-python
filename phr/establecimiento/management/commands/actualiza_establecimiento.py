import csv

from django.core.management import BaseCommand

from phr.establecimiento.models import (
    Diresa, Establecimiento, EstablecimientoCategoria, EstablecimientoSector, Microred, Red,
)
from phr.ubigeo.models import UbigeoDistrito


class Command(BaseCommand):
    def handle(self, *args, **options):

        with open('establecimientos.csv') as f:
            """
            La estructura del .csv debe ser:
            institución, código único, nombre del eess, clasificación, tipo,
            departamento, provincia, distrito, ubigeo, dirección,
            código disa, código red, código microred, nombre disa, nombre red, nombre microred,
            código UE, unidad ejecutora, categoría, teléfono, coordenada norte, coordenada este.
            """
            rows = csv.reader(f)
            total = 0
            creados = 0
            actualizados = 0
            for row in rows:
                total += 1
                row[1] = row[1].lstrip('0')
                try:
                    eess = Establecimiento.objects.get(codigo_renaes=row[1])
                    es_valido, data, mensaje = self.procesar_data(row)
                    if es_valido:
                        for field in data:
                            setattr(eess, field, data[field])
                        eess.save()
                        actualizados += 1
                    else:
                        self.stdout.write('No se actualizó el eess: {} {}. Error {}'.format(row[1], row[2], mensaje))
                        continue
                except Establecimiento.DoesNotExist:
                    es_valido, data, mensaje = self.procesar_data(row)
                    if es_valido:
                        Establecimiento.objects.create(**data)
                        creados += 1
                        self.stdout.write('Creando establecimiento: {} {}'.format(row[1], row[2]))
                    else:
                        self.stdout.write('No se creó el eess: {} {}. Error {}'.format(row[1], row[2], mensaje))
                        continue
            self.stdout.write('Total: {}'.format(total))
            self.stdout.write('Creados: {}'.format(creados))
            self.stdout.write('Actualizados: {}'.format(actualizados))

    def procesar_data(self, row):
        try:
            distrito = self.get_distrito(row[8])
            data = {
                'codigo_renaes': row[1],
                'nombre': row[2],
                'telefono': row[19],
                'direccion': row[9],
                'sector': self.get_sector(row[0]),
                'categoria': self.get_categoria(row[18]),
                'diresa': self.get_diresa(row[10]),
                'red': self.get_red(row[11], row[10]),
                'microred': self.get_microred(row[12], row[11], row[10]),
                'ubigeo': row[8],
                'continente': distrito.continente,
                'pais': distrito.pais,
                'departamento': distrito.departamento,
                'provincia': distrito.provincia,
                'distrito': distrito
            }
            return True, data, 'Sin problemas'
        except Exception as ex:
            return False, None, str(ex)

    def get_sector(self, name):
        try:
            return EstablecimientoSector.objects.get(descripcion=name)
        except EstablecimientoSector.DoesNotExist:
            raise ValueError('No existe sector con el nombre {}'.format(name))
        except EstablecimientoSector.MultipleObjectsReturned:
            raise ValueError('Existen sectores con el nombre {}'.format(name))

    def get_categoria(self, name):
        try:
            return EstablecimientoCategoria.objects.get(nombre_categoria=name)
        except EstablecimientoCategoria.DoesNotExist:
            raise ValueError('No existe categoría {}'.format(name))
        except EstablecimientoCategoria.MultipleObjectsReturned:
            raise ValueError('Existen categorías  con el nombre {}'.format(name))

    def get_diresa(self, codigo):
        try:
            return Diresa.objects.get(codigo=codigo)
        except Diresa.DoesNotExist:
            raise ValueError('No existe diresa {}'.format(codigo))
        except Diresa.MultipleObjectsReturned:
            raise ValueError('Existen diresas con el código {}'.format(codigo))

    def get_red(self, codigo_red, codigo_disa):
        try:
            return Red.objects.get(codigo=codigo_red, diresa__codigo=codigo_disa)
        except Red.DoesNotExist:
            raise ValueError('No existe red {}'.format(codigo_red))
        except Red.MultipleObjectsReturned:
            raise ValueError('Existen redes  con el código {}'.format(codigo_red))

    def get_microred(self, codigo_microred, codigo_red, codigo_disa):
        try:
            return Microred.objects.get(codigo=codigo_microred,
                                        red__codigo=codigo_red,
                                        diresa__codigo=codigo_disa)
        except Microred.DoesNotExist:
            ValueError('No existe microred {}'.format(codigo_microred))
        except Microred.MultipleObjectsReturned:
            raise ValueError('Existen microredes con el código {}'.format(codigo_microred))

    def get_distrito(self, codigo):
        try:
            return UbigeoDistrito.objects.get(cod_ubigeo_inei_distrito=codigo)
        except UbigeoDistrito.DoesNotExist:
            ValueError('No existe distrito {}'.format(codigo))
        except UbigeoDistrito.MultipleObjectsReturned:
            ValueError('Existen distrito con el código {}'.format(codigo))
