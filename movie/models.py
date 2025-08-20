from django.db import models
from actor.models import Actor

from django.utils.text import slugify
import requests
from io import BytesIO
from django.core import files
from django.urls import reverse

from django.contrib.auth.models import User
# Create your models here.

class Genre(models.Model):
	title = models.CharField(max_length=25)
	slug = models.SlugField(null=False, unique=True)

	def get_absolute_url(self):
		return reverse('genres', args=[self.slug])

	def __str__(self):
		return self.title

	def save(self, *args, **kwargs):
		if not self.slug:
			self.title.replace(" ", "")
			self.slug = slugify(self.title)
		return super().save(*args, **kwargs)


	def __str__(self):
		return self.Title







