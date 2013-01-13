# Note about Mommy
Mommy uses fuzzy testing techniques. If you don't know what that is,
read here: http://en.wikipedia.org/wiki/Fuzz_testing

# Creating objects for testing shouldn't hurt

model_mommy is a tool for creating good model objects for testing in Django, inspired in ruby's ObjectDaddy and FactoryGirl.

All values are basically generated according to the django model field type using instrospection.

#Installing

    pip install model_mommy

## Basic Usage

If you have a model like this in your app:

    class Kid(models.Model):
        happy = models.BooleanField()
        name = models.CharField(max_length=30)
        age = models.IntegerField()
        bio = models.TextField()
        wanted_games_qtd = models.BigIntegerField()
        birthday = models.DateField()
        appointment = models.DateTimeField()

just call mommy =):

    from model_mommy import mommy
    from model_mommy.models import Kid

    kid = mommy.make_one(Kid)

and your object is created! No boring attribute passing like 'foobar' every damn time. You
can check your generated model like this:

    assert kid.happy in (True or False)
    >>> True
    assert isinstance(kid.name, basestring)
    >>> True
    ... etc

mommy also handles relationships. Suppose the kid has a dog:

    class Dog(models.Model):
        owner = models.ForeignKey('Kid')
        kind = models.CharField(max_length=50, blank=True)

let's create a dog:

    rex = mommy.make_one(Dog)

the Kid instance will be created automatically.

You can also specify values for one or more attribute.

    another_kid = mommy.make_one(Kid, age=3)
    assert another_kid.age == 3  # all other kid attribute values are random

In both examples above, the kid and rex objects are persisted in the database.
If you don't need a persisted object, mommy can handle this for you as well:

    from model_mommy import mommy
    from model_mommy.models import Kid

    kid = mommy.prepare_one(Kid)
    assert Kid.objects.count() == 0

It works like make_one, but it doesn't persist the instance **nor** related fields.

## Note 1

Related fields are not populated by default if not required (null=True). This behavior
helps avoiding problems like recursive loops and the "diamond effect".

How's that?

    from django.db.models import Model
    from model_mommy import mommy

    class Person(Model):
        gender = models.CharField(max_length=1, choices=((0, 'M'), (1, 'F'))
        name = models.CharField(max_length=100)
        age = models.IntegerField()
        partner = models.ForeignKey('Person', null=True)

    person = mommy.make(Person)
    assert person.partner is None

## Note 2

A field with blank=True or with a declared default value has a 25% chance of being left blank
or with the default value. Same behavior goes for fields with null=True.

## Not so Basic Usage

Model instances can also be generated from Mommy factories. Make your mass producer mom like this:

    from model_mommy.mommy import Mommy
    from model_mommy.models import Kid

    mom = Mommy(Kid)
    first_kid = mom.make()
    second_kid = mom.make()
    third_kid = mom.make()

    assert isinstance(first_kid, Kid)
    assert isinstance(second_kid, Kid)
    assert isinstance(third_kid, Kid)

This kind of construction is more efficient than mommy.make_one(Model).
So, if you need to create a lot of instances of the same model, this
approach is good for you, or...

    from model_mommy.mommy import Mommy
    from model_mommy.models import Kid

    mom = Mommy(Kid)
    kids = mom.make_many(3)
    assert len(kids) == 3

## Extending Mommy

All attributes used to automatically populate mommy generated instances
are created with generator methods from the **model_mommy/base.Base** class. If you want
a specific field to be populated with a value different from the default
generator, you must extend the Mommy class to get this behavior.

Let's see a example:

    class BabeMommy(Mommy):
        def value_for_agefield(self, field):
            return 0

    mom = BabeMommy(Kid)
    baby = mom.make_one()
    assert(baby.age == 0)

The naming convention for the generator methods is **value_for_<fieldname>field** and
**value_for_<fieldtype>**. If you want to overwrite the behavior for a field type,
the example above would look like this:

    from random import choice
    from model_mommy.models import Kid
    from model_mommy.mommy import Mommy

    int_range = range(0, 10)

    class CustomMommy(Mommy):
        def value_for_integerfield(self, field):
            return choice(int_range)

    mom = CustomMommy(Kid)
    kid = mom.make_one()

    assert(kid.wanted_games_qtd in int_range)

The example above overwrites the behavior for the generator of all integer fields.

## Recipes

If you wish to test a model with a set of specific values, you can simply pass
the attribute values you wish to the building method.

    from model_mommy import mommy

    person = mommy.make_one(Person, name='john', age=15)
    assert person.name == 'john'
    assert person.age == 15

In the example above, your instance is guaranteed to have the attributes name and age set to 'john' and 15.
Another approach would look like this:

    from model_mommy import mommy

    attrs = {'name': 'john', 'age': 15}
    person = mommy.make_one(Person, **attrs)
    assert person.name == 'john'
    assert person.age == 15

A third approach would look like this:

    from model_mommy import mommy

    def attrs():
        return {'name': 'john', 'age': 15}

    person = mommy.make_one(Person, **attrs())
    assert person.name == 'john'
    assert person.age == 15

This third approach is useful if you wish to set distinct relation attributes,
as a foreignkey, for many fields.
An actual example:

    from model_mommy import mommy

    def attrs():
        return {
            'partner': mommy.make_one(Person)
        }

    # each person with a different partner
    person_with_partner_1 =  mommy.make_one(Person, **attrs())
    person_with_partner_2 =  mommy.make_one(Person, **attrs())
    person_with_partner_3 =  mommy.make_one(Person, **attrs())

The example above would not work with **make_many** and **prepare_many**
as attrs is evaluated only once. In real code, you DO NOT WANT to do the
above example with make/prepare_many as _random similar multiple_ data is usually
a bad idea for testing.

## For contributors

If you want to contribute, fork the project and send your fixes. Here are a few guidelines for you:

 * Write tests for all code you commit (untested code might be refused)
 * Check your code coverage
 * Follow pep8 guidelines

For more examples, see tests.

You can also override the value type mapping, if you want all values from a given Field to be populate with a value you prefer.

Do it like this:

    from random import randint
    from model_mommy import Mommy

    class MyMommy(Mommy):
        def value_for_integerfield(self, field):
            return randint(0, 126)

## Doubts? Loved it? Hated it? Suggestions?

Mail us!:

 *  vanderson.mota **at** gmail **dot** com
 *  italo.maia **at** gmail **dot** com

##Currently supports the fields:

 * BooleanField
 * NullBooleanField
 * SmallIntegerField
 * PositiveSmallIntegerField
 * IntegerField
 * PositiveIntegerField
 * BigIntegerField
 * FloatField
 * DecimalField
 * CommaSeparatedIntegerField
 * DateField
 * TimeField
 * DateTimeField
 * IPAddressField
 * CharField
 * SlugField
 * TextField
 * URLField
 * FileField
 * ImageField
 * EmailField
