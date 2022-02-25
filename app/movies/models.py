import uuid
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _
from django.db.models import UniqueConstraint


class TimeStamped(models.Model):
    # информации о дате и времени создания записи
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        # класс не является представлением таблицы
        abstract = True


class TimeStampedMixin(TimeStamped):
    # информации о дате и времени последнего изменения записи
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        # класс не является представлением таблицы
        abstract = True
        

class UUIDMixin(models.Model):
    # поле id из таблицы
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        # класс не является представлением таблицы
        abstract = True


class Genre(UUIDMixin, TimeStampedMixin):
    name = models.CharField(_('name'), max_length=255)
    description = models.TextField(_('description'), blank=True)
    
    # настройка отображения
    def __str__(self):
        return self.name

    class Meta:
        # путь до таблицы в схеме
        db_table = "content\".\"genre"
        # название модели в интерфейсе
        verbose_name = _('genre')
        verbose_name_plural = _('genres')


class Person(UUIDMixin, TimeStampedMixin):

    full_name = models.CharField(_('full name'), max_length=255)
    birth_date = models.DateField(_('birth date'), default=None, blank=True, null=True)

    # настройка отображения
    def __str__(self):
        return self.full_name 
    
    class Meta:
        db_table = "content\".\"person"
        # название модели в интерфейсе
        verbose_name = _('person')
        verbose_name_plural = _('persons')


class Filmwork(UUIDMixin, TimeStampedMixin):

    class FilmType(models.TextChoices):
        MOVIE = 'movie', _('movie')
        TV_SHOW = 'TV series', _('TV series')

    title = models.CharField(_('title'), max_length=255)
    description = models.TextField(_('description'), blank=True)
    creation_date = models.DateField(_('creation date'))
    rating = models.FloatField(_('rating'), blank=True,
                               validators=[MinValueValidator(0),
                                           MaxValueValidator(100)]) 
    type = models.CharField(
        max_length=9,
        choices=FilmType.choices,
        default=FilmType.MOVIE,)
    genres = models.ManyToManyField(Genre, through='GenreFilmwork')
    persons = models.ManyToManyField(Person, through='PersonFilmwork')
    certificate = models.CharField(_('certificate'), max_length=512, blank=True, null=True)
    file_path = models.FileField(_('file'), blank=True, null=True, upload_to='movies/')
    
    # настройка отображения
    def __str__(self):
        return self.title 
    
    class Meta:
        # путь до таблицы в схеме
        db_table = "content\".\"film_work"
        # название модели в интерфейсе
        verbose_name = _('movie')
        verbose_name_plural = _('movies')


class GenreFilmwork(UUIDMixin, TimeStamped):
    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE)
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE)
    
    class Meta:
        db_table = "content\".\"genre_film_work" 
        # название модели в интерфейсе
        verbose_name = _('movie genre')
        verbose_name_plural = _('movie genres')
        indexes = [
            models.Index(fields=['film_work_id', 'genre_id'], name='film_work_genre'),
        ]
        constraints = [
            UniqueConstraint(fields=['film_work_id', 'genre_id'], name='film_work_genre'),
        ]


class PersonRole(models.TextChoices):
    DIRECTOR = 'director', _('director')
    WRITER = 'writer', _('writer')
    ACTOR = 'actor', _('actor')


class PersonFilmwork(UUIDMixin, TimeStamped):

    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE)
    person = models.ForeignKey('Person', on_delete=models.CASCADE)
    role = models.CharField(
        max_length=9,
        choices=PersonRole.choices,
        default=PersonRole.ACTOR,)
    
    class Meta:
        db_table = "content\".\"person_film_work"
        # название модели в интерфейсе
        verbose_name = _('movie person')
        verbose_name_plural = _('movie persons')
        indexes = [
            models.Index(fields=['film_work_id', 'person_id', 'role'], name='film_work_person_role'),
        ]
        constraints = [
            UniqueConstraint(fields=['film_work_id', 'person_id', 'role'], name='film_work_person_role'),
        ]
