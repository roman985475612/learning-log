from django.contrib.auth.models import User
from django.db import models
# from django.utils.text import slugify
from pytils.translit import slugify
from django.urls import reverse


class Tag(models.Model):
    PRIMARY = 'primary'
    SECONDARY = 'secondary'
    SUCCESS = 'success'
    INFO = 'info'
    WARNING = 'warning'
    DANGER = 'danger'
    LIGHT = 'light'
    DARK = 'dark'
    COLOR_CHOICES = (
        (PRIMARY, 'Blue'),
        (SECONDARY, 'Gray'),
        (SUCCESS, 'Green'),
        (INFO, 'Cyan'),
        (WARNING, 'Yellow'),
        (DANGER, 'Red'),
        (LIGHT, 'White'),
        (DARK, 'Black')
    )
    color = models.CharField(max_length=10, choices=COLOR_CHOICES, default=PRIMARY)
    title = models.CharField(max_length=30, unique=True)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Entry(models.Model):
    tag = models.ManyToManyField(Tag, default='', blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='entry')
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(unique=True)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='learning_logs/img', default='', blank=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    comments = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Entry, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'entries'
        ordering = ['title']

    def __str__(self):
        return self.title

    def text_short(self):
        if len(self.text) < 100:
            return self.text
        else:
            return self.text[:100] + '...'

    def get_absolute_url(self):
        return reverse('learning_logs:entry', kwargs={'slug': self.slug})


class LogLikedEntries(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE)
    is_liked = models.BooleanField(default=False)

    def __str__(self):
        return self.owner.username + ' ' + self.entry.title


class LogViewedEntries(models.Model):
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE)
    remote_addr = models.CharField(max_length=20)
    date_added = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment')
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date_added']

    def __str__(self):
        if len(self.text) < 40:
            return self.text
        else:
            return self.text[:40] + '...'

    def get_absolute_url(self):
        return reverse('learning_logs:entry', kwargs={'slug': self.entry.slug})
