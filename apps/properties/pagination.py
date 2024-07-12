from rest_framework.pagination import PageNumberPagination


class PropertyPagination(PageNumberPagination):
    def get_page_size(self, request):
        page_size = request.GET.get('page_size')
        return page_size
