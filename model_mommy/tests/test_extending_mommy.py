# -*- coding:utf-8 -*-

from django.test import TestCase
from django.db.models.fields import *

class SimpleExtendMommy(TestCase):

    def test_simple_extended_mommy_example(self):
        from model_mommy.mommy import Mommy
        from model_mommy.models import Person

        class Aunt(Mommy):
            pass

        aunt = Aunt(Person)
        self.cousin = aunt.make_one()

    def test_type_mapping_overwriting_boolean_model_behavior(self):
        from model_mommy.mommy import Mommy
        from model_mommy.models import Person

        class SadPeopleMommy(Mommy):
            def __init__(self, model):
                super(SadPeopleMommy, self).__init__(model)
                self.type_mapping.update({
                    BooleanField: lambda: False
                })

        sad_people_mommy = SadPeopleMommy(Person)
        person = sad_people_mommy.make_one()

        # making sure this person is sad >:D
        self.assertEqual(person.happy, False)


class LessSimpleExtendMommy(TestCase):

    def test_fail_no_field_attr_string_to_generator_required(self):
        from model_mommy.mommy import Mommy
        from model_mommy.models import Person

        gen_oposite = lambda x: not x
        gen_oposite.required = ['house']

        class SadPeopleMommy(Mommy):
            attr_mapping = {'happy': gen_oposite}

        mom = SadPeopleMommy(Person)
        self.assertRaises(AttributeError, lambda: mom.make_one())

    def test_string_to_generator_required(self):
        from model_mommy.mommy import Mommy
        from model_mommy.models import Person

        gen_oposite = lambda default: not default
        gen_oposite.required = ['default']

        class SadPeopleMommy(Mommy):
            attr_mapping = {'happy': gen_oposite}

        happy_field = Person._meta.get_field('happy')
        mom = SadPeopleMommy(Person)
        person = mom.make_one()
        self.assertEqual(person.happy, not happy_field.default)

    def test_fail_pass_non_string_to_generator_required(self):
        from model_mommy.mommy import Mommy
        from model_mommy.models import Person

        gen_age = lambda x: 10

        class MyMommy(Mommy):
            attr_mapping = {'age': gen_age}

        mom = MyMommy(Person)

        # for int
        gen_age.required = [10]
        self.assertRaises(ValueError, lambda: mom.make_one())

        # for float
        gen_age.required = [10.10]
        self.assertRaises(ValueError, lambda: mom.make_one())

        # for iterable
        gen_age.required = [[]]
        self.assertRaises(ValueError, lambda: mom.make_one())

        # for iterable/dict
        gen_age.required = [{}]
        self.assertRaises(ValueError, lambda: mom.make_one())

        # for boolean
        gen_age.required = [True]
        self.assertRaises(ValueError, lambda: mom.make_one())
