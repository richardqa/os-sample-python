# coding=utf-8
import csv
import datetime
import re

from phr.ciudadano.models import Ciudadano
from phr.ubigeo.models import UbigeoDepartamento, UbigeoDistrito, UbigeoProvincia


def get_departamento(ubigeo):
    try:
        return UbigeoDepartamento.objects.get(cod_ubigeo_reniec_departamento=ubigeo)
    except Exception as ex:
        return None


def get_provincia(ubigeo):
    try:
        return UbigeoProvincia.objects.get(cod_ubigeo_reniec_provincia=ubigeo)
    except Exception as ex:
        return None


def get_distrito(ubigeo):
    try:
        return UbigeoDistrito.objects.get(cod_ubigeo_reniec_distrito=ubigeo)
    except Exception as ex:
        return None


def get_fecha_nac(fechastr):
    try:
        return datetime.datetime.strptime(
            '{}-{}-{}'.format(fechastr[:4], fechastr[4:6], fechastr[-2:]), '%Y-%m-%d').date()
    except Exception as ex:
        print("{} - {}".format(ex, fechastr))
        return None


def cargar_ciudadano():
    i = 0
    with open('/home/cj/Documents/Tablas/pacientes_new.csv', newline='', encoding='latin-1') as f:
        rows = csv.reader(f, delimiter='|')
        rows.__next__()
        for row in rows:
            try:
                if re.match("^[\d]+$", row[5]):
                    i += 1
                    print(i)

                    cdno, is_new = Ciudadano.objects.get_or_create(
                        tipo_documento=row[3], tipo_documento_minsa=row[4], numero_documento=row[5])
                    if is_new:
                        cdno.nombres = row[0] or None
                        cdno.apellido_paterno = row[1] or None
                        cdno.apellido_materno = row[2] or None
                        cdno.correo = row[6] or None
                        cdno.telefono = row[7] or None
                        cdno.celular = row[8] or None
                        cdno.domicilio_direccion = row[9] or None
                        cdno.domicilio_referencia = row[10] or None
                        cdno.nacimiento_ubigeo = row[11] or None
                        cdno.sexo = row[12] or None
                        cdno.estado_civil = row[13] or None
                        cdno.etnia = row[14] or None
                        cdno.lengua = row[15] or None
                        cdno.tipo_seguro = row[16] or None
                        cdno.estado = '1'
                        cdno.continente_domicilio_id = 1
                        cdno.pais_domicilio_id = 1
                        cdno.departamento_nacimiento = get_departamento(row[20])
                        cdno.provincia_nacimiento = get_provincia(row[26])
                        cdno.distrito_nacimiento = get_distrito(row[22])
                        cdno.departamento_domicilio = get_distrito(row[19])
                        cdno.provincia_domicilio = get_distrito(row[25])
                        cdno.distrito_domicilio = get_distrito(row[21])
                        cdno.fecha_nacimiento = get_fecha_nac(row[27])
                        cdno.cui = row[28] or None
                        cdno.grado_instruccion = row[29] or None
                        cdno.ocupacion = row[30] or None

                        cdno.save()
            except Exception as ex:
                print(ex, row)
                with open('/home/cj/Documents/Tablas/pacientes_new_error.csv', 'a', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(row)
