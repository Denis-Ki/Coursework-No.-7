from rest_framework.pagination import PageNumberPagination


class HabitsListPagination(PageNumberPagination):
    page_size = 5
