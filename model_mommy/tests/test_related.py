# -*- coding:utf-8 -*-

from django.test import TestCase
from django.db.models.fields.related import *


class TestDummyRelationModel(TestCase):

    def test_model_has_no_fields_but_pk(self):
        from django.db.models.fields import AutoField
        from model_mommy.models import DummyRelationModel

        fields = DummyRelationModel._meta.fields

        self.assertEqual(len(fields), 1)
        self.assertTrue(isinstance(fields[0], AutoField))


class TestFillingOneToOneField(TestCase):

    def test_create_model_with_OneToOneField(self):
        from model_mommy.models import DummyOneToOneModel
        from model_mommy.models import DummyRelationModel
        from model_mommy import mommy

        dummy_one_to_one_model = mommy.make_one(DummyOneToOneModel)
        one_to_one_field = dummy_one_to_one_model.\
            _meta.get_field('one_to_one_field')

        self.assertTrue(isinstance(one_to_one_field, OneToOneField))
        self.assertTrue(
            isinstance(
                dummy_one_to_one_model.one_to_one_field, DummyRelationModel))


class TestFillingM2MField(TestCase):

    def test_create_model_with_M2MField(self):
        from model_mommy.models import DummyM2MModel
        from model_mommy.models import DummyRelationModel
        from model_mommy import mommy

        dummy_m2m_model = mommy.make_one(DummyM2MModel)
        m2m_field = DummyM2MModel._meta.get_field('m2m_field')

        self.assertTrue(isinstance(m2m_field, ManyToManyField))
        self.assertEqual(DummyRelationModel.objects.count(), 5)
        self.assertEqual(dummy_m2m_model.m2m_field.count(), 5)

    def test_prepare_model_with_M2MField_does_not_hit_database(self):
        from model_mommy.models import DummyM2MModel
        from model_mommy.models import DummyRelationModel
        from model_mommy import mommy

        dummy_m2m_model = mommy.prepare_one(DummyM2MModel)

        # relation is not created if parent model is not persisted
        self.assertEqual(DummyRelationModel.objects.count(), 0)
        self.assertRaises(ValueError, lambda: dummy_m2m_model.m2m_field)
