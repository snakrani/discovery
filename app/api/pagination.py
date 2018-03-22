from django.conf import settings

from rest_framework.pagination import PageNumberPagination


class BasePagination(PageNumberPagination):
    page_query_param = 'page'
    page_size_query_param = 'count'


class ResultSetPagination(BasePagination): 
    page_size = settings.REST_PAGE_COUNT
    max_page_size = 1000

class TestResultSetPagination(BasePagination):
    page_size = 20
    max_page_size = 100
