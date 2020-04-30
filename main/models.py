from django.db import models
from django.contrib.auth.models import AbstractUser


class AdvUser(AbstractUser):
    is_active = models.BooleanField(default=True,db_index=True,verbose_name='Прошел валидацию')
    send_massages = models.BooleanField(default=True,verbose_name='Слать оповещения о новых коментариях')

    class Meta(AbstractUser.Meta):
        pass

