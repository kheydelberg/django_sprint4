"""
Добавлены новые модели: CreatedTimeIsPublishedModel, Comment.
CreatedTimeIsPublishedModel облегчает добавление
стандартных полей в другие модели, наследующие от нее.
Связано с требованиями: 1.1., 1.2., 1.6., 1.7., 2.2., 2.6.
"""

from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

STRING_LENGTH = 25
User = get_user_model()


class CreatedTimeIsPublishedModel(models.Model):
    """
    Абстрактная модель, которая используется для моделей,
    которым требуется информация
    о статусе публикации и времени создания.
    """

    is_published = models.BooleanField(
        default=True,
        verbose_name='Опубликовано',
        help_text='Снимите галочку, чтобы скрыть публикацию.'
    )
    created_at = models.DateTimeField(
        verbose_name='Добавлено',
        auto_now_add=True
    )

    class Meta:
        abstract = True

    def __str__(self):
        return (f'{self.is_published=}, {self.created_at=}')


class Category(CreatedTimeIsPublishedModel):
    """
    Модель для категорий, к которым могут быть привязаны посты.
    С возможностью редактирования в админке.
    """

    title = models.CharField(max_length=256, verbose_name='Заголовок')
    description = models.TextField(verbose_name='Описание')
    slug = models.SlugField(
        unique=True,
        verbose_name='Идентификатор',
        help_text=('Идентификатор страницы для URL; '
                   'разрешены символы латиницы, '
                   'цифры, дефис и подчёркивание.'),
        max_length=128
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title


class Location(CreatedTimeIsPublishedModel):
    """
    Модель для местоположений, к которым могут быть привязаны посты.
    С возможностью редактирования в админке.
    """

    name = models.CharField(
        max_length=256,
        verbose_name='Название места'
    )

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return self.name


class Post(CreatedTimeIsPublishedModel):
    """
    Модель для публикаций в блоге.
    Содержит заголовок, текст, дату публикации, а также
    связь с пользователем, категорией и местоположением.
    """

    title = models.CharField(max_length=256, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Текст')
    pub_date = models.DateTimeField(
        verbose_name='Дата и время публикации',
        help_text='Если установить дату и время в будущем — '
        'можно делать отложенные публикации.'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации',
        related_name='posts'
    )
    location = models.ForeignKey(
        Location,
        null=True,
        on_delete=models.SET_NULL,
        blank=True,
        verbose_name='Местоположение',
    )
    category = models.ForeignKey(
        Category,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='Категория',
        related_name='posts'
    )
    image = models.ImageField('Фото', upload_to='post_images/', blank=True)

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.pk])


class Comment(models.Model):
    """
    Модель для комментариев к публикациям.
    Связана с пользователем и публикацией.
    """

    text = models.TextField("Текст")
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации',
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        verbose_name='Номер публикации',
        related_name='comments'
    )
    created_at = models.DateTimeField('Добавлено', auto_now_add=True)

    class Meta:
        default_related_name = 'comments'
        ordering = ('created_at',)
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text
