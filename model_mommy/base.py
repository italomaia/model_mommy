# -*- coding:utf-8 -*-

from django.db.models.fields import *
from django.db.models.fields.related import *
from django.db.models.fields.files import *

from random import randint, choice, random


MIN_INT, MAX_INT = -2147483648, 2147483647
MIN_BIG_INT, MAX_BIG_INT = -9223372036854775808l, 9223372036854775807l
MIN_SMALL_INT, MAX_SMALL_INT = -32768, 32767


def generate_string(length, char_table):
    return ''.join([choice(char_table) for i in range(size)])


class Base(object):

    def __init__(self, model):
        self.model = model

    def make(self, **attrs):
        return self._make(True, **attrs)

    def prepare(self, **attrs):
        return self._make(False, **attrs)

    def _make(self, commit, **attrs):
        for field in self.get_fields():
            if isinstance(field, AutoField):  # auto populated
                continue
            elif field.name in attrs:
                continue
            elif field.null:
                continue
            else:
                attrs[field.name] = self.get_value_for_field(field)

    def get_fields(self):
        return self.model._meta.fields + self.model._meta.many_to_many

    def get_value_for_field(self, field):
        field_cls = field.__class__
        field_cls_name = field_cls.__name__

        # get from avaiable choices
        if hasattr(field, 'choices'):
            return choice(map(lambda c: c[0], field.choices))
        # generate from class method
        elif hasattr(self, 'value_for_' + field_cls_name):
            return getattr(self, 'value_for_' + field_cls_name)(field)
        else:  # unsupported field type
            raise TypeError('%s is not supported by mommy.' % field_cls_name)

    def value_for_booleanfield(self, field):
        return choice((False, True))

    def value_for_nullbooleanfield(self, field):
        pass

    def value_for_smallintegerfield(self, field):
        return randint(MIN_SMALL_INT, MAX_SMALL_INT)

    def value_for_positivesmallintegerfield(self, field):
        return randint(0, MAX_SMALL_INT)

    def value_for_integerfield(self, field):
        return randint(MIN_INT, MAX_INT)

    def value_for_positiveintegerfield(self, field):
        return randint(0, MAX_INT)

    def value_for_bigintegerfield(self, field):
        return randint(MIN_BIG_INT, MAX_BIG_INT)

    def value_for_floatfield(self, field):
        return random() * randint(MIN_INT, MAX_INT)

    def value_for_decimalfield(self, field):
        md, dp = field.max_digits, field.decimal_places

    def value_for_commaseparatedintegerfield(self, field):
        pass

    def value_for_datefield(self, field):
        pass

    def value_for_timefield(self, field):
        pass

    def value_for_datetimefield(self, field):
        pass

    def value_for_charfield(self, field):
        max_length, blank = field.max_length, field.blank

    def value_for_slugfield(self, field):
        pass

    def value_for_textfield(self, field):
        pass

    def value_for_xmlfield(self, field):
        pass

    def value_for_filefield(self, field):
        pass

    def value_for_filepathfield(self, field):
        pass

    def value_for_imagefield(self, field):
        pass

    def value_for_urlfield(self, field):
        pass

    def value_for_emailfield(self, field):
        pass

    def value_for_foreignkey(self, field):
        pass

    def value_for_onetoonefield(self, field):
        pass

    def value_for_manytomanyfield(self, field):
        pass