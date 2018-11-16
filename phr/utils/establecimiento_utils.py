# coding=utf-8
import csv

from django.contrib.gis.geos import Point

from phr.establecimiento.models import (
    Diresa, Establecimiento, EstablecimientoCategoria, EstablecimientoSector, Microred, Red, Servicio,
)
from phr.ubigeo.models import UbigeoDistrito


def carga_servicios():
    with open('/home/cj/Documents/Tablas/Establecimiento_Servicio/Servicios.csv', newline='', encoding='latin-1') as f:
        rows = csv.reader(f, delimiter="|")
        rows.__next__()
        for row in rows:
            Servicio.objects.create(codigo=row[0], descripcion=row[1], estado=int(row[2]))


def carga_servicio_establecimiento():
    with open('/home/cj/Documents/Tablas/Establecimiento_Servicio/Establecimiento_Servicio.csv', newline='',
              encoding='latin-1') as f:
        rows = csv.reader(f, delimiter="|")
        rows.__next__()
        for row in rows:
            try:
                establecimiento = Establecimiento.objects.get(codigo_renaes=row[0])
                servicio = Servicio.objects.get(codigo=row[1])
                establecimiento.servicios.add(servicio)
            except Exception as ex:
                print(ex)


def create_red_vacia():
    for diresa in Diresa.objects.all():
        Red.objects.get_or_create(codigo='00', nombre='No pertenece a ninguna Red', diresa=diresa)


def create_microred_vacia():
    for red in Red.objects.filter(codigo='00'):
        Microred.objects.get_or_create(codigo='00', nombre='No pertenece a ninguna Red', red=red, diresa=red.diresa)


def actualizar_micored_establecimiento():
    establecimientos = Establecimiento.objects.filter(microred_id=288)
    for estab in establecimientos:
        microred = Microred.objects.get(codigo='00', diresa=estab.diresa)
        estab.microred = microred
        estab.red = microred.red
        estab.save()


def obtener_sector(sector_cod, sector_nombre):
    sector, is_new = EstablecimientoSector.objects.get_or_create(codigo=sector_cod)
    if is_new:
        sector.descripcion = sector_nombre
        sector.save()
    return sector


def obtener_categoria(categoria_cod):
    categoria, is_new = EstablecimientoCategoria.objects.get_or_create(nombre_categoria=categoria_cod)
    if is_new:
        categoria.nombre_categoria = categoria_cod
        categoria.save()
    return categoria


def diresa_red_mred(diresa_cod, diresa_nom, red_cod, red_nom, mred_cod, mred_nom):
    diresa, d_is_new = Diresa.objects.get_or_create(codigo=diresa_cod)
    if d_is_new:
        diresa.nombre = diresa_nom
        diresa.save()
    red, r_is_new = Red.objects.get_or_create(codigo=red_cod, diresa=diresa)
    if r_is_new:
        red.nombre = red_nom
        red.save()
    microred, m_is_new = Microred.objects.get_or_create(codigo=mred_cod, red=red, diresa=diresa)
    if m_is_new:
        microred.nombre = mred_nom
        microred.save()
    return diresa, red, microred


def obtener_ubigeo(ubigeo):
    distrito = UbigeoDistrito.objects.get(cod_ubigeo_inei_distrito=ubigeo)
    return distrito.provincia.departamento.pais.continente, distrito.provincia.departamento.pais, distrito.provincia.departamento, distrito.provincia, distrito  # noqa


def carga_establecimiento(filename):
    if not filename:
        filename = '/home/cj/Documents/Tablas/establecimientos17.csv'
    i = 0
    e = 0
    with open(filename, newline='', encoding='utf-8') as f:
        rows = csv.reader(f, delimiter=",")
        rows.__next__()
        for row in rows:
            try:
                cod_renaes = row[0]
                nombre = row[4]
                sector_cod = row[6]
                sector_nombre = row[7]
                sector = obtener_sector(sector_cod, sector_nombre)
                direccion = row[8]
                ubigeo = row[9]
                continente, pais, departamento, provincia, distrito = obtener_ubigeo(ubigeo)
                telefono = row[13]
                categoria_cod = row[22]
                categoria = obtener_categoria(categoria_cod)
                diresa_cod = row[35]
                red_cod = row[36]
                mred_cod = row[37]
                diresa_nom = row[38]
                red_nom = row[39]
                mred_nom = row[40]
                point_lat = float(row[42])
                point_lon = float(row[43])
                diresa, red, microred = diresa_red_mred(diresa_cod, diresa_nom, red_cod, red_nom, mred_cod, mred_nom)

                establecimiento, _ = Establecimiento.objects.get_or_create(codigo_renaes=cod_renaes)
                establecimiento.nombre = nombre
                establecimiento.sector = sector
                establecimiento.direccion = direccion
                establecimiento.telefono = telefono
                establecimiento.categoria = categoria
                establecimiento.diresa = diresa
                establecimiento.red = red
                establecimiento.microred = microred
                establecimiento.ubigeo = ubigeo
                establecimiento.continente = continente
                establecimiento.pais = pais
                establecimiento.departamento = departamento
                establecimiento.provincia = provincia
                establecimiento.distrito = distrito
                if point_lat and point_lon:
                    estab_point = Point(point_lat, point_lon, srid=4326)
                    establecimiento.location = estab_point
                establecimiento.save()
                i += 1
                print(i, ">", cod_renaes)
            except Exception as ex:
                ferr = open('/home/cj/err.txt', 'a')
                ferr.writelines("{} > {} \n".format(ex, row))
                ferr.close()
                e += 1
                print(ex, row)
        print("Agregados: {} | Errores : {}".format(i, e))
