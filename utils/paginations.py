from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class PageNumber25Pagination(PageNumberPagination):
    page_size = 25
    page_size_query_param = 'page_size'
    max_page_size = 1000

    def get_paginated_response(self, data):
        return Response({
            'total_pages': self.page.paginator.num_pages,
            'results': data
        })

    def get_paginated_response_schema(self, schema):
        return {
            'type': 'object',
            'properties': {
                'total_pages': {
                    'type': 'integer',
                    'example': 10
                },
                'results': schema
            }
        }

