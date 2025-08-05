from rest_framework.pagination import PageNumberPagination

class GenericPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'item_count'
    max_page_size = 100