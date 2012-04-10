# -*- coding:utf-8 -*-

__doc__ = '''
Some useful functions if you plan on overwriting mommy methods.
'''.strip()

import re
import string

from random import randint, choice

AUD_EXT_LIST = (
    '.aif', '.iff', '.mid', '.mp3', '.m4a', '.wav', '.wma'
)

DOC_EXT_LIST = (
    '.doc', '.docx', '.ppt', '.pps', '.rtf', '.tex', '.log',
    '.xsl', '.xml', '.odt', '.odp', '.txt'
)

IMG_EXT_LIST = (
    '.bmp', '.gif', '.jpg', '.png', '.psd', '.tga', '.tif',
    '.xcf'
)

VID_EXT_LIST = (
    '.3gp', '.asf', '.avi', '.flv', '.mov', '.mp4', '.mpg',
    '.rm', '.swf', '.vob', '.wmv', '.mkv'
)

FILE_EXT_LIST = AUD_EXT_LIST + DOC_EXT_LIST + IMG_EXT_LIST + VID_EXT_LIST


def raw_string(length, table):
    """
    Creates a random string with length equal to `length` using
    only characters from `table`

    Keyword arguments:
    length -- length for the new string
    table -- string with usable characters or tuple with usable char code range

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
    length -- length for the new filename
    ext_list -- list of valid extensions.

    >>> from os import path
    >>>
    >>> length = 20
    >>> ext_list = ('.doc', '.pdf')
    >>> filename = raw_filename(length, ext_list)
    >>> name, ext = path.splitext(filename)
    >>>
    >>> assert ext in ext_list
    >>> assert len(filename) == length

    """
    char_table = re.sub(r'[/\?%*:|"<>]', '', string.printable)

    if ext_list is not None:
        ext = choice(ext_list)
    else:
        ext = ''

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

    Keyword arguments:
    length -- length for the new hostname label

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

    Keyword arguments:
    length -- length for the new hostname
    ext_list -- if provided, domain ext will belong to this list.

    >>> length = 20
    >>> ext_list = ('.org', '.org.br')

    >>> value = raw_hostname(length)
    >>> assert isinstance(value, basestring), 'method returned something other than a basestring'

    >>> value = raw_hostname(length, ext_list)
    >>> split = value.split('.')

    >>> assert len(split) > 1, 'no extension found'
    >>> assert split[-1] == 'org' or split[-1] == 'br', 'found extension is other than provided'

    """
    assert length > 0, 'length is too short'
    assert length < 256, 'length is too big'

    if ext_list is not None:
        assert max(map(lambda i: len(i), ext_list)) < length, \
        'length must be bigger than any provided extension'

    labels = []

    if ext_list:
        ext = choice(ext_list)
        labels.append(ext.startswith(".") and ext[1:] or ext)

    sum_labels = sum(map(lambda i: len(i), labels))
    while sum_labels + len(labels) < length:
        max_length = min(63, length - sum_labels - len(labels))
        label_length = randint(1, max_length)

        label = raw_hostname_label(label_length)
        labels.insert(0, label)
        sum_labels = sum(map(lambda i: len(i), labels))

    return '.'.join(labels)


if __name__ == "__main__":
    import doctest
    doctest.testmod()