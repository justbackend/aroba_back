from django.core.management import BaseCommand
from apps.users.models import Action, Module
from utils.choices import APIRoutes

MODULS = [
    {
        'module': 'Dispetcher',
        'actions': [
            {
                'name': "ko'rish",
                'apis': [
                    {
                        'name': 'new-orders/',
                        'route': APIRoutes.DISPATCHERS,
                        'dynamic': False,
                        'method': 'GET',
                    },
                ]
            },
            {
                'name': "band qilish",
                'apis': [
                    {
                        'name': 'book-orders/$/',
                        'route': APIRoutes.DISPATCHERS,
                        'dynamic': True,
                        'method': 'GET',
                    },
                ]
            },

            {
                'name': "to'ldirish",
                'apis': [
                    {
                        'name': 'fill-order/$/',
                        'route': APIRoutes.DISPATCHERS,
                        'dynamic': True,
                        'method': 'GET',
                    },
                ]
            },


        ]
    },
    {
        'module': 'Manager',
        'actions': [
            {
                'name': "ko'rish",
                'apis': [
                    {
                        'name': 'new-orders/',
                        'route': APIRoutes.DISPATCHERS,
                        'dynamic': False,
                        'method': 'GET',
                    },
                ]
            },
            {
                'name': "band qilish",
                'apis': [
                    {
                        'name': 'book-orders/$/',
                        'route': APIRoutes.DISPATCHERS,
                        'dynamic': False,
                        'method': 'GET',
                    },
                ]
            },
        ]
    },



]


class Command(BaseCommand):
    def handle(self, *args, **options):

        for module in MODULS:
            m_obj = Module.objects.get_or_create(name=module['module'])[0]

            for action in module['actions']:
                Action.objects.get_or_create(module=m_obj, action=action)
