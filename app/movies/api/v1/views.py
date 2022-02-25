from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q
from django.http import JsonResponse
from django.views.generic.list import BaseListView
from django.views.generic.detail import BaseDetailView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from movies.models import Filmwork, PersonRole


class MoviesApiMixin:
    """Основной класс"""
    model = Filmwork
    http_method_names = ['get']

    def get_queryset(self):
        """Формирования QuerySet"""
        genres = ArrayAgg('genres__name', distinct=True)
        annotate_dict = dict()
        annotate_dict['genres'] = genres
        for role in PersonRole:
            role = role.value
            persons = ArrayAgg(
                'persons__full_name',
                filter=Q(personfilmwork__role=role),
                distinct=True
            )
            annotate_dict[role] = persons
        data_from_db = self.model.objects.values('id', 'title', 'description', 'creation_date', 'rating', 'type',)\
            .annotate(**annotate_dict)
        return data_from_db  # Сформированный QuerySet

    def render_to_response(self, context, **response_kwargs):
        """Возвращает сформированные данные, который должны вернуться в GET запросе"""
        return JsonResponse(context)


class MoviesListApi(MoviesApiMixin, BaseListView):
    paginate_by = 50

    def paginate_queryset(self, queryset,  paginate_by, page_num):
        """
        Пагинатор для вывода:
        input:
            queryset - разбиваемый QuerySet,
            paginate_by - число запросов на странице,
            page_num - номер страницы
        """
        paginator = Paginator(queryset, paginate_by)
        try:
            page = paginator.page(page_num)
        except PageNotAnInteger:
            page = queryset
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
        """
        Вовращает словарь с данными для формирования страницы
        """
        queryset = self.get_queryset()
        page_num = self.request.GET.get('page')
        paginator, page, prev_page_num, next_page_num = self.paginate_queryset(
            queryset,
            self.paginate_by,
            page_num
        )
        results = list(page)
        context = {
            'count': paginator.count,
            'total_pages': paginator.num_pages,
            'prev': prev_page_num,
            'next': next_page_num,
            'results': results
        }
        return context


class MoviesDetailApi(MoviesApiMixin, BaseDetailView):
    """Возврат фильма по ID"""
    def get_context_data(self, **kwargs):
        return self.get_object()
