import csv

from phr.catalogo.models import CatalogoProcedimiento


def catalogo_cpt():
    i = 0
    e = 0
    with open('/home/cj/Documents/Tablas/cpt.csv', newline='') as f:
        rows = csv.reader(f)
        for row in rows:
            try:
                cpt_codigo = row[0]
                cpt_descripcion = row[1]
                cpt, _ = CatalogoProcedimiento.objects.get_or_create(codigo_cpt=cpt_codigo)
                cpt.denominacion_procedimiento = cpt_descripcion
                cpt.save()
                i += 1
                print(i)
            except Exception as ex:
                e += 1
                print(ex)
