# -*- coding:utf-8 -*-

from django.test import TestCase


class SimpleExtendMommy(TestCase):

    def test_simple_extended_mommy_example(self):
        from model_mommy.mommy import Mommy
        from model_mommy.models import Person

        class Aunt(Mommy):
            pass

        aunt = Aunt(Person)
        self.cousin = aunt.make()

    def test_type_mapping_overwriting_boolean_model_behavior(self):
        from random import randint
        from model_mommy.mommy import Mommy
        from model_mommy.models import Person

        max_age = 12

        class YoungPeopleMommy(Mommy):

            def value_for_agefield(self, field):
                return randint(0, max_age)

        young_people_mommy = YoungPeopleMommy(Person)
        person = young_people_mommy.make()

        # making a young person
        self.assertLessEqual(person.age, max_age)
