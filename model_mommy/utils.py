# -*- coding:utf-8 -*-

__doc__ = '''
Some useful functions if you plan on overwriting any
mommy methods.
'''.strip()

import re
import string

from random import randint, choice
from xml.dom.minidom import parseString

DOMAIN_EXT_LIST = (
    '.com', '.co', '.info', '.net', '.org', '.me', '.mobi', '.us',
    '.biz', '.mx', '.ca', '.ws', '.ag', '.com.co', '.net.co', '.nom.co',
    '.com.ag', '.net.ag', '.it', '.fr', '.org.ag', '.am', '.asia',
    '.at', '.be', '.bz', '.se', '.com.bz', '.net.bz', '.net.br', '.vg',
    '.com.br', '.cc', '.de', '.es', '.com.es', '.nom.es', '.org.es',
    '.eu', '.fm', '.gs', '.in', '.co.in', '.firm.in', '.gen.in', '.tv',
    '.ind.in', '.net.in', '.org.in', '.jobs', '.jp', '.ms', '.com.mx',
    '.nl', '.nu', '.co.nz', '.net.nz', '.org.nz', '.tc', '.tk',
    '.tw', '.com.tw', '.idv.tw', '.co.uk', '.me.uk', '.org.uk')


def raw_string(length, table):
    '''
    Creates a random string with length equal to `length` using
    only characters from `table`

    >>> import string
    >>> output = raw_string(20, string.letters)
    >>> assert len(output) == 20
    >>> assert all(map(lambda c: c in string.letters, output))

    '''
    if isinstance(table, basestring):
        return u''.join([choice(table) for i in range(length)])
    elif isinstance(table, tuple):
        return u''.join([unichr(randint(table)) for i in range(length)])
    else:
        raise Exception("Table type unsupported.")


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
    name = raw_string(length - len(ext), char_table)
    return name + ext


def raw_hostname(length):
    '''
    Creates a hostname with length equal to informed length.

    '''
    assert length > 0, 'length is too small'
    assert length < 64, 'length is too big'

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


def raw_domain(length, domain_ext_list=None):
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

        # -1 for the dot separating hostnames
        length = length - newhost_length - 1
        hostnames.append(raw_hostname(newhost_length))

    return '.'.join(hostnames) + ext


def raw_tagname(size=12):
    '''
    Creates a tagname for use with xml

    ps: not all valid tagnames are produced.
    '''
    # string_ascii_lowercase used for simplicity
    return raw_string(randint(1, size), string.ascii_lowercase + "_")


def raw_xml():
    '''
    Creates a random xml string. Final result can be pretty big.

    '''

    def add_children(doc, element, level=0):
        new_element = doc.createElement(raw_tagname())

        if choice((True, True, False)):
            text_node = doc.createTextNode(
                raw_string(randint(1, 100), string.printable))

            new_element.childNodes.append(text_node)

        element.childNodes.append(new_element)

        if choice((True, False)):
            add_children(doc, element, level)

        if level < 5 and choice((True, False)):
            add_children(doc, new_element, level + 1)

    # doc with random name
    doc = parseString(u'<%s />' % raw_tagname())
    root = doc.childNodes[0]

    while choice((True, True, False)):
        add_children(doc, root)

    return doc.toxml()
