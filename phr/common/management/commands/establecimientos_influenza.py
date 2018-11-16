from django.core.management import BaseCommand

from phr.establecimiento.models import Establecimiento


class Command(BaseCommand):
    help = 'Actualiza Establecimientos que tienen vacuna contra influenza'

    def add_arguments(self, parser):
        parser.add_argument(
            'excluidos',
            help='Codigos RENAES de Establecimientos que no vacunan contra influenza',
            type=str
        )

    def actualizar_establecimientos(self, *args, **options):
        print('Actualizando establecimientos...')
        if options.get('excluidos'):
            establecimientos_excluidos = options.get('excluidos').split(',')
            establecimientos = Establecimiento.objects.filter(sector__codigo__in=['1', '7', '14']).exclude(
                codigo_renaes__in=establecimientos_excluidos).order_by('codigo_renaes')
            total_estab = establecimientos.count()
            print('Cantidad de establecimientos: {}'.format(total_estab))
            i = 0
            for establecimiento in establecimientos:
                i += 1
                establecimiento.tiene_influenza = True
                establecimiento.save()
                print('Actualizado: {} de {}: {} - {}'.format(
                    i, total_estab, establecimiento.codigo_renaes, establecimiento.nombre))

    def handle(self, *args, **options):
        self.actualizar_establecimientos(*args, **options)
