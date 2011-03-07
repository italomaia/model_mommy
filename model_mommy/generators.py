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

MAX_LENGTH = 300
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

    @staticmethod
    def raw_string(length, table):
        '''
        Creates a random string with length equal to `length` using
        only characters from `table`

        >>> import string
        >>> output = raw_string(20, string.letters)
        >>> assert len(output) == 20
        >>> assert all(map(lambda c: c in string.letters, output))

        '''
        return u''.join([choice(table) for
            i in range(length)])

    @staticmethod
    def raw_filename(length, ext_list):
        '''
        Creates a random filename with length up to `max_length`
        and one of the given extensions. Make sure the biggest extension
        length is smaller than `length`.

        Keyword arguments:
        -- length - len(name) + len(ext) == length
        -- ext_list - list of valid extensions.

        >>> from os import path
        >>> ext_list = ('.doc', '.pdf')
        >>> filename = raw_filename(20, ext_list)
        >>> name, ext = path.splitext(filename)
        >>> assert ext in ext_list

        '''
        char_table = re.sub(r'[/\?%*:|"<>]', '', string.printable)
        ext = '.%s' % choice(ext_list)
        name = self.raw_string(max_length - len(ext), char_table)
        return name + ext

    def raw_hostname(self, length):
        '''
        Creates a hostname with length equal to informed length.

        '''
        assert length > 0, 'length is too small'
        assert length < 64, 'length is too big'

        char_table = string.ascii_letters + string.digits
        char_table_ = string.ascii_letters + string.digits + '-'
        hostname = ''
        while len(hostname) < length:
            if len(hostname) == 0 or len(hostname) == length - 1:
                hostname += choice(char_table)
            else:
                hostname += choice(char_table_)
        return hostname

    def raw_domain(self, length, domain_ext_list=None):
        '''
        Creates a random valid domain name with one of the extensions
        informed in domain_ext_list. If not informed, an extension from
        DOMAIN_EXT_LIST is used. Values of ext_list should begin with
        a dot.
        Resulted domain length is between length and length - 1.

        '''
        assert length < 256, 'length is too big'
        ext_list = domain_ext_list or DOMAIN_EXT_LIST
        ext = choice(ext_list)
        length -= len(ext)

        hostnames = []
        while length > 1:
            newhost_length = randint(1, min(63, length))
            length = length - newhost_length - 1
            hostnames.append(self.raw_hostname(newhost_length))
        return '.'.join(hostnames) + ext

    def __init__(self, fill_null=True, use_default=False):
        '''
        Keyword arguments:
        -- fill_null - If False, all fields with null=True will receive None.
        -- use_default - If True, all fields with default value defined
        will be filled from default value.

        '''
        self.fill_null = fill_null
        self.use_default = use_default

    def value_from_choices(self, field):
        '''
        Returns a value from one of the possible values defined in
        field.choices.
        '''
        return choice(map(lambda c: c[0], field.choices))

    def value_for_integerfield(self, min=-2147483647, max=2147483647):
        '''
        Creates a random 32bits integer.

        '''
        return randint(min, max)

    def value_for_smallintegerfield(self, min=-32768, max=32768):
        '''
        Creates a random 16bits integer.

        '''
        return randint(min, max)

    def value_for_decimalfield(self, field):
        '''
        Creates a random decimal field obeying field decimal_places and
        max_digits constrains.
        
        '''
        max_digits, decimal_places =\
            field.max_digits, field.decimal_places

        num_as_str = lambda max_length: self.raw_string(
            ranint(1, max_length), string.digits)

        return Decimal('%s.%s' % (
            num_as_str(max_digits-decimal_places), 
            num_as_str(decimal_places)))

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
        return self.raw_string(
            randint(1, field.max_length), char_table)

    def value_for_charfield(self, field):
        '''
        Creates a random size string with length up to field.max_length.
        '''
        return self.raw_string(
            randint(1, field.max_length), string.printable)

    def value_for_textfield(self, field):
        '''
        Creates a random size string with length up to MAX_LENGTH.
        '''
        return self.raw_string(
            randint(1, MAX_LENGTH), string.printable)

    def value_for_urlfield(self, field):
        '''
        Creates a random size url string in the
        format 'http://[domain].[ext]'

        '''
        assert field.max_length > 16, 'max_length is too small'

        length = randint(9, field.max_length - 7)
        return 'http://%s' % self.raw_domain(length)

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

            data = self.raw_string(1, char_table_cc)
            while len(data) < length:
                if data[-1] == '.' or len(data) + 1 == length:
                    data += self.raw_string(1, char_table_cc)
                else:
                    data += self.raw_string(1, char_table_nc)
            return data

        return '%s@%s' % (
            gen_local_part(local_length),
            self.raw_domain(domain_length))

    def value_for_imagefield(self, field):
        '''
        Creates a filename with a image extension.
        
        '''
        ext_list = ('.jpg', '.png', '.gif')
        return self.raw_filename(field.max_length, ext_list)

    def value_for_filefield(self, field):
        '''
        Creates a filename with a document extension.
        
        '''
        ext_list = ('.txt', '.odt', '.pdf')
        return self.raw_filename(field.max_length, ext_list)

    def value_for_booleanfield(self, field):
        '''
        Generates a random True or False value.
        
        '''
        return choice((True, False))

    def value_for_foreignkey(self, field):
        pass

    def resolve(self, field):
        '''
        Finds out which method is mapped for a given field.
        Order: null -> default -> choices -> name -> type -> unsupported

        '''
        name = field.name
        class_name = field.__class__.__name__.lower()

        if field.null and not self.fill_null:
            return None

        elif field.has_default() and self.use_default:
            return self.default

        elif field.choices:
            return self.value_from_choices(field)

        else:
            if hasattr(self, 'value_for_%s' % name):
                return getattr('value_for_%s' % name)(field)

            elif hasattr(self, 'value_for_%s' % class_name):
                return getattr('value_for_%s' % class_name)(field)

            else:  # type not supported
                raise TypeError('%s is not supported by mommy.' % field.__class__)


class Field(object):
    def __init__(self, **kw):
        for k,v in kw.items():
            setattr(self, k, v)
