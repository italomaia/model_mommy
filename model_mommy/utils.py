# -*- coding:utf-8 -*-

__doc__ = '''
Some useful functions if you plan on overwriting mommy methods.
'''.strip()

import re
import string
from random import randint, choice

from .constants import ASCII_TABLE


def raw_string(length, table):
    """
    Creates a random string with length equal to `length` using
    only characters from `table`

    Keyword arguments:
    length -- length for the new string
    table -- string with usable characters or tuple with usable char code range

    """
    if isinstance(table, basestring):
        return u''.join([choice(table) for i in range(length)])
    elif isinstance(table, tuple):
        return u''.join([unichr(randint(*table)) for i in range(length)])
    else:
        raise TypeError("Unsupported table type provided.")


def raw_filename(length, ext_list=None):
    """
    Creates a random filename with length up to `max_length`
    and one of the given extensions. Make sure the biggest extension
    length is smaller than `length`.

    Keyword arguments:
    length -- length for the new filename
    ext_list -- list of valid extensions.

    ref: http://en.wikipedia.org/wiki/Filename

    """
    char_table = re.sub(r'[/\?%*:|"<>]', '', ASCII_TABLE)

    if ext_list is not None:
        ext = choice(ext_list)
    else:
        ext = ''

    name = raw_string(length - len(ext), char_table)
    return name + ext


def raw_email_localpart(length):
    """
    Creates the localpart for an e-mail.

    ref: http://en.wikipedia.org/wiki/Email_address

    """
    char_table = string.ascii_letters + string.digits + "!#$%&'*+-/=?^_`{|}~"
    char_table_ = char_table + "."

    email = ""
    while len(email) < length:
        if len(email) in (0, length - 1) or email[-1] == '.':
            email += choice(char_table)
        else:
            email += choice(char_table_)
    return email


def raw_hostname_label(length):
    """
    Creates a hostname label.

    Keyword arguments:
    length -- length for the new hostname label

    """
    assert length > 0, 'provided length for hostname is too small. min is 1'
    assert length < 64, 'provided length for hostname is too big. max is 63'

    char_table = string.ascii_letters + string.digits
    char_table_ = string.ascii_letters + string.digits + '-'
    hostname = ''

    while len(hostname) < length:
        # hostname can't start nor end in dot
        if len(hostname) == 0 or len(hostname) == length - 1:
            hostname += choice(char_table)
        else:
            hostname += choice(char_table_)

    return hostname


def raw_hostname(apr_length, ext_list=None):
    """
    Creates a random valid hostname.
    (a domain name is a hostname with an associated ip address)

    Keyword arguments:
    apr_length -- approximate length for new hostname (length is never bigger than apr_length)
    ext_list -- if provided, domain ext will belong to this list.

    ref: http://en.wikipedia.org/wiki/Hostname
    ref: http://en.wikipedia.org/wiki/Domain_Name

    """
    assert apr_length > 0, 'length is too short'
    assert apr_length < 256, 'length is too big'

    if ext_list is not None:
        assert max(map(lambda i: len(i), ext_list)) < apr_length,\
        'length must be bigger than any provided extension'

    labels = []

    if ext_list:
        ext = choice(ext_list)
        labels.append(ext.startswith(".") and ext[1:] or ext)

    sum_labels = sum(map(lambda i: len(i), labels))
    while sum_labels + len(labels) < apr_length:
        max_length = min(63, apr_length - sum_labels - len(labels))
        label_length = randint(1, max_length)

        label = raw_hostname_label(label_length)
        labels.insert(0, label)
        sum_labels = sum(map(lambda i: len(i), labels))

    return '.'.join(labels)
