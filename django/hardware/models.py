from django.db import models

# Create your models here.

class Item(models.Model):
	name = models.CharField(max_length=255)
	price = models.PositiveIntegerField()
	date = models.DateField()
	username = models.CharField(max_length=255)

	class Meta:
		verbose_name_plural = "items"

	def __str__(self):
		return self.name

class User(models.Model):
	username = models.CharField(max_length=255)
	numTrades = models.PositiveIntegerField()

	class Meta:
		verbose_name_plural = "users"
	def __str__(self):
		return self.username

class Manufacturer(models.Model):
	mID = models.PositiveIntegerField()
	mName = models.CharField(max_length=255)
	class Meta:
		verbose_name_plural = "manufacturers"
	def __str__(self):
		return self.mName

class Search(models.Model):
	query = models.CharField(max_length=255)
	class Meta:
		verbose_name_plural = "searches"
	def __str__(self):
		return self.query