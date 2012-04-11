# -*- coding:utf-8 -*-

from django.test import TestCase

from random import choice

class TestUtilsRawString(TestCase):

    def test_raw_string_output_length(self):
        from model_mommy.utils import raw_string
        from model_mommy.constants import ASCII_TABLE, ASCII_RANGE, LATIN1_TABLE, LATIN1_RANGE, UNICODE_RANGE

        length = 11
        value = raw_string(length, ASCII_TABLE)
        self.assertEqual(len(value), length)

        value = raw_string(length, ASCII_RANGE)
        self.assertEqual(len(value), length)

        length = 22
        value = raw_string(length, ASCII_TABLE)
        self.assertEqual(len(value), length)

        value = raw_string(length, ASCII_RANGE)
        self.assertEqual(len(value), length)

        length = 11
        value = raw_string(length, LATIN1_TABLE)
        self.assertEqual(len(value), length)

        value = raw_string(length, LATIN1_RANGE)
        self.assertEqual(len(value), length)

        value = raw_string(length, UNICODE_RANGE)
        self.assertEqual(len(value), length)

        length = 22
        value = raw_string(length, LATIN1_TABLE)
        self.assertEqual(len(value), length)

        value = raw_string(length, LATIN1_RANGE)
        self.assertEqual(len(value), length)

        value = raw_string(length, UNICODE_RANGE)
        self.assertEqual(len(value), length)

    def test_raw_string_output_type(self):
        from model_mommy.utils import raw_string
        from model_mommy.constants import ASCII_TABLE, LATIN1_TABLE, UNICODE_RANGE

        value = raw_string(10, ASCII_TABLE)
        self.assertEqual(type(value), unicode)

        value = raw_string(10, LATIN1_TABLE)
        self.assertEqual(type(value), unicode)

        value = raw_string(10, UNICODE_RANGE)
        self.assertEqual(type(value), unicode)

    def test_raw_string_with_char_table(self):
        from model_mommy.utils import raw_string
        from model_mommy.constants import ASCII_TABLE, LATIN1_TABLE

        length = 20

        value = raw_string(length, ASCII_TABLE)
        self.assertTrue(all(map(lambda c: c in ASCII_TABLE, value)))

        value = raw_string(length, LATIN1_TABLE)
        self.assertTrue(all(map(lambda c: c in LATIN1_TABLE, value)))

    def test_raw_string_with_char_range(self):
        from model_mommy.utils import raw_string
        from model_mommy.constants import ASCII_TABLE, ASCII_RANGE, LATIN1_TABLE, LATIN1_RANGE

        length = 20
        value = raw_string(length, ASCII_RANGE)
        self.assertTrue(all(map(lambda c: ASCII_RANGE[0] <= ord(c) <= ASCII_RANGE[-1], value)))

        value = raw_string(length, LATIN1_RANGE)
        self.assertTrue(all(map(lambda c: LATIN1_RANGE[0] <= ord(c) <= LATIN1_RANGE[-1], value)))

    def test_fail_raw_string_with_wrong_table_type(self):
        from model_mommy.utils import raw_string

        self.assertRaises(TypeError, lambda: raw_string(10, choice((1, False, object(), {}))))


class TestUtilsRawFileMethods(TestCase):
    def test_raw_filename_with_none_as_ext_list_param(self):
        from model_mommy.utils import raw_filename

        value = raw_filename(10, None)
        self.assertEqual(type(value), unicode)

    def test_raw_filename_with_supplied_ext_list_param(self):
        from model_mommy.utils import raw_filename
        from model_mommy.constants import FILE_EXT_LIST

        from os.path import splitext

        value = raw_filename(10, FILE_EXT_LIST)
        name, ext = splitext(value)

        self.assertTrue(ext in FILE_EXT_LIST)

    def test_raw_filename_output_type(self):
        from model_mommy.utils import raw_filename

        value = raw_filename(10)
        self.assertEqual(type(value), unicode)

    def test_raw_filename_output_length(self):
        from model_mommy.utils import raw_filename

        length = 11
        value = raw_filename(length)
        self.assertEqual(len(value), length)

        length = 22
        value = raw_filename(length)
        self.assertEqual(len(value), length)

        length = 33
        value = raw_filename(length)
        self.assertEqual(len(value), length)


class TestUtilsRawHostnameMethods(TestCase):
    def test_raw_hostname_output_type(self):
        from model_mommy.utils import raw_hostname

        value = raw_hostname(12)
        self.assertTrue(isinstance(value, basestring))


    def test_raw_hostname_output_length(self):
        from model_mommy.utils import raw_hostname

        length = 11
        value = raw_hostname(length)
        self.assertLessEqual(len(value), length)

        length = 22
        value = raw_hostname(length)
        self.assertLessEqual(len(value), length)

        length = 33
        value = raw_hostname(length)
        self.assertLessEqual(len(value), length)

    def test_raw_hostname_with_ext_list(self):
        from model_mommy.utils import raw_hostname

        ext_list = ['.com', '.com.br', '.org', '.org.br']
        value = raw_hostname(12, ext_list)
        self.assertTrue(any(map(lambda ext: value.endswith(ext), ext_list)))

        ext_list = ['.com.br']
        value = raw_hostname(12, ext_list)
        self.assertTrue(value.endswith('.com.br'))

        ext_list = ['com.br']
        value = raw_hostname(12, ext_list)
        self.assertTrue(value.endswith('.com.br'))