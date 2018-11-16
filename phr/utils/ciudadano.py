import uuid

from django.core.paginator import Paginator

from phr.ciudadano.models import Ciudadano


def actualiza_uuid():
    ciudadanos = Ciudadano.objects.filter(uuid='')
    paginator = Paginator(ciudadanos, 10000)

    for i in paginator.page_range:
        cpage = paginator.page(i)
        u = 0
        for row in cpage.object_list:
            row.uuid = uuid.uuid4()
            row.save(update_fields=['uuid'])
            u += 1
            print(row.uuid, i, u)


def actualiza_uuid_1000():
    ciudadanos = Ciudadano.objects.filter(uuid='')
    paginator = Paginator(ciudadanos, 1000)
    cpage = paginator.page(1)
    u = 0

    for row in cpage.object_list:
        row.uuid = uuid.uuid4()
        row.save(update_fields=['uuid'])
        u += 1
        print(row.uuid, u)
