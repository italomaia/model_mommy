# -*- coding:utf-8 -*-
from django.db.models.fields import *
from django.db.models.fields.related import *
from django.db.models.fields.files import *

import django
from django.test import TestCase

if django.VERSION < (1, 2):
    BigIntegerField = IntegerField


class HandlingModelsWithUnsupportedFields(TestCase):
    def test_unsupported_model_raises_an_explanatory_exception(self):
        from model_mommy import mommy
        from model_mommy.models import UnsupportedModel

        self.assertRaises(TypeError, lambda: mommy.make_one(UnsupportedModel))


class TestFillingSlugField(TestCase):
    def is_slug(self, slug):
        import string

        slug_table = string.lowercase + string.digits + '_-'
        for char in slug:
            if char not in slug_table:
                return False
        return True

    def test_create_model_with_slugfield(self):
        from model_mommy import mommy
        from model_mommy.models import DummySlugModel

        dummy_slug_model = mommy.make_one(DummySlugModel)
        self.assertTrue(
            isinstance(dummy_slug_model.slug_field, basestring))

    def test_if_data_for_slugfield_is_slug_text(self):
        from model_mommy.models import DummySlugModel
        from model_mommy import mommy

        dummy_slug_model = mommy.make_one(DummySlugModel)
        self.assertTrue(
            self.is_slug(dummy_slug_model.slug_field))


class TestFillingStringFields(TestCase):
    def test_create_model_with_CharField(self):
        from model_mommy import mommy
        from model_mommy.models import DummyCharModel

        char_field = DummyCharModel._meta.get_field('char_field')
        self.assertTrue(isinstance(char_field, CharField))

        dummy_char_model = mommy.make_one(DummyCharModel)
        self.assertTrue(
            isinstance(dummy_char_model.char_field, basestring))

    def test_create_model_with_TextField(self):
        from model_mommy import mommy
        from model_mommy.models import DummyTextModel

        text_field = DummyTextModel._meta.get_field('text_field')
        self.assertTrue(isinstance(text_field, TextField))

        dummy_text_model = mommy.make_one(DummyTextModel)
        self.assertTrue(
            isinstance(dummy_text_model.text_field, basestring))


class TestFillingBooleanFields(TestCase):
    def test_create_model_with_BooleanField(self):
        from model_mommy import mommy
        from model_mommy.models import DummyBooleanModel

        dummy_boolean_model = mommy.make_one(DummyBooleanModel)
        boolean_field = DummyBooleanModel._meta.get_field('boolean_field')

        self.assertTrue(isinstance(boolean_field, BooleanField))
        self.assertTrue(
            isinstance(dummy_boolean_model.boolean_field, bool))


class TestFillingDateTimeFields(TestCase):
    def test_create_model_with_DateField(self):
        from model_mommy import mommy
        from model_mommy.models import DummyDateModel

        from datetime import date

        dummy_date_model = mommy.make_one(DummyDateModel)
        date_field = dummy_date_model._meta.get_field('date_field')

        self.assertTrue(isinstance(date_field, DateField))
        self.assertTrue(
            isinstance(dummy_date_model.date_field, date))

    def test_create_model_with_DateTimeField(self):
        from model_mommy import mommy
        from model_mommy.models import DummyDateTimeModel

        from datetime import date

        dummy_datetime_model = mommy.make_one(DummyDateTimeModel)
        datetime_field = dummy_datetime_model._meta.get_field('datetime_field')

        self.assertTrue(isinstance(datetime_field, DateTimeField))
        self.assertTrue(
            isinstance(dummy_datetime_model.datetime_field, date))

    def test_create_model_with_TimeField(self):
        from model_mommy import mommy
        from model_mommy.models import DummyTimeModel

        from datetime import date

        dummy_time_model = mommy.make_one(DummyTimeModel)
        time_field = dummy_time_model._meta.get_field('time_field')

        self.assertTrue(isinstance(time_field, TimeField))
        self.assertTrue(
            isinstance(dummy_time_model.time_field, date))


