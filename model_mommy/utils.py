# -*- coding:utf-8 -*-

__doc__ = '''
Some useful functions if you plan on overwriting mommy methods.
'''.strip()

import re
import string

from random import randint, choice

DOC_EXT_LIST = ('.doc', '.xsl', '.ppt', '.odt', '.odp', '.xml',
                '.txt', '.zip', '.tar', '.tar.gz')

IMG_EXT_LIST = ('.jpg', '.png', '.gif', '.bmp')


def raw_string(length, table):
    """
    Creates a random string with length equal to `length` using
    only characters from `table`

    >>> import string
    >>> output = raw_string(20, string.letters)
    >>> assert len(output) == 20
    >>> assert all(map(lambda c: c in string.letters, output))

    """
    if isinstance(table, basestring):
        return u''.join([choice(table) for i in range(length)])
    elif isinstance(table, tuple):
        return u''.join([unichr(randint(table)) for i in range(length)])
    else:
        raise Exception("Unsupported table type provided.")


def raw_filename(length, ext_list=None):
    """
    ref: http://en.wikipedia.org/wiki/Filename

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
    >>>
    >>> assert ext in ext_list
    >>> assert len(filename) == length

    """
    char_table = re.sub(r'[/\?%*:|"<>]', '', string.printable)
    ext = choice(ext_list)
    name = raw_string(length - len(ext), char_table)
    return name + ext


def raw_email_localpart(length):
    """
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
    Creates a hostname with length equal to informed length.

    >>> length = 10
    >>> value = raw_hostname_label(length)
    >>>
    >>> assert len(value) == length
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


def raw_hostname(length, ext_list=None):
    """
    ref: http://en.wikipedia.org/wiki/Hostname
    ref: http://en.wikipedia.org/wiki/Domain_Name

    Creates a random valid hostname.
    (a domain name is a hostname with an associated ip address)

    Params:
    - ext_list - if provided, domain ext will belong to this list.

    >>> length = 20
    >>> ext_list = ('.org', '.org.br')
    >>> value = raw_hostname(length)
    >>> assert isinstance(value, basestring), 'method returned something other than a basestring'
    >>> value = raw_hostname(length, ext_list)
    >>> split = value.split('.')
    >>> assert len(split) > 1, 'no extension found'
    >>> assert split[-1] == 'org' or split[-1] == 'br', 'found extension is other than provided'

    """
    assert length > 1, 'length is too short'
    assert length < 256, 'length is too big'

    if ext_list is not None:
        assert max(map(lambda i: len(i), ext_list)) < length, \
        'length must be bigger than any provided extension'

    labels = []

    if ext_list:
        ext = choice(ext_list)
        labels.append(ext.startswith(".") and ext[1:] or ext)

    sum_labels = sum(map(lambda i: len(i), labels))
    while (sum_labels + len(labels)) < length:
        label_length = randint(1, min(63, sum_labels))

        label = raw_hostname_label(label_length)
        labels.append(label)
        sum_labels = sum(map(lambda i: len(i), labels))

    return '.'.join(labels)