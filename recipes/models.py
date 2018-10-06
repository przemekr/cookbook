# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from markupfield.fields import MarkupField
import os.path
import md5
import uuid
from PIL import Image

class Recipe(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    descr = MarkupField()
    ingredient = MarkupField()
    steps = MarkupField()
    added = models.DateTimeField()

    def __str__(self):
        return ('Recipe: %s' % self.title).encode('ascii', errors='replace')

def picture_path(instance, filename):
    return 'recipe_{0}/img_{1}.{2}'.format(instance.recipe.id, md5.new(filename).hexdigest(), os.path.splitext(filename)[1])

def get_thumb_path(path):
    base, ext = os.path.splitext(path)
    return base+"_thumb"+ext

def get_small_path(path):
    base, ext = os.path.splitext(path)
    return base+"_small"+ext

def get_thumb_url(picture):
    if not picture:
        return "missing"
    return get_thumb_path(picture.upload.url)

def get_small_url(picture):
    if not picture:
        return "missing"
    return get_small_path(picture.upload.url)

class Picture(models.Model):
    upload = models.ImageField(upload_to=picture_path)
    recipe = models.ForeignKey(Recipe)

    def __str__(self):
        return ('Img: %s' % self.recipe.title).encode('ascii', errors='replace') + str(self.id)

    def save(self):
        super(Picture, self).save()

	tsize = 128, 128
	ssize = 480, 320
	tout = get_thumb_path(self.upload.path)
	sout = get_small_path(self.upload.path)
	im = Image.open(self.upload.path)
	im.thumbnail(ssize)
	im.save(sout, "JPEG")
	im.thumbnail(tsize)
	im.save(tout, "JPEG")

class Tag(models.Model):
    name = models.CharField(max_length=255)
    recipes = models.ManyToManyField(Recipe)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return ('Tag: %s' % self.name).encode('ascii', errors='replace')
