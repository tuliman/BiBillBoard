from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import Signal

from .utilities import send_activator_notification


class AdvUser(AbstractUser):
    is_active = models.BooleanField(default=True, db_index=True, verbose_name='Прошел валидацию')
    send_massages = models.BooleanField(default=True, verbose_name='Слать оповещения о новых коментариях')

    class Meta(AbstractUser.Meta):
        pass


user_registrated = Signal(providing_args=['instance'])


def user_registrated_dispatcher(sender, **kwargs):
    send_activator_notification(kwargs['instance'])


user_registrated.connect(user_registrated_dispatcher)