class TestFillingIntFields(TestCase):
    def setUp(self):
        from model_mommy import mommy
        from model_mommy.models import DummyIntModel

        self.dummy_int_model = mommy.make_one(DummyIntModel)

    def test_create_model_with_IntegerField(self):
        from model_mommy.models import DummyIntModel

        integer = self.dummy_int_model.int_field
        integer_field = DummyIntModel._meta.get_field('int_field')

        self.assertTrue(isinstance(integer_field, IntegerField))
        self.assertTrue(isinstance(integer, int))
        self.assertTrue(integer >= -2147483648)
        self.assertTrue(integer <= 2147483647)

    def test_create_model_with_BigIntegerField(self):
        from model_mommy.models import DummyIntModel

        big_int = self.dummy_int_model.big_int_field
        big_int_field = DummyIntModel._meta.get_field('big_int_field')

        self.assertTrue(isinstance(big_int_field, BigIntegerField))
        self.assertTrue(isinstance(big_int, int) or isinstance(big_int, long))
        self.assertTrue(big_int >= -9223372036854775808l)
        self.assertTrue(big_int <= 9223372036854775807l)

    def test_create_model_with_SmallIntegerField(self):
        from model_mommy.models import DummyIntModel

        small_int = self.dummy_int_model.small_int_field
        small_int_field = DummyIntModel._meta.get_field('small_int_field')

        self.assertTrue(isinstance(small_int_field, SmallIntegerField))
        self.assertTrue(isinstance(small_int, int))
        self.assertTrue(small_int >= -32768)
        self.assertTrue(small_int <= 32767)


class TestFillingPositiveIntFields(TestCase):
    def setUp(self):
        from model_mommy import mommy
        from model_mommy.models import DummyPositiveIntModel

        self.dummy_positive_int_model = mommy.make_one(DummyPositiveIntModel)

    def test_create_model_with_PositiveSmallIntegerField(self):
        from model_mommy.models import DummyPositiveIntModel

        positive_small_int = self.dummy_positive_int_model.positive_small_int_field
        positive_small_int_field = DummyPositiveIntModel._meta.get_field('positive_small_int_field')

        self.assertTrue(isinstance(
            positive_small_int_field, PositiveSmallIntegerField))

        self.assertTrue(isinstance(positive_small_int, int))
        self.assertTrue(positive_small_int >= 0)
        self.assertTrue(positive_small_int <= 65535)

    def test_create_model_with_PositiveIntegerField(self):
        from model_mommy.models import DummyPositiveIntModel

        positive_int = self.dummy_positive_int_model.positive_int_field

        positive_int_field = DummyPositiveIntModel._meta.get_field('positive_int_field')

        self.assertTrue(isinstance(positive_int_field, PositiveIntegerField))
        self.assertTrue(isinstance(positive_int, int) or isinstance(positive_int, long))
        self.assertTrue(positive_int >= 0)
        self.assertTrue(positive_int <= 4294967295)


class TestFillingOthersNumericFields(TestCase):
    def test_create_model_with_FloatField(self):
        from model_mommy import mommy
        from model_mommy.models import DummyNumbersModel

        self.dummy_numbers_model = mommy.make_one(DummyNumbersModel)
        float_field = DummyNumbersModel._meta.get_field('float_field')

        self.assertTrue(isinstance(float_field, FloatField))
        self.assertTrue(isinstance(
            self.dummy_numbers_model.float_field, float))

    def test_create_model_with_DecimalField(self):
        from model_mommy import mommy
        from model_mommy.models import DummyDecimalModel

        self.dummy_decimal_model = mommy.make_one(DummyDecimalModel)
        decimal_field = DummyDecimalModel._meta.get_field('decimal_field')

        self.assertTrue(isinstance(decimal_field, DecimalField))
        self.assertTrue(isinstance(self.dummy_decimal_model.decimal_field, basestring))


class TestFillingCommaSeparatedIntegerFields(TestCase):
    def is_comma_separated_integer_field(self, value):
        import re
        regex = re.compile('^-?\d+(,-?\d+)*$')
        return regex.match(value) is not None

    def test_create_model_with_CommaSeparatedIntegerField(self):
        from model_mommy import mommy
        from model_mommy.models import DummyCommaSeparatedIntegerModel

        self.comma_separated_model = mommy.make_one(DummyCommaSeparatedIntegerModel)
        comma_separated_field = DummyCommaSeparatedIntegerModel._meta.get_field('comma_separated_integer_field')
        field_value = self.comma_separated_model.comma_separated_integer_field

        self.assertTrue(isinstance(comma_separated_field, CommaSeparatedIntegerField))
        self.assertTrue(len(field_value) <= comma_separated_field.max_length)

    def test_if_CommaSeparatedIntegerField_format_is_valid(self):
        from model_mommy import mommy
        from model_mommy.models import DummyCommaSeparatedIntegerModel

        self.comma_separated_model = mommy.make_one(DummyCommaSeparatedIntegerModel)
        field_value = self.comma_separated_model.comma_separated_integer_field

        self.assertTrue(self.is_comma_separated_integer_field(field_value))


