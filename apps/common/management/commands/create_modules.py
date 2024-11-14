from django.core.management import BaseCommand
from apps.users.models import Action, Module, Section, APIRoute
import json

SECTIONS = json.loads(open('perms.json').read())


class Command(BaseCommand):
    def handle(self, *args, **options):

        for section in SECTIONS:
            s_obj, created = Section.objects.get_or_create(name=section['name'])

            for module in section['modules']:
                m_obj, created = Module.objects.get_or_create(name=module['name'], section=s_obj)

                for action in module['actions']:
                    ac_obj, created = Action.objects.get_or_create(name=action['name'], module=m_obj)

                    for api in action['apis']:
                        ap_obj = APIRoute.objects.filter(
                            route=api['route'],
                            name=api['name'],
                            dynamic=api['dynamic'],
                            method=api['method'],
                        ).first()

                        if ap_obj:
                            ac_obj.apis.add(ap_obj)

