from django.contrib.auth.models import User
from django.db import models


class Person(models.Model):
    MALE = 'M'
    FEMALE = 'F'
    SEX_CHOICES = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
    )
    owner = models.ForeignKey(User)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    sex = models.CharField(max_length=1, choices=SEX_CHOICES)
    birth_date = models.DateField()
    email = models.EmailField()
    home_page = models.URLField()
    about_me = models.TextField(blank=True)

    def __str__(self):
        return str(self.owner)