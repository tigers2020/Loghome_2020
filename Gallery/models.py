import os
from datetime import datetime

from PIL.ExifTags import TAGS
from django.db import models
from ckeditor.fields import RichTextField
from PIL import Image
from django.utils.safestring import mark_safe
from sorl.thumbnail import ImageField, get_thumbnail
from django.conf import settings

# Create your models here.
from django.template.defaultfilters import slugify


class Location(models.Model):
    state_code = models.CharField(max_length=2)
    state_name = models.CharField(max_length=32)

    def __str__(self):
        return '[' + self.state_code + ']' + self.state_name

    class Meta:
        ordering = ["-state_name"]


class City(models.Model):
    id_state = models.ForeignKey(Location, on_delete=models.CASCADE)
    city = models.CharField(max_length=32)
    country = models.CharField(max_length=64)
    lat = models.FloatField()
    lng = models.FloatField()

    def __str__(self):
        return '%s, %s - %s[%s]' % (self.city, self.country, self.id_state.state_name, self.id_state.state_code)


class Provider(models.Model):
    name = models.CharField(max_length=64)
    homepage = models.URLField()
    phone_number = models.CharField(max_length=12)

    def __str__(self):
        return self.name


class Project(models.Model):
    title = models.CharField(max_length=64)
    slug = models.SlugField(blank=True, null=True)
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    location = models.ForeignKey(City, on_delete=models.CASCADE)
    project_date = models.DateTimeField()
    status = models.IntegerField(choices=settings.STATUS, default=0)
    h_first_floor_sq_ft = models.FloatField(default=0)
    h_second_floor_sq_ft = models.FloatField(default=0)
    h_bedrooms = models.FloatField(default=0)
    h_baths = models.FloatField(default=0)
    h_stories = models.IntegerField(default=0)
    h_roof_pitch = models.CharField(max_length=8)
    h_roof_system = models.CharField(max_length=16)
    h_price = models.FloatField(default=0)
    description = RichTextField()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Project, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-project_date']

    def __str__(self):
        return self.title


def get_image_location(instance, filename):
    year = instance.date_taken.year
    return os.path.join(str(year), instance.project.location.id_state.state_code, filename)


class HomeImage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    image = ImageField(upload_to=get_image_location, verbose_name='Image')
    date_taken = models.DateTimeField(blank=True, editable=False)
    description = RichTextField(blank=True, null=True)
    status = models.IntegerField(choices=settings.STATUS, default=0)

    def __str__(self):
        return '{} - {}'.format(str(self.date_taken), self.get_title())

    def get_title(self):
        return self.project.location.id_state.state_name + " - " + self.image.name

    def image_tag(self):
        im = get_thumbnail(self.image, '250x125', crop='center')
        return mark_safe('<img src="%s" with=250px />' % im.url)

    def save(self, *args, **kwargs):
        if self.date_taken is None or self.date_taken == "":
            image_exif = get_exif(self.image)
            if "DateTimeOriginal" in image_exif:
                date_taken = datetime.strptime(image_exif['DateTimeOriginal'], '%Y:%m:%d %H:%M:%S')
            elif "DateTimeDigitized" in image_exif:
                date_taken = datetime.strptime(image_exif['DateTimeDigitized'], '%Y:%m:%d %H:%M:%S')
            else:
                date_taken = datetime.now()
            self.date_taken = date_taken

        super(HomeImage, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-date_taken']


def get_exif(fn):
    ret = {}
    i = Image.open(fn)
    info = i._getexif()
    for tag, value in info.items():
        decoded = TAGS.get(tag, tag)
        ret[decoded] = value
    return ret
