# coding=utf-8
import csv

from phr.ubigeo.models import UbigeoDistrito, UbigeoLocalidad


def get_distrito(ubigeo):
    try:
        return UbigeoDistrito.objects.get(cod_ubigeo_inei_distrito=ubigeo)
    except Exception as ex:
        return None


def get_area(area_str):
    if area_str == 'URBANO':
        return 1
    elif area_str == 'RURAL':
        return 2
    return None


def get_region(region_str):
    if region_str == 'COSTA':
        return 1
    elif region_str == 'SIERRA':
        return 2
    elif region_str == 'SELVA':
        return 3
    elif region_str == 'LIMA METROPOLITANA':
        return 4
    return None


def data_distritos():
    i = 0
    with open('/home/cj/Documents/Tablas/ubigeo_2014.csv', newline='', encoding='latin-1') as f:
        rows = csv.reader(f)
        for row in rows:
            i += 1
            try:
                distrito = get_distrito(row[0])
                distrito.cod_ubigeo_reniec_distrito = row[1]
                distrito.l_inf = row[5] or None
                distrito.l_sup = row[6] or None
                distrito.pobreza = row[7] or None
                distrito.quintil_20 = row[8] or None
                distrito.area = get_area(row[9])
                distrito.region = get_region(row[10])
                distrito.save()
            except Exception as ex:
                print(ex, i, row)


def distritos_friaje():
    i = 0
    with open('/home/cj/Documents/Tablas/ubigeo_2014_friaje.csv', newline='', encoding='latin-1') as f:
        rows = csv.reader(f)
        for row in rows:
            i += 1
            try:
                distrito = get_distrito(row[0])
                distrito.tiene_friaje = True
                distrito.save()
            except Exception as ex:
                print(ex)


def carga_localidades():
    i = 0
    e = 0
    with open('/home/cj/Documents/Tablas/CentrosPoblados.csv', newline='') as f:
        rows = csv.reader(f)
        rows.__next__()
        last_ubigeo = ''
        i_loc = 0
        for row in rows:
            try:
                ubigeo_dist = "{:06}".format(int(row[1]))
                nombre = row[2]
                if last_ubigeo != ubigeo_dist:
                    last_ubigeo = ubigeo_dist
                    i_loc = 0
                i_loc += 1
                ubigeo_localidad = "{}{:03}".format(ubigeo_dist, i_loc)
                distrito = UbigeoDistrito.objects.get(cod_ubigeo_inei_distrito=ubigeo_dist)
                UbigeoLocalidad.objects.create(
                    cod_ubigeo_inei_localidad=ubigeo_localidad,
                    ubigeo_localidad=nombre,
                    continente=distrito.provincia.departamento.pais.continente,
                    pais=distrito.provincia.departamento.pais,
                    departamento=distrito.provincia.departamento,
                    provincia=distrito.provincia,
                    distrito=distrito,
                )
                i += 1
                print(i, )
            except Exception as ex:
                e += 1
                print(ex, row)
    print(i, e)
