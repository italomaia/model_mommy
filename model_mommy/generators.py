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

import sys
import string
import datetime
from decimal import Decimal
from random import randint, choice, random

MAX_LENGTH = 300


def gen_from_default(default):
    return default
gen_from_default.required = ['default']


def gen_from_list(L):
    '''Makes sure all values of the field are generated from the list L
    Usage:
    from mommy import Mommy
    class KidMommy(Mommy):
      attr_mapping = {'some_field':gen_from_list([A, B, C])}
    '''
    return lambda: choice(L)

# -- DEFAULT GENERATORS --


def gen_from_choices(C):
    choice_list = map(lambda x: x[0], C)
    return gen_from_list(choice_list)


def gen_integer(min_int=-sys.maxint, max_int=sys.maxint):
    return randint(min_int, max_int)


gen_float = lambda: random() * gen_integer()


def gen_decimal(max_digits, decimal_places):
    num_as_str = lambda x: ''.join([str(randint(0, 9)) for i in range(x)])
    return "%s.%s" % (
        num_as_str(max_digits - decimal_places),
        num_as_str(decimal_places))
gen_decimal.required = ['max_digits', 'decimal_places']


gen_date = datetime.date.today


gen_datetime = datetime.datetime.now


def gen_raw_string(max_length, chr_table):
    '''
    Generates a random string from `chr_table` with
    size `max_length`.
    '''
    return ''.join(choice(chr_table) for i in range(max_length))


def gen_filename(max_length, ext_list=('txt', 'pdf', 'odt'), ext=None):
    '''
    Generates a random filename with length up to `max_length` and
    extension `ext`. If `ext` is not provided, one of these will be
    used:('txt', 'pdf', 'odt').
    '''
    if ext is None:
        ext = choice(ext_list)

    ext = '.%s' % ext
    txt_length = choice(range(1, max_length - len(ext)))
    return gen_raw_string(txt_length, string.letters + '-_') + ext
gen_filename.required = ['max_length']


def gen_slug(max_length=50):
    '''
    Generates a random slug with length up to `max_length`.
    '''
    slug_table = string.lowercase + string.digits + '_-'
    txt_length = choice(range(1, max_length + 1))
    return gen_raw_string(txt_length, slug_table)
gen_slug.required = ['max_length']


def gen_string(max_length):
    '''
    Generates a random string with length up to `max_length`.
    '''
    txt_length = choice(range(1, max_length + 1))
    return gen_raw_string(txt_length, string.printable)
gen_string.required = ['max_length']


gen_text = lambda: gen_string(MAX_LENGTH)


gen_boolean = lambda: choice((True, False))


# Needs improvement. This only generates one possible URL pattern.
def gen_url(max_length):
    assert max_length >= 20
    
    ext = gen_raw_string(choice([2, 3]), string.letters)
    letters = ''.join(choice(string.letters)
        for i in range(max_length - 15 - len(ext)))
    return 'http://www.%s.%s' % (letters, ext)
gen_url.required = ['max_length']


def gen_email(max_length):
    # ref: http://en.wikipedia.org/wiki/Email_address
    # local-part: up to 64char
    # domain-part: up to 253char
    # total: up to 254char

    assert max_length >= 3
    max_length = min(max_length, 254) - 1  # -> @
    local_length = choice(range(1, min(max_length, 65)))
    domain_length = min(max_length - local_length, 253)
    email = '%s@%s'

    def gen_local_part(length):
        char_table_cc = string.letters + string.digits + "!#$%&'*+-/=?^_`{|}~"
        char_table_nc = string.letters + string.digits + "!#$%&'*+-/=?^_`{|}~."

        data = gen_raw_string(1, char_table_cc)
        while len(data) < length:
            if data[-1] == '.' or len(data) + 1 == length:
                data += gen_raw_string(1, char_table_cc)
            else:
                data += gen_raw_string(1, char_table_nc)
        return data

    def gen_domain_part(length):
        char_table_cc = string.letters + string.digits + '-_'
        char_table_nc = string.letters + string.digits + '-_.'
        count = 0

        data = gen_raw_string(1, char_table_cc)
        while len(data) < length:
            if data[-1] == '.' or len(data) + 1 == length or count == 63:
                data += gen_raw_string(1, char_table_cc)
                count = 0
            else:
                data += gen_raw_string(1, char_table_nc)
                count += 1
        return data

    return email % (
        gen_local_part(local_length),
        gen_domain_part(domain_length))
gen_email.required = ['max_length']
