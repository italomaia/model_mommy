# -*- coding: utf-8 -*-

#######################################
# TESTING PURPOSE ONLY MODELS!!       #
# DO NOT ADD THE APP TO INSTALLED_APPS#
#######################################

from django.db import models

# fix for django <= 1.1
if not hasattr(models, 'BigIntegerField'):
    setattr(models, 'BigIntegerField', models.IntegerField)

GENDER_CH = [('M', 'male'), ('F', 'female')]


class Person(models.Model):
    gender = models.CharField(max_length=1, choices=GENDER_CH)
    happy = models.BooleanField(default=True)
    name = models.CharField(max_length=30)
    age = models.IntegerField()
    bio = models.TextField(null=True)
    birthday = models.DateField()
    appointment = models.DateTimeField()
    wanted_games_qtd = models.BigIntegerField()
    blog = models.URLField()
    email = models.EmailField()


class Dog(models.Model):
    owner = models.ForeignKey('Person')
    breed = models.CharField(max_length=50)


class Store(models.Model):
    customers = models.ManyToManyField(Person, related_name='favorite_stores',
        blank=True, null=True)
    employees = models.ManyToManyField(Person, related_name='employers')


class Penguin(models.Model):
    partner = models.OneToOneField('self')
    parcel = models.ManyToManyField('self')


class DummyDateModel(models.Model):
    date_field = models.DateField()


class DummyDateTimeModel(models.Model):
    datetime_field = models.DateTimeField()


class DummySlugModel(models.Model):
    slug_field = models.SlugField()


class DummyCharModel(models.Model):
    char_field = models.CharField(max_length=255)


class DummyTextModel(models.Model):
    text_field = models.TextField()


class DummyURLModel(models.Model):
    url_field = models.URLField()


class DummyEmailModel(models.Model):
    email_field = models.EmailField()


class DummyIntModel(models.Model):
    int_field = models.IntegerField()
    small_int_field = models.SmallIntegerField()
    big_int_field = models.BigIntegerField()


class DummyPositiveIntModel(models.Model):
    positive_small_int_field = models.PositiveSmallIntegerField()
    positive_int_field = models.PositiveIntegerField()


class DummyNumbersModel(models.Model):
    float_field = models.FloatField()


class DummyDecimalModel(models.Model):
    decimal_field = models.DecimalField(max_digits=5, decimal_places=2)


class DummyBooleanModel(models.Model):
    boolean_field = models.BooleanField()


class DummyFileModel(models.Model):
    file_field = models.FileField(upload_to='uploads')


class DummyImageModel(models.Model):
    image_field = models.FileField(upload_to='images')


class UnsupportedField(models.Field):
    description = "I'm bad company, mommy doesn't know me"
    def __init__(self, *args, **kwargs):
        super(UnsupportedField, self).__init__(*args, **kwargs)


class UnsupportedModel(models.Model):
    unsupported_field = UnsupportedField()
