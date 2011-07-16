# -*- coding:utf-8 -*-

from django.test import TestCase
from django.db.models.fields import *

class SimpleExtendMommy(TestCase):

    def test_simple_extended_mommy_example(self):
        from model_mommy.mommy import Mommy
        from model_mommy.models import Person

        class Aunt(Mommy):
            pass

        aunt = Aunt()
        self.cousin = aunt.make(Person)

    def test_overwriting_happy_field_behavior(self):
        from model_mommy.mommy import Mommy
        from model_mommy.models import Person

        class SadPeopleMommy(Mommy):
            def value_for_happy(self, field):
                return False

        sad_people_mommy = SadPeopleMommy()
        person = sad_people_mommy.make(Person)

        # making sure this person is sad >:D
        self.assertEqual(person.happy, False)

    def test_overwriting_boolean_field_behavior(self):
        from model_mommy.mommy import Mommy
        from model_mommy.models import Person

        class SadPeopleMommy(Mommy):
            def value_for_booleanfield(self, field):
                return False

        sad_people_mommy = SadPeopleMommy()
        person = sad_people_mommy.make(Person)

        # making sure this person is sad >:D
        self.assertEqual(person.happy, False)

    def test_overwriting_foreignkey_behavior(self):
        from model_mommy.mommy import Mommy
        from model_mommy.models import Person


