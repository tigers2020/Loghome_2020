from django.utils import timezone

from django.contrib.auth.models import User
from django.db import models
from ckeditor.fields import RichTextField
from django.utils.safestring import mark_safe
from django.conf import settings

from hitcount.models import HitCountMixin, HitCount
from django.contrib.contenttypes.fields import GenericRelation

# Create your models here.
from django.utils.text import slugify


class Category(models.Model):
    parent_id = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    slug = models.SlugField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Post(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=255)
    slug = models.SlugField(null=True, blank=True)
    content = RichTextField()
    status = models.IntegerField(choices=settings.STATUS, default=5)
    create_time = models.DateTimeField(editable=False)
    update_time = models.DateTimeField()
    images = models.ImageField(blank=True, null=True)
    hit_count = GenericRelation(HitCount, object_id_field='object_pk', related_query_name='hit_count_relation')

    def save(self, *args, **kwargs):
        if not self.id:
            self.create_time = timezone.now()
        self.update_time = timezone.now()
        if not self.slug:
            self.slug = slugify(self.title)

        return super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-create_time']
