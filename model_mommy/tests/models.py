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


class Penguin(models.Model):  # a family animal...
    partner = OneToOneField('self', related_name='mate', null=True)
    parcel = ManyToManyField('self', related_name='fellows')


class Car(models.Model):
    COLOR_CHOICES = ((0, 'white'), (1, 'black'), (2, 'red'))
    color = IntegerField(default=0, choices=COLOR_CHOICES)
    accessories = CharField(max_length=100, blank=True)
    license_plate = CharField(max_length=10)


class DummyDateModel(models.Model):
    date_field = DateField()


class DummyDateTimeModel(models.Model):
    datetime_field = DateTimeField()


class DummyTimeModel(models.Model):
    time_field = TimeField()


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


class DummyCommaSeparatedIntegerModel(models.Model):
    comma_separated_integer_field = CommaSeparatedIntegerField(max_length=20)


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


class DummyNullBooleanModel(models.Model):
    null_boolean_field = NullBooleanField()


class DummyFileModel(models.Model):
    file_field = FileField(upload_to='uploads')


class DummyFilePathModel(models.Model):
    file_path_field = FilePathField(path='uploads')


class DummyImageModel(models.Model):
    image_field = ImageField(upload_to='images')


class DummyIPAddressFieldModel(models.Model):
    ip_address_field = IPAddressField()


class DummyRelationModel(models.Model):
    pass


class DummyOneToOneModel(models.Model):
    one_to_one_field = models.OneToOneField(DummyRelationModel)


class DummyForeignKeyModel(models.Model):
    foreignkey_field = models.ForeignKey(DummyRelationModel)


class DummyM2MModel(models.Model):
    m2m_field = models.ManyToManyField(DummyRelationModel,
        related_name='relation')


class UnsupportedField(Field):
    description = "I'm bad company, mommy doesn't know me"

    def __init__(self, *args, **kwargs):
        super(UnsupportedField, self).__init__(*args, **kwargs)


class UnsupportedModel(models.Model):
    unsupported_field = UnsupportedField()


class DummySelfReferenceModel(models.Model):
    one_to_one_field = models.OneToOneField('self', related_name='o2o_set', null=True)
    foreignkey_field = models.ForeignKey('self', related_name='fk_set', null=True)
    m2m_field = models.ManyToManyField('self', related_name='m2m_set', null=True)
