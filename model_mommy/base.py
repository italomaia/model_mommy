# -*- coding:utf-8 -*-

from django.db.models.fields import *
from django.db.models.fields.related import *
from django.db.models.fields.files import *

from .utils import *

import datetime
from random import random

# ref: http://docs.python.org/howto/unicode.html
UNICODE_RANGE = (0, 1114111)
LATIN1_RANGE = (0, 255)
ASCII_RANGE = (0, 127)

LATIN1_TABLE = u''.join([unichr(i) for i in range(256)])
ASCII_TABLE = LATIN1_TABLE[:128]
SLUG_TABLE = string.ascii_lowercase + string.digits + "-_"

LEAVE_TO_CHANCE = (True, False, False)
TEXT_MAX_LENGTH = 500
MIN_INT, MAX_INT = -2147483648, 2147483647
MIN_BIG_INT, MAX_BIG_INT = -9223372036854775808l, 9223372036854775807l
MIN_SMALL_INT, MAX_SMALL_INT = -32768, 32767


class Base(object):

    def __init__(self, model):
        self.model = model

    def make(self, **attrs):
        """
        Makes one instance of the registered model. (commits instance)

        """
        return self.__make(True, **attrs)

    def prepare(self, **attrs):
        """
        Prepares one instance of the registered model. (does not commit instance)

        """
        return self.__make(False, **attrs)

    def get_fields(self):
        """
        Returns all available fields (regular fields plus m2m fields)

        """
        return self.model._meta.fields + self.model._meta.many_to_many

    def __make(self, commit, **attrs):
        for field in self.get_fields():
            # field value was provided. Ignoring...
            if field.name in attrs:
                continue
            elif type(field) in (OneToOneField, ForeignKey, ManyToManyField) and field.null:
                continue
            elif field.null and choice(LEAVE_TO_CHANCE):
                continue
            elif field.blank and choice(LEAVE_TO_CHANCE):
                attrs[field.name] = ''
            else:
                attrs[field.name] = self.__get_value_for_field(field)

    def __get_value_for_field(self, field):
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

    def value_for_autofield(self, field):
        return None

    def value_for_booleanfield(self, field):
        """
        Returns True or False

        """
        return choice((False, True))

    def value_for_nullbooleanfield(self, field):
        """
        Returns None, True or False

        """
        return choice((None, False, True))

    def value_for_smallintegerfield(self, field):
        return randint(MIN_SMALL_INT, MAX_SMALL_INT)

    def value_for_positivesmallintegerfield(self, field):
        """
        Returns a positive 16bits integer

        >>> field = object()
        >>> base = Base({})
        >>> value = base.value_for_positivesmallintegerfield(field)
        >>> assert value >= 0
        """
        return randint(0, MAX_SMALL_INT)

    def value_for_integerfield(self, field):
        return randint(MIN_INT, MAX_INT)

    def value_for_positiveintegerfield(self, field):
        """
        Returns a positive 32bits integer

        >>> field = object()
        >>> base = Base({})
        >>> value = base.value_for_positiveintegerfield(field)
        >>> assert value >= 0
        """
        return randint(0, MAX_INT)

    def value_for_bigintegerfield(self, field):
        return randint(MIN_BIG_INT, MAX_BIG_INT)

    def value_for_floatfield(self, field):
        """
        Returns a random float value

        >>> field = object()
        >>> base = Base({})
        >>> value = base.value_for_floatfield(field)
        >>>
        >>> assert isinstance(value, float)
        """
        return random() * randint(MIN_INT, MAX_INT)

    def value_for_decimalfield(self, field):
        """
        Returns a random decimal like string obeying field's max_digits and decimal_places

        >>> field = object()
        >>> field.max_digits = 10
        >>> field.decimal_places = 2
        >>> base = Base({})
        >>> value = base.value_for_decimalfield(field)
        >>> dec, frac = value.split(".")
        >>>
        >>> assert len(dec) + len(frac) <= field.max_digits
        >>> assert len(frac) <= field.decimal_places
        >>> assert dec.isdigit() or frac.isdigit()
        """
        md, dp = field.max_digits, field.decimal_places
        dp_length = randint(0, dp)
        md_length = md - dp_length
        md_number = ''.join([randint(0, 9) for i in range(md_length)])
        dp_number = ''.join([randint(0, 9) for i in range(dp_length)])
        return "%s.%s" % (md_number, dp_number)

    def value_for_commaseparatedintegerfield(self, field):
        """
        Returns string in the format number[,number]*
        *number* is a 32bits integer

        >>> import re
        >>> c = re.compile('^\d+(m\d+)$')
        >>> field = object()
        >>> field.max_length = 10
        >>> base = Base({})
        >>> value = base.value_for_commaseparatedintegerfield(field)
        >>>
        >>> assert c.match(value) is not None
        >>> assert len(value) <= field.max_value
        """
        max_length = field.max_length

        number = randint(MIN_INT, MAX_INT)
        str_number = str(number)

        rt = str(int(str_number[min(len(str_number), max_length):]))

        while (len(rt) < max_length - 1) and choice(True, True, False):
            number = randint(MIN_INT, MAX_INT)
            str_number = str(number)

            rt += ","
            rt += str(int(str_number[min(len(str_number), max_length - len(rt)):]))

        return rt

    def value_for_datefield(self, field):
        """
        Returns a datetime.date object for the current time

        """
        return datetime.today()

    def value_for_timefield(self, field):
        """
        Returns a datetime.datetime object for the current time

        """
        return datetime.now()

    def value_for_datetimefield(self, field):
        """
        Returns a datetime.datetime object for the current time

        """
        return datetime.now()

    def value_for_ipaddressfield(self, field):
        '''
        Generates a valid IPV4 for IPAddress

        Does not produce the following ip addresses:
        ref: http://www.comptechdoc.org/independent/networking/guide/netaddressing.html
        - 0.0.0.0 - reserved for hosts
        - 0.x.x.x - class A network can't be zero
        - x.x.x.0 - host ip can't be 0
        - 255.x.x.x or x.255.x.x or x.x.255.x or x.x.x.255 - no network address can be 255/ broadcast address
        - 10.x.x.x - private use for IANA
        - 192.168.x.x - private use for IANA
        - 172.16.0.0 to 172.31.255.255 - private use for IANA

        '''
        ip_address = None

        while True:
            ip_address = (
                randint(1, 254), randint(0, 254),
                randint(0, 254), randint(1, 254))

            if (ip_address[0] == 10) or\
               (ip_address[0] == 192 and ip_address[1] == 168) or\
               (ip_address >= (172, 16, 0, 0) and ip_address <= (172, 31, 255, 255)):
                continue
            else:
                break
        return '.'.join([str(token) for token in ip_address])

    def value_for_charfield(self, field):
        """
        Creates a random string with provided max_length

        """
        max_length = field.max_length
        length = randint(1, max_length)
        return raw_string(length, UNICODE_RANGE)

    def value_for_slugfield(self, field):
        """
        Creates a random slug field with provided max_length

        """
        max_length = field.max_length
        length = randint(1, max_length)
        return raw_string(length, SLUG_TABLE)

    def value_for_textfield(self, field):
        length = randint(1, TEXT_MAX_LENGTH)
        return raw_string(length, UNICODE_RANGE + "\n")

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