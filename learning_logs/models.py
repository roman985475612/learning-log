from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse


class Topic(models.Model):
    owner = models.ForeignKey(User)
    title = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Topic, self).save(*args, **kwargs)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('learning_logs:topics')


class Entry(models.Model):
    owner = models.ForeignKey(User)
    topic = models.ForeignKey(Topic)
    title = models.CharField(max_length=200)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Entry, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'entries'

    def __str__(self):
        return self.title

    def text_short(self):
        if len(self.text) < 100:
            return self.text
        else:
            return self.text[:100] + '...'
