# -*- coding: utf-8 -*-

#######################################
# TESTING PURPOSE ONLY MODELS!!       #
# DO NOT ADD THE APP TO INSTALLED_APPS#
#######################################

from django.db import models
from django.db.models.fields import *
from django.db.models.fields.related import *
from django.db.models.fields.files import *

import django

if django.VERSION < (1, 2):
    BigIntegerField = IntegerField

GENDER_CH = [('M', 'male'), ('F', 'female')]


class Person(models.Model):
    gender = CharField(max_length=1, choices=GENDER_CH)
    happy = BooleanField(default=True)
    name = CharField(max_length=30)
    age = IntegerField()
    bio = TextField(null=True)
    birthday = DateField()
    appointment = DateTimeField()
    wanted_games_qtd = BigIntegerField()
    blog = URLField()
    email = EmailField()


class Dog(models.Model):
    owner = ForeignKey('Person')
    breed = CharField(max_length=50)


class Store(models.Model):
    customers = ManyToManyField(Person, related_name='favorite_stores',
        blank=True, null=True)
    employees = ManyToManyField(Person, related_name='employers')


class Penguin(models.Model):
    partner = OneToOneField('self')
    parcel = ManyToManyField('self')


class DummyDateModel(models.Model):
    date_field = DateField()


class DummyDateTimeModel(models.Model):
    datetime_field = DateTimeField()


class DummySlugModel(models.Model):
    slug_field = models.SlugField()


class DummyCharModel(models.Model):
    char_field = CharField(max_length=255)


class DummyTextModel(models.Model):
    text_field = TextField()


class DummyURLModel(models.Model):
    url_field = URLField()


class DummyEmailModel(models.Model):
    email_field = EmailField()


class DummyIntModel(models.Model):
    int_field = IntegerField()
    small_int_field = SmallIntegerField()
    big_int_field = BigIntegerField()


class DummyPositiveIntModel(models.Model):
    positive_small_int_field = PositiveSmallIntegerField()
    positive_int_field = PositiveIntegerField()


class DummyNumbersModel(models.Model):
    float_field = FloatField()


class DummyDecimalModel(models.Model):
    decimal_field = DecimalField(max_digits=5, decimal_places=2)


class DummyBooleanModel(models.Model):
    boolean_field = BooleanField()


class DummyFileModel(models.Model):
    file_field = FileField(upload_to='uploads')


class DummyImageModel(models.Model):
    image_field = FileField(upload_to='images')


class DummyRelationModel(models.Model):
    pass


class DummyOneToOneModel(models.Model):
    one_to_one_field = models.OneToOneField(DummyRelationModel)


class UnsupportedField(Field):
    description = "I'm bad company, mommy doesn't know me"

    def __init__(self, *args, **kwargs):
        super(UnsupportedField, self).__init__(*args, **kwargs)


class UnsupportedModel(models.Model):
    unsupported_field = UnsupportedField()
