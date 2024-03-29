from django.contrib import admin
from movies.models import (
    Filmwork,
    Genre,
    GenreFilmwork,
    Person,
    PersonFilmwork,
)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    # Поиск по полям
    search_fields = ("name", "description", "id")


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    # Поиск по полям
    search_fields = ("full_name",)


class GenreFilmworkInline(admin.TabularInline):
    model = GenreFilmwork


class PersonFilmworkInline(admin.TabularInline):
    model = PersonFilmwork
    autocomplete_fields = ("person",)


@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):

    inlines = (GenreFilmworkInline, PersonFilmworkInline)
    # Отображение полей в списке
    list_display = ("title", "type", "creation_date", "rating")

    # Фильтрация в списке
    list_filter = ("type",)

    # Поиск по полям
    search_fields = ("title", "description", "id")
