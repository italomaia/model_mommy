# -*- coding:utf-8 -*-

from django.db.models.fields import NOT_PROVIDED

from django.db.models.fields.related import *
from django.contrib.contenttypes.generic import GenericRelation

from .utils import *
from .constants import *

import datetime
from random import random


if not hasattr(__builtins__, 'long'):
    long = int  # python < 3.0


class Mommy(object):
    def __init__(self, model, fill_null=None):
        """
        Keyword arguments:
        model -- base model instance
        fill_null -- force null or non null value for nullable fields. If None, leave up to chance.

        """
        self.model = model
        self.fill_null = fill_null

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

    def attrs(self, flat, **attrs):
        """
        Returns all attributes (but related fields) required for a model.

        """
        return self.__attrs(False, flat, self.get_fields(), **attrs)

    def get_fields(self):
        """
        Returns all available fields, but m2m fields.

        """
        return self.model._meta.fields

    def get_m2m_fields(self):
        """
        Returns all m2m fields.

        """
        return self.model._meta.many_to_many

    def get_all_fields(self):
        """
        Returns all available fields.

        """
        return self.get_fields() + self.get_m2m_fields()

    def __attrs(self, commit, flat, fields, **attrs):
        """
        Returns all fields, but m2m fields, used to populate a model. You can
        use this method directly to create fake form data.

        Arguments:
        commit -- should related fields be commited?
        flat -- should related fields be ignored?
        fields -- which fields should be created?
        **attrs -- optional defined values for fields

        """
        rt = {}  # return value / values for fields

        for field in fields:
            # field value was provided. Ignoring...
            if field.name in attrs:
                rt[field.name] = attrs[field.name]

            elif isinstance(field, RelatedField) and flat:
                continue  # ignore non-provided related fields

            elif isinstance(field, RelatedField) and field.null:
                continue  # ignore nullable related fields

            elif type(field) in (AutoField, GenericRelation):
                continue

            elif field.null and (self.fill_null is False):
                continue

            elif field.null and (self.fill_null is None) and choice(LEAVE_TO_CHANCE):
                continue

            elif field.blank and choice(LEAVE_TO_CHANCE):
                if field.default == NOT_PROVIDED:
                    rt[field.name] = ''
                else:
                    rt[field.name] = field.default

            else:
                rt[field.name] = self.__get_value_for_field(field)

                if hasattr(rt[field.name], 'save') and commit:
                    rt[field.name].save()

        return rt

    def __m2m_attrs(self, fields, **attrs):
        rt = {}

        for field in fields:
            # field value was provided. Ignoring...
            if field.name in attrs:
                rt[field.name] = attrs[field.name]
            else:
                rt[field.name] = self.__get_value_for_field(field)
        return rt

    def __make(self, commit, **attrs):
        """
        If attribute value is provided in attrs, it is not overwritten.
        AutoField and GenericRelation fields are ignored.
        Nullable OneToOne, ForeignKey and ManyToMany fields are ignored.

        Keyword arguments:
        commit (bool) -- Should instance be commited?
        attrs (dict) -- pre-defined instance values

        """

        m2m_attrs = self.__m2m_attrs(self.get_m2m_fields(), **attrs)
        attrs = self.__attrs(commit, False, self.get_fields(), **attrs)

        instance = self.model(**attrs)

        if commit:
            instance.save()

            # m2m instance are only persisted if commit is True
            for key, m2m_values in m2m_attrs.items():
                m2m_relation = getattr(instance, key)

                for value in m2m_values:
                    m2m_relation.add(value)

        return instance

    def __get_value_for_field(self, field):
        """
        Decides which method should create the value for field.

        Evaluation order:
            choices -> value_for_<fieldname>field -> value_for_<fieldtype>

        """
        field_cls = field.__class__
        field_cls_name = field_cls.__name__.lower()

        field_name_method = 'value_for_' + field.name + "field"
        field_type_method = 'value_for_' + field_cls_name

        if field.choices:  # get from avaiable choices
            return choice(map(lambda c: c[0], field.choices))

        elif hasattr(self, field_name_method):
            return getattr(self, field_name_method)(field)

        elif hasattr(self, field_type_method):
            return getattr(self, field_type_method)(field)

        else:  # unsupported field type
            raise TypeError('%s is not supported by mommy.' % field_cls_name)

    def value_for_booleanfield(self, field):
        """
        Returns True or False.

        >>> field = object()
        >>> base = Base({})
        >>> value = base.value_for_booleanfield(field)
        >>> assert value in (True, False), 'returned value is invalid'

        """
        return choice((False, True))

    def value_for_nullbooleanfield(self, field):
        """
        Returns None, True or False.

        >>> field = object()
        >>> base = Base({})
        >>> value = base.value_for_nullbooleanfield(field)
        >>> assert value in (None, True, False), 'returned value is invalid'

        """
        return choice((False, True))  # nullbooleanfield ahs null=True by default

    def value_for_smallintegerfield(self, field):
        """
        Returns a 16bits integer.

        >>> field = object()
        >>> base = Base({})
        >>> value = base.value_for_smallintegerfield(field)
        >>> assert isinstance(value, int), 'value is not integer'

        """
        return randint(MIN_SMALL_INT, MAX_SMALL_INT)

    def value_for_positivesmallintegerfield(self, field):
        """
        Returns a positive 16bits integer.

        """
        return randint(0, MAX_SMALL_INT)

    def value_for_integerfield(self, field):
        """
        Returns a 32bits integer.

        """
        return randint(MIN_INT, MAX_INT)

    def value_for_positiveintegerfield(self, field):
        """
        Returns a positive 32bits integer.

        """
        return randint(0, MAX_INT)

    def value_for_bigintegerfield(self, field):
        """
        Returns a 64bits integer.

        """
        return randint(MIN_BIG_INT, MAX_BIG_INT)

    def value_for_floatfield(self, field):
        """
        Returns a random float value

        """
        return random() * randint(MIN_INT, MAX_INT)

    def value_for_decimalfield(self, field):
        """
        Returns a random decimal like string obeying field's max_digits and decimal_places

        """
        md, dp = field.max_digits, field.decimal_places

        md_number = ''.join([str(randint(0, 9)) for i in range(md - dp)])
        dp_number = ''.join([str(randint(0, 9)) for i in range(dp)])

        return "%s.%s" % (md_number, dp_number)

    def value_for_commaseparatedintegerfield(self, field):
        """
        Returns string in the format number[,number]*
        *number* is a 32bits integer

        """
        max_length = field.max_length

        number = randint(MIN_INT, MAX_INT)
        str_number = str(number)

        cut_off = len(str_number) - min(len(str_number), max_length)
        rt = str(int(str_number[cut_off:]))

        while (len(rt) < max_length - 1) and not choice(LEAVE_TO_CHANCE):
            number = randint(MIN_INT, MAX_INT)
            str_number = str(number)

            rt += ","
            cut_off = len(str_number) - min(len(str_number), max_length - len(rt))
            rt += str(int(str_number[cut_off:]))

        return rt

    def value_for_datefield(self, field):
        """
        Returns a datetime.date object for the current time

        """
        return datetime.date.today()

    def value_for_timefield(self, field):
        """
        Returns a datetime.datetime object for the current time

        """
        return datetime.datetime.now()

    def value_for_datetimefield(self, field):
        """
        Returns a datetime.datetime object for the current time

        """
        return datetime.datetime.now()

    def value_for_ipaddressfield(self, field):
        """
        Generates a valid IPV4 for IPAddress

        Does not produce the following ip addresses:
        - 0.0.0.0 - reserved for hosts
        - 0.x.x.x - class A network can't be zero
        - x.x.x.0 - host ip can't be 0
        - 255.x.x.x or x.255.x.x or x.x.255.x or x.x.x.255 - no network address can be 255/ broadcast address
        - 10.x.x.x - private use for IANA
        - 192.168.x.x - private use for IANA
        - 172.16.0.0 to 172.31.255.255 - private use for IANA

        ref: http://www.comptechdoc.org/independent/networking/guide/netaddressing.html

        """
        ip_address = None

        while True:
            ip_address = (
                randint(1, 254), randint(0, 254),
                randint(0, 254), randint(1, 254))

            if (ip_address[0] == 10) or\
               (ip_address[0] == 192 and ip_address[1] == 168) or\
               ((172, 16, 0, 0) <= ip_address <= (172, 31, 255, 255)):
                continue
            else:
                break
        return '.'.join([str(token) for token in ip_address])

    def value_for_charfield(self, field):
        """
        Returns a random word with provided max_length.

        """
        length = randint(1, field.max_length)
        return raw_string(length, LATIN1_TABLE)

    def value_for_slugfield(self, field):
        """
        Returns a random slug with provided max_length.

        """
        length = randint(1, field.max_length)
        return raw_string(length, SLUG_TABLE)

    def value_for_textfield(self, field):
        """
        Returns a random text with default max_length

        """
        length = randint(1, TEXT_MAX_LENGTH)
        return raw_string(length, LATIN1_TABLE + '\n')

    def value_for_xmlfield(self, field):
        """
        Deprecated since django 1.3

        """
        raise Exception("XMLField generator should be implemented manually.")

    def value_for_filefield(self, field):
        """
        Returns a random file path

        """
        length = randint(1, field.max_length)
        return raw_filename(length, FILE_EXT_LIST)

    def value_for_filepathfield(self, field):
        """
        Returns a random file path

        """
        length = randint(1, field.max_length)
        return raw_filename(length, FILE_EXT_LIST)

    def value_for_imagefield(self, field):
        """
        Returns a random image file path

        """
        length = randint(1, field.max_length)
        return raw_filename(length, IMG_EXT_LIST)

    def value_for_urlfield(self, field):
        """
        Returns a random url without parameters.

        """
        assert field.max_length > 8, 'informed max_length for url is too small'

        length = randint(1, field.max_length - 7)
        return "http://%s" % raw_hostname(length)

    def value_for_emailfield(self, field):
        """
        Returns a random email string.

        ref: http://en.wikipedia.org/wiki/Email_address

        """
        max_length = field.max_length

        assert max_length >= 3, 'max_length for emailfield is too short'

        max_length -= 1  # @
        local_part_length = randint(1, max_length - 1)  # make sure local part < max_length
        domain_part_length = randint(1, max_length - local_part_length)

        local_part = raw_email_localpart(local_part_length)
        domain_part = raw_hostname(domain_part_length)
        return u"%s@%s" % (local_part, domain_part)

    def value_for_foreignkey(self, field):
        """
        Returns a instance for the field.

        """
        if not field.null:
            model = field.related.parent_model
            base = self.__class__(model)
            return base.__make(False)

    def value_for_onetoonefield(self, field):
        """
        Returns a instance for the field.

        """
        if not field.null:
            model = field.related.parent_model
            base = self.__class__(model)
            return base.__make(False)

    def value_for_manytomanyfield(self, field):
        """
        Implement this method manually.

        """
        return []