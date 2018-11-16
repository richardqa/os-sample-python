import csv

from django.contrib.gis.geos import Point

from phr.establecimiento.models import Establecimiento
from phr.insteducativa.models import InstitucionEducativa


def carga_ie():
    i = 0
    e = 0

    with open('/home/cj/Documents/Tablas/colegios/colegios.csv', newline='') as f:
        rows = csv.reader(f, delimiter=",")
        rows.__next__()
        for row in rows:
            try:
                i += 1
                nombre = row[9]
                codigo_modular = row[7]
                codigo_colegio = row[0]
                ubigeo = "{:06}".format(int(row[5]))
                direccion = row[10]
                nivel = '1' if row[11] == 'INICIAL' else '2' if row[11] == 'PRIMARIA' else '3'
                ubicacion = Point(float(row[13]), float(row[14]), srid=4326)

                ie, _ = InstitucionEducativa.objects.get_or_create(codigo_modular=codigo_modular)
                ie.nombre = nombre
                ie.codigo_modular = codigo_modular
                ie.codigo_colegio = codigo_colegio
                ie.ubigeo = ubigeo
                ie.direccion = direccion
                ie.nivel = nivel
                ie.ubicacion = ubicacion
                ie.save()
                print(i, ie)
            except Exception as ex:
                e += 1
                print(e, ex, row)
    print("correctos: {} - errores: {}".format(i, e))


def ie_estab():
    i = 0
    e = 0

    with open('/home/cj/Documents/Tablas/colegios/estab_colegio.csv', newline='', encoding='latin-1') as f:
        rows = csv.reader(f, delimiter=";")
        rows.__next__()
        for row in rows:
            try:
                i += 1
                codigo_modular = row[4]
                codigo_estab = int(row[1])
                try:
                    establecimiento = Establecimiento.objects.get(codigo_renaes=codigo_estab)
                except Establecimiento.DoesNotExist:
                    establecimiento = None
                try:
                    ie = InstitucionEducativa.objects.get(codigo_modular=codigo_modular)
                    ie.establecimiento = establecimiento
                    ie.save()
                    print(ie)
                except InstitucionEducativa.DoesNotExist:
                    pass
            except Exception as ex:
                e += 1
                print(ex, row)
    print("correctos: {} - errores: {}".format(i, e))


def actualiza_ie_tipo():
    for ie in InstitucionEducativa.objects.all():
        ie.tipo = '2' if ie.nivel == '1' else '3'
        ie.save()
        print(ie)
