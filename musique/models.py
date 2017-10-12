import os
from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.utils.text import slugify

class SongArtist(models.Model):
	slug = models.SlugField(max_length=40, unique=True)
	name = models.CharField(max_length=100)
	country = models.CharField(max_length=50, null=True, blank=True)
	popularity = models.IntegerField(default=0)

	def save(self, *args, **kwargs):
		if not self.id:
			self.slug = slugify(self.name)
		super(SongArtist, self).save(*args, **kwargs)

class Genre(models.Model):
	slug = models.SlugField(max_length=40, unique=True)
	name = models.CharField(max_length=100)

	def save(self, *args, **kwargs):
		if not self.id:
			self.slug = slugify(self.name)
		super(SongArtist, self).save(*args, **kwargs)

class SongAlbum(models.Model):
	slug = models.SlugField(max_length=40, unique=True)
	artist = models.ForeignKey(SongArtist)
	name = models.CharField(max_length=250, unique=True)
	release_date = models.DateTimeField(null=True, blank=True)
	genre = models.ManyToManyField(Genre)
	logo = models.FileField()
	popularity = models.IntegerField(default=0)
	rating = models.IntegerField(default=0)

	def __str__(self):
		return self.title

	def save(self, *args, **kwargs):
		if not self.id:
			self.slug = slugify(self.name)
		super(SongAlbum, self).save(*args, **kwargs)

class Song(models.Model):
	slug = models.SlugField(max_length=40, unique=True)
	name = models.CharField(max_length=250)
	album = models.ForeignKey(SongAlbum, on_delete=models.CASCADE)
	genre = models.ManyToManyField(Genre)
	likes = models.IntegerField(default=0)
	times_played = models.IntegerField(default=0)

	def __str__(self):
		return self.name

	def save(self, *args, **kwargs):
		if not self.id:
			self.slug = slugify(self.name)
		super(Song, self).save(*args, **kwargs)

class SongUpload(models.Model):
	song = models.ForeignKey(Song, null=True)
	uploader = models.ForeignKey(User, on_delete=models.CASCADE)
	file = models.FileField()
	no_of_downloads = models.CharField(max_length=5, default='0')

	def extension(self):
		fname, extension = os.path.splitext(self.file.name)
		return extension

class SongReview(models.Model):
	song = models.ForeignKey(Song, on_delete=models.CASCADE, null=True)
	reviewer = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
	review = models.TextField(max_length=1000)
	createdAt = models.DateTimeField(null=True, blank=True)
	updatedAt = models.DateTimeField(auto_now = True, null=True, blank=True)
	deletedAt = models.DateTimeField(null=True, blank=True)

	def __str__(self):
		return self.review

	def save(self, *args, **kwargs):
		if not self.createdAt:
			self.createdAt = timezone.now()

		self.updatedAt = timezone.now()
		return super(Review, self).save(*args, **kwargs)