class TestFillingIPAddressField(TestCase):
    def is_ip_address_format_valid(self, value):
        split = tuple(map(lambda v: int(v), value.split('.')))

        if split == (0, 0, 0, 0):
            return False
        elif split[0] in (0, 10):
            return False
        elif split[-1] == 0:
            return False
        elif 255 in split:
            return False
        elif split[:1] == (192, 168):
            return False
        elif (172, 16, 0, 0) <= split <= (172, 31, 255, 255):
            return False
        else:
            return True

    def test_create_model_with_IPAddressField(self):
        from model_mommy import mommy
        from model_mommy.models import DummyIPAddressFieldModel

        self.ip_address_model = mommy.make_one(DummyIPAddressFieldModel)
        ip_address_field = DummyIPAddressFieldModel._meta.get_field('ip_address_field')
        field_value = self.ip_address_model.ip_address_field

        self.assertTrue(isinstance(ip_address_field, IPAddressField))
        self.assertTrue(isinstance(field_value, basestring))

    def test_if_IPAddressField_format_is_valid(self):
        from model_mommy import mommy
        from model_mommy.models import DummyIPAddressFieldModel

        self.ip_address_model = mommy.make_one(DummyIPAddressFieldModel)
        field_value = self.ip_address_model.ip_address_field

        self.assertTrue(self.is_ip_address_format_valid(field_value))


class TestFillingURLFields(TestCase):
    def test_create_model_with_URLField(self):
        from model_mommy import mommy
        from model_mommy.models import DummyURLModel

        dummy_url_model = mommy.make_one(DummyURLModel)
        url_field = dummy_url_model._meta.get_field('url_field')
        field_value = dummy_url_model.url_field

        self.assertTrue(isinstance(url_field, URLField))
        self.assertTrue(isinstance(field_value, basestring))
        self.assertTrue(len(field_value) <= url_field.max_length)


class TestFillingFileFields(TestCase):
    def test_create_model_with_FileField(self):
        from model_mommy import mommy
        from model_mommy.models import DummyFileModel

        dummy_file_model = mommy.make_one(DummyFileModel)
        file_field = dummy_file_model._meta.get_field('file_field')
        field_value = dummy_file_model.file_field

        field_value_len = len(unicode(field_value.name))
        field_max_len = file_field.max_length

        self.assertTrue(isinstance(file_field, FileField))
        self.assertTrue(isinstance(field_value.name, basestring))
        self.assertTrue(field_value_len <= field_max_len)

    def test_create_model_with_ImageField(self):
        from model_mommy import mommy
        from model_mommy.models import DummyImageModel

        dummy_image_model = mommy.make_one(DummyImageModel)
        image_field = dummy_image_model._meta.get_field('image_field')
        field_value = dummy_image_model.image_field

        self.assertTrue(isinstance(image_field, FileField))
        self.assertTrue(isinstance(field_value.name, basestring))
        self.assertTrue(len(field_value.name) <= image_field.max_length)


class TestFillingEmailField(TestCase):
    def test_create_model_with_EmailField(self):
        from model_mommy import mommy
        from model_mommy.models import DummyEmailModel

        dummy_email_model = mommy.make_one(DummyEmailModel)
        email_field = DummyEmailModel._meta.get_field('email_field')
        field_value = dummy_email_model.email_field

        self.assertTrue(isinstance(email_field, EmailField))
        self.assertTrue(isinstance(field_value, basestring))
        self.assertTrue(len(field_value) <= email_field.max_length)

    def test_if_EmailField_format_is_valid(self):
        import re
        import string

        from model_mommy import mommy
        from model_mommy.models import DummyEmailModel

        dummy_email_model = mommy.make_one(DummyEmailModel)
        data = dummy_email_model.email_field

        table = string.letters + string.digits + "!#$%&'*+-/=?^_`{|}~."

        m = re.match(r"[%(t)s]+@[%(t)s](\.[%(t)s]+)*" % {'t': table}, data)
        self.assertTrue(m is not None)
        self.assertTrue('..' not in data)
        self.assertTrue(data[0] != '.')
        self.assertTrue(data[-1] != '.')