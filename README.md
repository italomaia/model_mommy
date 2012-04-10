# Creating objects for testing shouldn't hurt

model_mommy is a tool for creating objects for testing in Django, inspired in ruby's ObjectDaddy and FactoryGirl.
It generate the values according with the field type, but i will add support to custom values as well.

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


and your object is created! No boring attributes passing like 'foobar' every damn time.


mommy also handles relationships. Suppose the kid has a dog:

    class Dog(models.Model):
        owner = models.ForeignKey('Kid')

when you do:

    rex = mommy.make_one(Dog)

it will also create the Kid, automatically.

You can also specify values for one or more attribute.

    another_kid = mommy.make_one(Kid, age = 3)
    assert another_kid.age == 3

But, if don't need a persisted object, mommy can handle this for you as well:

    from model_mommy import mommy
    from model_mommy.models import Kid

    kid = mommy.prepare_one(Kid)

It works like make_one, but like was said, it doesn't persist the instance nor related fields.

## Note 1

ForeignKey and OneToOne fields are not populated by default if null=True. This behavior
helps avoiding problems with recursive loops and the "diamond effect".

## Not so Basic Usage

Model instances can also be generated from Mommy factories. Make your mass producer mom like this:

    from model_mommy.mommy import Mommy
    from model_mommy.models import Kid

    mom = Mommy(Kid)
    first_kid = mom.make()
    second_kid = mom.make()
    third_kid = mom.make()

Note that this kind of construction is more efficient than mommy.make_one(Model),
so, if you need to create a lot of instances, this might be a nice approach, or...

    from model_mommy.mommy import Mommy
    from model_mommy.models import Kid

    mom = Mommy(Kid)
    kids = mom.make_many(3)
    assert len(kids) == 3

## Extending Mommy

All attributes used to automatically populate mommy generated instances
are created with generators from **model_mommy/generators.py**. If you want
a specific field to be populated with a generator different from the default
generator, you must extend the Mommy class to get this behavior.
Let's see a example:

    from random import choice
    from model_mommy.models import Kid
    from model_mommy.mommy import Mommy

    a_lot_of_games = range(30, 100)

    class HardGamerMommy(Mommy):
        def value_for_wanted_games_qtdfield(self, field):
            return choice(a_lot_of_games)

    mom = HardGamerMommy(Kid)
    kid = mom.make_one()
    assert(kid.wanted_games_qtd in a_lot_of_games)

Note that you can also create your own generator.

## Your Own Generator

A generator is just a simple method which receives a field as argument.
Let's see a dead simple example:

    class BabeMommy(Mommy):
        def value_for_agefield(self, field):
            return 0

    mom = BabeMommy(Kid)
    baby = mom.make_one()
    assert(baby.age == 0)

## For contributors

If you want to contribute with model_mommy, fork the project. Here are a few guidelines for you:

 * Write tests for all code you commit (untested code might be refused)
 * Check your tests coverage
 * Follow pep8 guidelines

For more examples, see tests.

You can also override the type_mapping, if you want to all values from a given Field to be populate with a value you prefer.
To it like this:

    class TimeCopMommy(Mommy):
        def __init__(self, model, fill_nullables=True):
            super(Mommy, self).__init__(model, fill_nullables)
            self.type_mapping[DateField] = datetime.date(2011, 02, 02)

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
 * EmailField
