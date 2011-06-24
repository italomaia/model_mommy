# -*- coding:utf-8 -*-

__doc__ = """
Generators are callables that return a value used to populate a field.

If this callable has a `required` attribute (a list, mostly), for each item in
the list, if the item is a string, the field attribute with the same name will
be fetched from the field and used as argument for the generator. If it is a
callable (which will receive `field` as first argument), it should return a
list in the format (key, value) where key is the argument name for generator
and value is the value for that argument.
"""

import re
import sys
import string
import datetime

from decimal import Decimal
from random import randint, choice, random

from . import utils

MIN_INT, MAX_INT = -2147483648, 2147483647
MIN_BIG_INT, MAX_BIG_INT = -9223372036854775808l, 9223372036854775807l
MIN_SMALL_INT, MAX_SMALL_INT = -32768, 32767

TEXT_LENGTH = 300

DOMAIN_EXT_LIST = (
    '.com', '.co', '.info', '.net', '.org', '.me', '.mobi', '.us',
    '.biz', '.mx', '.ca', '.ws', '.ag', '.com.co', '.net.co', '.nom.co',
    '.com.ag', '.net.ag', '.it', '.fr', '.org.ag', '.am', '.asia',
    '.at', '.be', '.bz', '.se', '.com.bz', '.net.bz', '.net.br', '.vg',
    '.com.br', '.cc', '.de', '.es', '.com.es', '.nom.es', '.org.es',
    '.eu', '.fm', '.gs', '.in', '.co.in', '.firm.in', '.gen.in', '.tv',
    '.ind.in', '.net.in', '.org.in', '.jobs', '.jp', '.ms', '.com.mx',
    '.nl', '.nu', '.co.nz', '.net.nz', '.org.nz', '.tc', '.tk',
    '.tw', '.com.tw', '.idv.tw', '.co.uk', '.me.uk', '.org.uk'
)


