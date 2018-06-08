from django.core.management.base import BaseCommand

from contracts.models import Contract


class Command(BaseCommand):

    def handle(self, *args, **options):
        for contract in Contract.objects.all().iterator():
            contract.base_piid = contract.piid.split('_')[0]
            contract.save()
