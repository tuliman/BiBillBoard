from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import Signal

from .utilities import send_activator_notification, get_timestamp_path


class AdvUser(AbstractUser):
    is_active = models.BooleanField(default=True, db_index=True, verbose_name='Прошел валидацию')
    send_massages = models.BooleanField(default=True, verbose_name='Слать оповещения о новых коментариях')

    class Meta(AbstractUser.Meta):
        pass

    def delete(self,*args,**kwargs):
        for bb in self.bb_set.all():
            bb.delete()
        return super().delete(*args,**kwargs)


user_registrated = Signal(providing_args=['instance'])


def user_registrated_dispatcher(sender, **kwargs):
    send_activator_notification(kwargs['instance'])


user_registrated.connect(user_registrated_dispatcher)


class Rubric(models.Model):
    name = models.CharField(max_length=20, db_index=True, unique=True, verbose_name='Название')
    order = models.SmallIntegerField(default=0, db_index=True, verbose_name='Порядок')
    super_rubric = models.ForeignKey('SuperRubric', on_delete=models.PROTECT, null=True, blank=True,
                                     verbose_name="Надрубрика")


class SuperRubricManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(super_rubric__isnull=True)


class SuperRubric(Rubric):
    objects = SuperRubricManager()

    def __str__(self):
        return self.name

    class Meta:
        proxy = True
        ordering = ('order', 'name')
        verbose_name = 'Надрубрика'
        verbose_name_plural = 'Надрубрики'


class SubRubricManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(super_rubric__isnull=False)


class SubRubric(Rubric):
    objects = SubRubricManager()

    def __str__(self):
        return '%s - %s' % (self.super_rubric.name, self.name)

    class Meta:
        proxy = True
        ordering = ('super_rubric__order', 'super_rubric__name', 'order', 'name')
        verbose_name = 'Подрубрика'
        verbose_name_plural = "Подрубрики"


class Bb(models.Model):
    rubric = models.ForeignKey(SubRubric, on_delete=models.PROTECT, verbose_name='Рубрика')
    title = models.CharField(max_length=40, verbose_name='Товар')
    content = models.TextField(verbose_name='Описание')
    price = models.FloatField(default=0, verbose_name='Цена')
    contacts = models.TextField(verbose_name="Контакты")
    image = models.ImageField(blank=True, upload_to=get_timestamp_path, verbose_name='Изображение')
    author = models.ForeignKey(AdvUser, on_delete=models.CASCADE, verbose_name='Автор обьявления')
    is_active = models.BooleanField(default=True, db_index=True, verbose_name='Выводить в списке')
    create_at = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Опубликованно')

    def delete(self, *args, **kwargs):
        for ai in self.additionalimage_set.all():
            ai.delete()
            super().delete(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Обьявления'
        verbose_name = "Обьявление"
        ordering = ['create_at']


class AdditionalImage(models.Model):
    bb = models.ForeignKey(Bb, on_delete=models.CASCADE, verbose_name='Обьявление')
    image = models.ImageField(upload_to=get_timestamp_path, verbose_name='Изображение')

    class Meta:
        verbose_name_plural = 'Дополнительные илюстрации'
        verbose_name = 'Дополнительная илюстрация'
