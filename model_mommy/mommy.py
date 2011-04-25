# -*- coding:utf-8 -*-

from string import letters
from random import choice, randint
from datetime import date
from decimal import Decimal
import sys

from django.db.models.fields import *
from django.db.models.fields.related import *
from django.db.models.fields.files import *
import django

if django.VERSION < (1, 2):
    BigIntegerField = IntegerField

import generators


#TODO: improve related models handling
foreign_key_required = [lambda field: ('model', field.related.parent_model)]


def make_one(model, **attrs):
    """
    Creates a persisted instance from a given model its associated models.
    It fill the fields with random values or you can specify
    which fields you want to define its values by yourself.
    """
    mommy = Mommy(model)
    return mommy.make_one(**attrs)


def prepare_one(model, **attrs):
    """
    Creates a BUT DOESN'T persist an instance from a given model
    its associated models.
    It fill the fields with random values or you can specify
    which fields you want to define its values by yourself.
    """
    mommy = Mommy(model)
    return mommy.prepare(**attrs)


def make_many(model, qty=5, **attrs):
    mommy = Mommy(model)
    return [mommy.make_one() for i in range(qty)]


def prepare_many(model, qty=5, **attrs):
    mommy = Mommy(model)
    return [mommy.prepare() for i in range(qty)]


make_one.required = foreign_key_required
prepare_one.required = foreign_key_required
make_many.required = foreign_key_required
prepare_many.required = foreign_key_required


default_mapping = {
    BooleanField: generators.gen_boolean,
    BigIntegerField: generators.gen_big_integer,
    IntegerField: generators.gen_integer,
    SmallIntegerField: generators.gen_small_integer,

    PositiveIntegerField: generators.gen_positive_integer,
    PositiveSmallIntegerField: generators.gen_positive_small_integer,

    FloatField: generators.gen_float,
    DecimalField: generators.gen_decimal,

    SlugField: generators.gen_slug,
    CharField: generators.gen_string,
    TextField: generators.gen_text,

    ForeignKey: make_one,
    OneToOneField: make_one,
    ManyToManyField: prepare_many,

    DateField: generators.gen_date,
    DateTimeField: generators.gen_date,

    URLField: generators.gen_url,
    EmailField: generators.gen_email,

    FileField: generators.gen_filename,
}


class Mommy(object):
    attr_mapping = {}
    type_mapping = None

    def __init__(self, model, fill_nullables=False):
        '''Set fill_nullables to False if you want fields that can receive
        null values to be left blank by default. You can still overwrite
        nullable fields manually.'''

        self.type_mapping = default_mapping.copy()
        self.model = model
        self.fill_nullables = fill_nullables

    def make_one(self, **attrs):
        '''Creates and persists an instance of the model
        associated with Mommy.'''

        return self._make_one(commit=True, **attrs)

    def prepare(self, **attrs):
        '''Creates, but does not persists, an instance of the model
        associated with Mommy.'''
        self.type_mapping[ForeignKey] = prepare_one
        return self._make_one(commit=False, **attrs)

    def get_fields(self):
        return self.model._meta.fields + self.model._meta.many_to_many

    def _make_one(self, commit=True, **attrs):
        '''
        Attributes:
        - attrs - dictionary of attributes that should be manually filled
        - commit - should created model instance be persisted in the database?

        Each field not informed in attrs is resolved like this:
        * If field is a reference to its own model, field is left blank.
        * If field accepts null and fill_nullables is False, field is left blank.
        * All other cases, a random value is created for the field.
        '''
        m2m_dict = {}  # dict of m2m fields for current model

        for field in self.get_fields():
            if isinstance(field, AutoField):  # auto populated
                continue
            elif field.name in attrs:
                if isinstance(field, ManyToManyField):
                    m2m_dict[field.name] = attrs.pop(field.name)
            else:
                if type(field) in (ForeignKey, OneToOneField, ManyToManyField) and (field.related.parent_model == self.model) and field.null:
                    continue
                elif field.null and not self.fill_nullables:  # leave blank?
                    continue
                elif isinstance(field, ManyToManyField):
                    m2m_dict[field.name] = self.generate_value(field)
                else:
                    attrs[field.name] = self.generate_value(field)

        instance = self.model(**attrs)

        if commit:
            instance.save()

            # m2m relations can only be created if the model is persisted
            for name, value in m2m_dict.items():
                m2m_relation = getattr(instance, name)

                for model_instance in value:
                    model_instance.save()
                    m2m_relation.add(model_instance)

        return instance

    def generate_value(self, field):
        '''Calls the generator associated with a field passing all
        required args.

        Generator Resolution Precedence Order:
        -- attr_mapping - mapping per attribute name
        -- choices -- mapping from avaiable field choices
        -- type_mapping - mapping from user defined type associated
        generators
        -- default_mapping - mapping from pre-defined type associated
        generators

        `attr_mapping` and `type_mapping` can be defined easely
        overwriting the model.
        '''
        if field.name in self.attr_mapping:  # manual mapping
            generator = self.attr_mapping[field.name]
        elif getattr(field, 'choices'):  # from code choices
            generator = generators.gen_from_choices(field.choices)
        elif field.__class__ in self.type_mapping:  # from type
            generator = self.type_mapping[field.__class__]
        else:
            raise TypeError('%s is not supported by mommy.' % field.__class__)

        required_fields = get_required_values(generator, field)
        return generator(**required_fields)


def get_required_values(generator, field):
    '''
    Gets required values for a generator from the field.
    If required value is a function, call's it with field as argument.
    If required value is a string, simply fetch the value from the field
    and returns.
    '''
    rt = {}
    if hasattr(generator, 'required'):
        for item in generator.required:

            if callable(item):  # mommy can deal with the nasty hacking too!
                key, value = item(field)
                rt[key] = value

            elif isinstance(item, basestring):
                rt[item] = getattr(field, item)
            else:
                raise ValueError("Required value '%s'"
                " is of wrong type. Don't make mommy sad." % str(item))
    return rt
