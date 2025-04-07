from rest_framework.pagination import CursorPagination, PageNumberPagination


class BasePagination(PageNumberPagination):
    page_size_query_param = "page_size"
    page_size = 20

    def paginate_queryset(self, queryset, request, view):
        sort_by = request.query_params.get("sort_by", "created_at")
        sort_order = request.query_params.get("sort_order", "desc")
        if sort_order == "desc":
            sort_by = f"-{sort_by}"
        queryset = queryset.order_by(sort_by)
        return super().paginate_queryset(queryset, request, view)


class BaseCursorPagination(CursorPagination):
    page_size_query_param = "page_size"
    ordering = "-created_at"
    page_size = 10

    def get_ordering(self, request, queryset, view):
        sort_by = request.query_params.get("sort_by", "created_at")
        sort_order = request.query_params.get("sort_order", "desc")
        if sort_order == "asc":
            return (sort_by,)
        return (f"-{sort_by}",)
