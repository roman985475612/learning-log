from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse

def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]


class Topic(models.Model):
    owner = models.ForeignKey(User, on_delete=models.SET(get_sentinel_user))
    title = models.CharField(max_length=200, unique=True)
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
        return reverse('learning_logs:topic', kwargs={'slug': self.slug})


class Entry(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.PROTECT)
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(unique=True)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='learning_logs/img', default='', blank=True)
    views = models.IntegerField(default=0)

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

    def get_absolute_url(self):
        return reverse('learning_logs:entry', kwargs={'slug': self.slug})


class Comment(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now=True)

    def __str__(self):
        if len(self.text) < 40:
            return self.text
        else:
            return self.text[:40] + '...'

    def get_absolute_url(self):
        return reverse('learning_logs:entry', kwargs={'slug': self.entry.slug})
