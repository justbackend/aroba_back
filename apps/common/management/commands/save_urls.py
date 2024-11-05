import re

from django.core.management import BaseCommand
from django.urls import get_resolver

from apps.users.models import APIRoute


class Command(BaseCommand):
    help = 'Save URLs'

    def handle(self, *args, **options):
        urls = self.list_api_v1_urls_with_specific_methods()

        for url_info in urls:
            for method in url_info['methods']:
                cleaned_url = self.process_url(url=url_info['url'], method=method)
                APIRoute.objects.get_or_create(**cleaned_url)

    @staticmethod
    def list_api_v1_urls_with_specific_methods():
        url_patterns = get_resolver().url_patterns
        api_v1_urls = []

        target_methods = {
            'partial_update': 'PATCH',
            'create': 'POST',
            'update': 'PUT',
            'partial_delete': 'DELETE',
            'destroy': 'DELETE',
            'retrieve': 'GET',
            'list': 'GET',
        }

        def get_urls(patterns, parent_pattern=""):
            for pattern in patterns:
                if hasattr(pattern, 'url_patterns'):
                    get_urls(pattern.url_patterns, parent_pattern + str(pattern.pattern))
                else:
                    full_url = parent_pattern + str(pattern.pattern)
                    if full_url.startswith("api/v1/"):
                        callback = pattern.callback
                        methods = set()

                        if hasattr(callback, 'actions'):
                            methods = set(target_methods[value] for value in callback.actions.values())
                        elif hasattr(callback, 'view_class'):

                            methods = {
                                method.upper() for method in
                                callback.view_class.http_method_names
                                if method != 'options' and hasattr(callback.view_class, method)
                            }
                        elif callable(callback):
                            methods = {'GET', 'POST', 'PUT', 'DELETE'}  # Custom metodlar kerak bo'lishi mumkin

                        available_methods = methods.intersection(target_methods.values())
                        if available_methods:
                            api_v1_urls.append({
                                'url': full_url,
                                'methods': list(available_methods),
                            })

        get_urls(url_patterns)
        return api_v1_urls

    @staticmethod
    def process_url(url, method) -> dict:
        if not isinstance(url, str):
            print(f"Invalid URL type: {type(url)}, value: {url}")
            raise TypeError("The URL must be a string.")

        pattern = re.compile(r"(api/v1/.+?/)(.*)")
        match = pattern.match(url)
        print(url, method)

        if not match:
            raise ValueError("URL format is incorrect")

        route = f"/{match.group(1)}"
        name = match.group(2) or ''  # Name can be an empty string if there's no additional segment

        # Check if the URL is dynamic (contains path parameters like <int:pk>)
        dynamic = bool(re.search(r"<\w+:\w+>", name))

        if dynamic:
            name = re.sub(r"<\w+:\w+>", "$", name)

        return {
            'route': route,
            'name': name,
            'dynamic': dynamic,
            'method': method
        }
