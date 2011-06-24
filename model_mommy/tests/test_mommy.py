# -*- coding:utf-8 -*-

from datetime import date, datetime
from decimal import Decimal

from django.db.models.fields import *
import django

if django.VERSION < (1, 2):
    BigIntegerField = IntegerField

from django.test import TestCase


class TestDjangoVersionIssues(TestCase):
    def test_if_bigintegerfield_works_for_v1_1(self):
        from model_mommy.models import BigIntegerField

        if django.VERSION < (1, 2):
            self.assertEqual(BigIntegerField, IntegerField)
        else:
            self.assertNotEqual(BigIntegerField, IntegerField)


class FieldFillingTestCase(TestCase):

    def setUp(self):
        from model_mommy import mommy
        from model_mommy.models import Person

        self.person = mommy.make_one(Person)


class FieldFillingWithParameterTestCase(TestCase):

    def test_simple_create_person_with_parameters(self):
        from model_mommy import mommy
        from model_mommy.models import Person

        kid = mommy.make_one(Person, happy=True, age=10, name='Mike')
        self.assertEqual(kid.age, 10)
        self.assertEqual(kid.happy, True)
        self.assertEqual(kid.name, 'Mike')

    def test_create_person_from_factory_using_paramters(self):
        from model_mommy.mommy import Mommy
        from model_mommy.models import Person

        person_mom = Mommy()

        person = person_mom.make(Person, {
            'happy': False,
            'age': 20,
            'gender': 'M',
            'name': 'John'
        })

        self.assertEqual(person.age, 20)
        self.assertEqual(person.happy, False)
        self.assertEqual(person.name, 'John')
        self.assertEqual(person.gender, 'M')


class TestMommyAPI(TestCase):

    def test_make_one_should_create_one_object(self):
        from model_mommy import mommy
        from model_mommy.models import Person

        person = mommy.make_one(Person)
        self.assertTrue(isinstance(person, Person))

        # makes sure there's someone in the database
        self.assertEqual(Person.objects.all().count(), 1)

        # makes sure it is the person we created
        self.assertEqual(Person.objects.all()[0].id, person.id)

    def test_make_many_people(self):
        from model_mommy import mommy
        from model_mommy.models import Person

        people = mommy.make_many(Person)

        # make_many creates 5 instances by default
        self.assertEqual(len(people), 5)
        self.assertEqual(Person.objects.count(), 5)

        # only what we created is in the database
        for person in people:
            Person.objects.get(pk=person.id)

    def test_make_many_people_with_params(self):
        from model_mommy import mommy
        from model_mommy.models import Person

        people = mommy.make_many(Person, 3, name='Mike')

        for person in people:
            self.assertTrue(person.name, 'Mike')

        for person in Person.objects.all():
            self.assertTrue(person.name, 'Mike')


class TestMommyModelsWithRelations(TestCase):

    def test_dependent_model_creation_with_ForeignKey(self):
        from model_mommy import mommy
        from model_mommy.models import Dog, Person

        dog = mommy.make_one(Dog)
        self.assertTrue(isinstance(dog.owner, Person))

    def test_dependent_model_creation_with_ForeignKey(self):
        from model_mommy import mommy
        from model_mommy.models import Dog, Person

        dog = mommy.make_one(Dog)
        self.assertTrue(isinstance(dog.owner, Person))

    def test_create_many_to_many(self):
        from model_mommy import mommy
        from model_mommy.models import Store

        store = mommy.make_one(Store)
        self.assertEqual(store.customers.count(), 0)
        self.assertEqual(store.employees.count(), 5)

    def test_provide_initial_to_many_to_many(self):
        from model_mommy.models import Person, Store
        from model_mommy import mommy

        employees = mommy.make_many(Person, 3)
        customers = mommy.make_many(Person, 20)
        store = mommy.make_one(Store, employees=employees, customers=customers)

        self.assertEqual(store.employees.count(), 3)
        self.assertEqual(store.customers.count(), 20)

        for employee in employees:
            store.employees.get(pk=employee.id)


class TestAutoRefPattern(TestCase):
    'Spooky!'
    pass


class FillNullablesTestCase(TestCase):

    def test_always_fill_nullables_if_value_provided_via_attrs(self):
        from model_mommy.mommy import Mommy
        from model_mommy.models import Person

        bio_data = 'some bio'
        mom = Mommy(False)
        p = mom.make(Person, {'bio': bio_data})
        self.assertEqual(p.bio, bio_data)

    def test_if_nullables_are_filled_when_fill_nullables_is_true(self):
        from model_mommy.mommy import Mommy
        from model_mommy.models import Person

        mom = Mommy(True)
        p = mom.make(Person)
        self.assertTrue(isinstance(p.bio, basestring))

    def test_if_nullables_are_not_filled_when_fill_nullables_is_false(self):
        from model_mommy.mommy import Mommy
        from model_mommy.models import Person

        mom = Mommy(False)
        p = mom.make(Person)
        self.assertTrue(p.bio == None)


class FillingFromChoice(FieldFillingTestCase):

    def test_if_gender_is_populated_from_choices(self):
        from model_mommy.models import GENDER_CH

        self.assertTrue(self.person.gender in map(lambda x: x[0], GENDER_CH))
