from django.db import models
from django.contrib.auth.models import AbstractUser
from config.settings import MEDIA_URL, STATIC_URL

class User(AbstractUser):
    image = models.ImageField(upload_to='users/%Y/%m/',null=True, blank=True)
    
    def get_image(self):
        if self.image:
            return f'{MEDIA_URL}{self.image}'
        return f'{STATIC_URL}media/img/empty.png'