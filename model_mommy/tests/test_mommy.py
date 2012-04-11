# -*- coding:utf-8 -*-

import django
from django.test import TestCase
from django.db.models.fields import *

if django.VERSION < (1, 2):
    BigIntegerField = IntegerField


class TestDjangoVersinoIssues(TestCase):
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

        person_mom = Mommy(Person)
        person = person_mom.make(happy=False,
            age=20, gender='M', name='John')
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

    def test_prepare_one_should_create_but_not_persist_one_object(self):
        from model_mommy import mommy
        from model_mommy.models import Person

        person = mommy.prepare_one(Person)
        self.assertTrue(isinstance(person, Person))

        # makes sure database is clean
        self.assertEqual(Person.objects.all().count(), 0)

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

    def test_prepare_many_people(self):
        from model_mommy import mommy
        from model_mommy.models import Person

        people = mommy.prepare_many(Person)

        # prepare_many creates 5 instances by default
        self.assertEqual(len(people), 5)
        self.assertEqual(Person.objects.count(), 0)

    def test_prepare_many_people_with_params(self):
        from model_mommy import mommy
        from model_mommy.models import Person

        people = mommy.prepare_many(Person, 3, name='Mike')

        for person in people:
            self.assertTrue(person.name, 'Mike')

        self.assertEqual(Person.objects.count(), 0)

    def test_make_one_object_with_fill_null_as_true(self):
        from model_mommy import mommy
        from model_mommy.models import Person

        person = mommy.make_one(Person, fill_null=True)
        meta = person._meta
        fields = meta.fields

        for field in fields:
            name = field.name

            if field.null:
                field_value = getattr(person, name)
                self.assertIsNotNone(field_value)

    def test_prepare_one_object_with_fill_null_as_true(self):
        from model_mommy import mommy
        from model_mommy.models import Person

        person = mommy.prepare_one(Person, fill_null=True)
        meta = person._meta
        fields = meta.fields

        for field in fields:
            name = field.name

            if field.null:
                field_value = getattr(person, name)
                self.assertIsNotNone(field_value)

    def test_make_one_object_with_fill_null_as_false(self):
        from model_mommy import mommy
        from model_mommy.models import Person

        person = mommy.make_one(Person, fill_null=False)
        meta = person._meta
        fields = meta.fields

        for field in fields:
            name = field.name

            if field.null:
                field_value = getattr(person, name)
                self.assertIsNone(field_value)

    def test_prepare_one_object_with_fill_null_as_false(self):
        from model_mommy import mommy
        from model_mommy.models import Person

        person = mommy.prepare_one(Person, fill_null=False)
        meta = person._meta
        fields = meta.fields

        for field in fields:
            name = field.name

            if field.null:
                field_value = getattr(person, name)
                self.assertIsNone(field_value)


class TestMommyModelsWithRelations(TestCase):
    def test_dependent_model_creation_with_ForeignKey(self):
        from model_mommy import mommy
        from model_mommy.models import Dog, Person

        dog = mommy.make_one(Dog)
        self.assertTrue(isinstance(dog.owner, Person))

    def test_prepare_one_should_not_create_one_object(self):
        from model_mommy import mommy
        from model_mommy.models import Dog, Person

        dog = mommy.prepare_one(Dog)
        self.assertTrue(isinstance(dog, Dog))
        self.assertTrue(isinstance(dog.owner, Person))

        # makes sure database is clean
        self.assertEqual(Person.objects.all().count(), 0)
        self.assertEqual(Dog.objects.all().count(), 0)

    def test_create_many_to_many(self):
        from model_mommy import mommy
        from model_mommy.models import Store

        store = mommy.make_one(Store)
        self.assertEqual(store.employees.count(), 0)
        self.assertEqual(store.customers.count(), 0)

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
    def test_create_one_lone_penguin(self):
        from model_mommy import mommy
        from model_mommy.models import Penguin

        penguin = mommy.make_one(Penguin, fill_null=False)
        other_penguin = Penguin.objects.all()[0]

        self.assertEqual(penguin, other_penguin)
        self.assertEqual(penguin.parcel.count(), 0)
        self.assertRaises(Penguin.DoesNotExist, lambda: penguin.mate)

    def test_create_two_penguins_in_love(self):
        from model_mommy import mommy
        from model_mommy.models import Penguin

        male = mommy.make_one(Penguin)
        female = mommy.make_one(Penguin, partner=male)
        self.assertEqual(male, female.partner)
        self.assertEqual(male.mate, female)

    def test_create_a_penguin_with_many_fellows(self):
        from model_mommy import mommy
        from model_mommy.models import Penguin

        fellows = mommy.make_many(Penguin, 10, fill_null=False)
        penguin = mommy.make_one(Penguin, fill_null=False, parcel=fellows)

        parcel_count = penguin.parcel.count()
        all_but_me_count = Penguin.objects.exclude(id=penguin.id).count()
        self.assertEqual(parcel_count, all_but_me_count)


class FillNullablesTestCase(TestCase):
    def test_always_fill_nullables_if_value_provided_via_attrs(self):
        from model_mommy.mommy import Mommy
        from model_mommy.models import Person

        bio_data = 'some bio'
        mom = Mommy(Person, None)
        p = mom.make(bio=bio_data)
        self.assertTrue(p.bio in (bio_data, None))

    def test_if_nullables_are_filled_when_fill_null_is_true(self):
        from model_mommy.mommy import Mommy
        from model_mommy.models import Person

        # force value for nullable fields
        mom = Mommy(Person, fill_null=True)
        p = mom.make()
        self.assertTrue(isinstance(p.bio, basestring))


    def test_if_nullables_are_not_filled_when_fill_null_is_false(self):
        from model_mommy.mommy import Mommy
        from model_mommy.models import Person

        # force None to nullable fields
        mom = Mommy(Person, fill_null=False)
        p = mom.make()
        self.assertEqual(p.bio, None)


class FillingFromChoice(FieldFillingTestCase):
    def test_if_gender_is_populated_from_choices(self):
        from model_mommy.models import GENDER_CH

        self.assertTrue(self.person.gender in map(lambda x: x[0], GENDER_CH))
