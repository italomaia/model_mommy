# -*- coding:utf-8 -*-
from django.db.models.fields import *
from django.test import TestCase

import django

if django.VERSION < (1, 2):
    BigIntegerField = IntegerField


class HandlingModelsWithUnsupportedFields(TestCase):

    def test_unsupported_model_raises_an_explanatory_exception(self):
        from model_mommy import mommy
        from model_mommy.models import UnsupportedModel

        self.assertRaises(TypeError, lambda: mommy.make_one(UnsupportedModel))


class TestFillingFileFields(TestCase):

    def test_create_model_with_file_field(self):
        pass


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

        # this is enforced by the generator
        self.assertEqual(
            len(dummy_char_model.char_field), char_field.max_length)

    def test_create_model_with_TextField(self):
        from model_mommy import mommy
        from model_mommy.models import DummyTextModel

        text_field = DummyTextModel._meta.get_field('text_field')
        self.assertTrue(isinstance(text_field, TextField))

        dummy_text_model = mommy.make_one(DummyTextModel)
        self.assertTrue(
            isinstance(dummy_text_model.text_field, basestring))


class TestFillingEmailField(TestCase):

    def test_create_model_with_email_field(self):
        from model_mommy import mommy
        from model_mommy.models import DummyEmailModel

        dummy_email_model = mommy.make_one(DummyEmailModel)
        email_field = DummyEmailModel._meta.get_field('email_field')

        self.assertTrue(isinstance(email_field, EmailField))
        self.assertTrue(
            isinstance(dummy_email_model.email_field, basestring))

    def test_generated_email_format(self):
        assert False


class TestFillingBooleanFields(TestCase):

    def test_create_model_with_BooleanField(self):
        from model_mommy import mommy
        from model_mommy.models import DummyBooleanModel

        dummy_boolean_model = mommy.make_one(DummyBooleanModel)
        boolean_field = DummyBooleanModel._meta.get_field('boolean_field')

        self.assertTrue(isinstance(boolean_field, BooleanField))
        self.assertTrue(
            isinstance(dummy_boolean_model.boolean_field, bool))


class TestFillingDateFields(TestCase):

    def test_create_model_with_DateField(self):
        from model_mommy import mommy
        from model_mommy.models import DummyDateModel

        from datetime import date

        dummy_date_model = mommy.make_one(DummyDateModel)
        date_field = dummy_date_model._meta.get_field('date_field')

        self.assertTrue(isinstance(date_field, DateField))
        self.assertTrue(
            isinstance(dummy_date_model.date_field, date))

class TestFillingDateTimeFields(TestCase):

    def test_create_model_with_DateTimeField(self):
        from model_mommy import mommy
        from model_mommy.models import DummyDateTimeModel

        from datetime import date

        dummy_datetime_model = mommy.make_one(DummyDateTimeModel)
        datetime_field = dummy_datetime_model._meta.get_field('datetime_field')

        self.assertTrue(isinstance(datetime_field, DateTimeField))
        self.assertTrue(
            isinstance(dummy_datetime_model.datetime_field, date))


class TestFillingIntFields(TestCase):

    def setUp(self):
        from model_mommy import mommy
        from model_mommy.models import DummyIntModel

        self.dummy_int_model = mommy.make_one(DummyIntModel)

    def test_create_model_with_IntegerField(self):
        from model_mommy.models import DummyIntModel

        int_field = DummyIntModel._meta.get_field('int_field')
        self.assertTrue(isinstance(int_field, IntegerField))

        self.assertTrue(isinstance(self.dummy_int_model.int_field, int))

    def test_create_model_with_BigIntegerField(self):
        from model_mommy.models import DummyIntModel

        big_int_field = DummyIntModel._meta.get_field('big_int_field')
        self.assertTrue(isinstance(big_int_field, BigIntegerField))

        self.assertTrue(isinstance(self.dummy_int_model.big_int_field, int))

    def test_create_model_with_SmallIntegerField(self):
        from model_mommy.models import DummyIntModel

        small_int_field = DummyIntModel._meta.get_field('small_int_field')
        self.assertTrue(isinstance(small_int_field, SmallIntegerField))

        self.assertTrue(isinstance(self.dummy_int_model.small_int_field, int))


class TestFillingPositiveIntFields(TestCase):

    def setUp(self):
        from model_mommy import mommy
        from model_mommy.models import DummyPositiveIntModel

        self.dummy_positive_int_model =\
            mommy.make_one(DummyPositiveIntModel)

    def test_create_model_with_PositiveSmallIntegerField(self):
        from model_mommy.models import DummyPositiveIntModel

        positive_small_int_field = DummyPositiveIntModel.\
            _meta.get_field('positive_small_int_field')

        self.assertTrue(isinstance(
            positive_small_int_field, PositiveSmallIntegerField))

        positive_small_int_field = \
            self.dummy_positive_int_model.positive_small_int_field

        self.assertTrue(isinstance(positive_small_int_field, int))
        self.assertTrue(positive_small_int_field > 0)

    def test_create_model_with_PositiveIntegerField(self):
        from model_mommy.models import DummyPositiveIntModel

        positive_int_field = DummyPositiveIntModel.\
            _meta.get_field('positive_int_field')

        self.assertTrue(isinstance(positive_int_field, PositiveIntegerField))

        self.assertTrue(isinstance(
            self.dummy_positive_int_model.positive_int_field, int))
        self.assertTrue(
            self.dummy_positive_int_model.positive_int_field > 0)


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
        decimal_field =\
            DummyDecimalModel._meta.get_field('decimal_field')

        self.assertTrue(isinstance(decimal_field, DecimalField))
        self.assertTrue(isinstance(
            self.dummy_decimal_model.decimal_field, basestring))


class TestFillingURLFields(TestCase):

    def test_create_model_with_URLField(self):
        from model_mommy import mommy
        from model_mommy.models import DummyURLModel

        dummy_url_field = mommy.make_one(DummyURLModel)
        url_field = dummy_url_field._meta.get_field('url_field')

        self.assertTrue(isinstance(url_field, URLField))
        self.assertTrue(
            isinstance(dummy_url_field.url_field, basestring))

    def test_generated_url_format(self):
        assert False
