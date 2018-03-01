from rest_framework.pagination import PageNumberPagination


class ResultSetPagination(PageNumberPagination):
    page_query_param = 'page'
    
    page_size_query_param = 'count'
    page_size = 100
    max_page_size = 1000
