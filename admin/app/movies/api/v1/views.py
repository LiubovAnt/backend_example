from django.contrib.postgres.aggregates import ArrayAgg
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q as QCONST
from django.http import JsonResponse
from django.views.generic.detail import BaseDetailView
from django.views.generic.list import BaseListView
from movies.models import Filmwork, PersonRole


class MoviesApiMixin:
    # Основной класс
    model = Filmwork
    http_method_names = ["get"]

    def get_queryset(self):
        # Формирования QuerySet
        genres = ArrayAgg("genres__name", distinct=True)
        annotate_dict = {"genres": genres}
        for role in PersonRole:
            role = "{role}s".format(role=role.value)
            persons = ArrayAgg(
                "persons__full_name",
                filter=QCONST(personfilmwork__role=role),
                distinct=True,
            )
            annotate_dict[role] = persons

        return self.model.objects.values(
            "id",
            "title",
            "description",
            "creation_date",
            "rating",
            "type",
        ).annotate(**annotate_dict)

    def render_to_response(self, context, **response_kwargs):
        # Возвращает сформированные данные в GET запросе
        return JsonResponse(context)


class MoviesListApi(MoviesApiMixin, BaseListView):
    paginate_by = 50

    def paginate_queryset(self, queryset, paginate_by, page_num):
        # Пагинатор для вывода:
        # input:
        #   queryset - разбиваемый QuerySet,
        #    paginate_by - число запросов на странице,
        #    page_num - номер страницы
        paginator = Paginator(queryset, paginate_by)
        if page_num == "last":
            page_num = paginator.num_pages
        try:
            page = paginator.page(page_num)
        except PageNotAnInteger:
            page = paginator.page(1)
        try:
            prev_page_num = page.previous_page_number()
        except EmptyPage:
            prev_page_num = None
        except AttributeError:
            prev_page_num = None
        try:
            next_page_num = page.next_page_number()
        except EmptyPage:
            next_page_num = None
        except AttributeError:
            next_page_num = None
        return paginator, page, prev_page_num, next_page_num

    def get_context_data(self, *, object_list=None, **kwargs):
        # Вовращает словарь с данными для формирования страницы
        queryset = self.get_queryset()
        page_num = self.request.GET.get("page")
        paginator, page, prev_page_num, next_page_num = self.paginate_queryset(
            queryset,
            self.paginate_by,
            page_num,
        )
        results = list(page)
        return {
            "count": paginator.count,
            "total_pages": paginator.num_pages,
            "prev": prev_page_num,
            "next": next_page_num,
            "results": results,
        }


class MoviesDetailApi(MoviesApiMixin, BaseDetailView):
    # Возврат фильма по ID
    def get_context_data(self, **kwargs):
        return self.get_object()
