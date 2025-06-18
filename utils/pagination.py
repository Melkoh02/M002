from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPageSizePagination(PageNumberPagination):
    page_size = 10

    def get_page_size(self, request):
        page_size = request.query_params.get('page_size')
        if page_size is not None:
            try:
                return int(page_size)
            except ValueError:
                pass
        return self.page_size

    def get_paginated_response(self, data):
        """
        Overwriting method get_paginated_response to add page, start and end to pagination output style.
        """
        return Response({
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'page': self.page.number,
            'start': self.page.start_index(),
            'end': self.page.end_index(),
            'results': data
        })