class Mapper(object):
    ''''''
    fields = property(get_fields)

    def __init__(self, fill_nullable=False, use_default=False):
        '''
        Keyword arguments:
        -- fill_nullable - If True, all fields with null=True will receive value.
        -- use_default - If True, all fields with default value defined
        will be filled from default value.

        '''
        self.fill_nullable = fill_nullable
        self.use_default = use_default

    def value_from_choices(self, field):
        '''
        Returns a value from one of the possible values defined in
        field.choices.
        '''
        return choice(map(lambda c: c[0], field.choices))

    def value_for_ipaddressfield(self, field):
        '''
        Generates a valid IPV4 for IPAddress

        Not allowed:
        - [0] 10.x.x.x
        - [1] 192.168.x.x
        - [2] 172.16.0.0 to 172.31.255.255

        '''
        ip_address = None

        while True:
            ip_address = [
                randint(0, 255), randint(0, 255),
                randint(0, 255), randint(0, 255)]

            if (ip_address[0] == 10) or\
                (ip_address[0] == 192 and ip_address[1] == 168) or\
                (ip_address >= [172, 16, 0, 0] and ip_address <= [172, 31, 255, 255]):
                continue
            else:
                break

        return '.'.join(ip_address)

    def value_for_integerfield(self, min=MIN_INT, max=MAX_INT):
        '''
        Creates a random 32bits integer.

        '''
        return randint(min, max)

    def value_for_positiveintegerfield(self, min=0, max=MAX_INT * 2 + 1):
        '''
        Creates a random 32bits integer.

        '''
        return randint(min, max)

    def value_for_smallintegerfield(self, min=MIN_SMALL_INT, max=MAX_SMALL_INT):
        '''
        Creates a random 16bits integer.

        '''
        return randint(min, max)

    def value_for_positivesmallintegerfield(self, min=0, max=MAX_SMALL_INT * 2 + 1):
        '''
        Creates a random 16bits integer.

        '''
        return randint(min, max)

    def value_for_bigintegerfield(self, min=MIN_BIG_INT, max=MAX_BIG_INT):
        '''
        Creates a random 64bits integer.

        '''
        return randint(min, max)

    def value_for_decimalfield(self, field):
        '''
        Creates a random decimal field obeying field decimal_places and
        max_digits constrains.

        '''
        max_digits, decimal_places =\
            field.max_digits, field.decimal_places

        num_as_str = lambda max_length: utils.raw_string(
            ranint(1, max_length), string.digits)

        return Decimal('%s.%s' % (
            num_as_str(max_digits-decimal_places),
            num_as_str(decimal_places)))

    def value_for_commaseparatedintegerfield(self, field):
        '''
        Returns a string of comma separated integers.

        '''
        char_table = ',0123456789'
        length = randint(1, field.max_length or 20)

        num = randint(MIN_INT, MAX_INT)
        str_num = str(num)

        while len(str_num) > length:
            num = num >> 1
            str_num = str(num)

        comma_int = str_num  # first number in the list
        while len(comma_int) < length - 1:
            num = randint(MIN_INT, MAX_INT)
            str_num = str(num)

            while len(comma_int) + ',' + len(str_num) > length:
                num = num >> 1
                str_num = str(num)

            comma_int += ',' + len(str_num)

        return comma_int

    def value_for_floatfield(self, field):
        '''
        Creates a random float value.

        '''
        return random() * self.gen_integer()

    def value_for_datefield(self, field):
        '''
        Creates a date value with the current date.

        '''
        return datetime.date.today()

    def value_for_timefield(self, field):
        raise Exception('Not implemented')

    def value_for_datetimefield(self, field):
        '''
        Creates a datetime value with the current time.

        '''
        return datetime.datetime.now()

    def value_for_slugfield(self, field):
        '''
        Creates a random size slug string with length up to
        field.max_length.

        '''
        char_table = string.letters + string.digits + '-_'
        return utils.raw_string(randint(1, field.max_length), char_table)

    def value_for_charfield(self, field):
        '''
        Creates a random size string with length up to field.max_length.

        '''
        return utils.raw_string(
            randint(1, field.max_length), string.printable)

    def value_for_textfield(self, field):
        '''
        Creates a random size string with length up to MAX_LENGTH.

        '''
        return utils.raw_string(
            randint(1, MAX_LENGTH), string.printable)

    def value_for_xmlfield(self, field):
        raise Exception('Not implemented')

    def value_for_urlfield(self, field):
        '''
        Creates a random size url string in the
        format 'http://[domain].[ext]'

        '''
        assert field.max_length > 16, 'max_length is too small'

        length = randint(9, field.max_length - 7)
        return 'http://%s' % Mapper.raw_domain(length)

    def value_for_emailfield(self, field):
        '''
        Creates a valid email string according to
        http://en.wikipedia.org/wiki/Email_address

        '''
        assert field.max_length > 11, 'max length is too small'
        assert field.max_length < 255, 'max length is too big'

        max_length = min(field.max_length, 254) - 1  # -> @
        local_length = randint(1, min(64, max_length - 9))
        domain_length = randint(9, max_length - local_length)

        def gen_local_part(length):
            char_table_cc = string.letters + string.digits + "!#$%&'*+-/=?^_`{|}~"
            char_table_nc = string.letters + string.digits + "!#$%&'*+-/=?^_`{|}~."

            data = utils.raw_string(1, char_table_cc)
            while len(data) < length:
                if data[-1] == '.' or len(data) + 1 == length:
                    data += utils.raw_string(1, char_table_cc)
                else:
                    data += utils.raw_string(1, char_table_nc)
            return data

        return '%s@%s' % (
            gen_local_part(local_length),
            utils.raw_domain(domain_length))

    def value_for_imagefield(self, field):
        '''
        Creates a filename with a image extension.

        '''
        ext_list = ('.jpg', '.png', '.gif')
        return utils.raw_filename(field.max_length, ext_list)

    def value_for_filefield(self, field):
        '''
        Creates a filename with a document extension.

        '''
        ext_list = ('.txt', '.odt', '.pdf')
        return utils.raw_filename(field.max_length, ext_list)

    def value_for_filepathfield(self, field):
        raise Exception('Not implemented')

    def value_for_booleanfield(self, field):
        '''
        Generates a random True or False value.

        '''
        return choice((True, False))

    def value_for_nullbooleanfield(self, field):
        '''
        Generates a random None, True or False value.

        '''
        return choice((None, True, False))

    def value_for_foreignkey(self, field):
        field_model = field.related.parent_model
        return Mapper(field_model).make_one()

    def make_one(self, model, attrs=None, m2m_attrs=None, commit=True):  # TODO
        attrs = attrs or {}
        m2m_attrs = m2m_attrs or {}

        for field in self.get_fields(model):
            if field.name not in attrs:
                attrs[field.name] = self.resolve(field)

        for field in self.get_m2m_fields(model):
            if field.name not in m2m_attrs:
                m2m_attrs[field.name] = self.resolve(field)

        instance = model(**attrs)
        if commit:
            instance.save()
            if m2m_attrs:  # m2m only for persisted instances
                for name, value in m2m_attrs.items():
                    m2m_relation = getattr(instance, name)
                    for m2m_instance in value:
                        m2m_instance.save()
                        m2m_relation.add(m2m_instance)
        return instance

    def get_fields(self, model):
        '''Returns a mapped dict with all non m2m fields from the model'''
        return model._meta.fields

    def get_m2m_fields(self, model):
        '''Returns a mapped dict with all manytomany fields from the model'''
        return model._meta.many_to_many

    def resolve(self, field):
        '''
        Finds out which method is mapped for a given field.
        Order: null -> default -> choices -> name -> type -> unsupported

        '''
        name = field.name
        class_name = field.__class__.__name__.lower()

        if field.null and not self.fill_nullable:
            return None

        elif field.has_default() and self.use_default:
            return self.default

        elif field.choices:
            return self.value_from_choices(field)

        else:
            # check for field_name
            if hasattr(self, 'value_for_%s' % name):
                return getattr('value_for_%s' % name)(field)

            # check for class_name
            elif hasattr(self, 'value_for_%s' % class_name):
                return getattr('value_for_%s' % class_name)(field)

            else:  # type not supported
                raise TypeError('%s is not supported by mommy.' % field.__class__)

