from django.contrib.auth.models import User
from django.db import models


class Person(models.Model):
    MALE = 'male'
    FEMALE = 'female'
    SEX_CHOICES = (
        (MALE, 'male'),
        (FEMALE, 'female'),
    )
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='person')
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    sex = models.CharField(max_length=6, choices=SEX_CHOICES, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    home_page = models.URLField(null=True, blank=True)
    image = models.ImageField(upload_to='users/img', default='', blank=True)

    def __str__(self):
        return str(self.owner)
