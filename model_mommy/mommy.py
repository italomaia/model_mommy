# -*- coding:utf-8 -*-

from .base import Base


def make_one(model, **attrs):
    """
    Creates a persisted instance from a given model its associated models.
    It fill the fields with random values or you can specify
    which fields you want to define its values by yourself.

    """
    fill_null = None
    if 'fill_null' in attrs:
        fill_null = attrs.pop('fill_null')

    mommy = Mommy(model, fill_null=fill_null)
    return mommy.make(**attrs)


def prepare_one(model, **attrs):
    """
    Creates a BUT DOESN'T persist an instance from a given model
    its associated models.
    It fill the fields with random values or you can specify
    which fields you want to define its values by yourself.

    """
    fill_null = None
    if 'fill_null' in attrs:
        fill_null = attrs.pop('fill_null')

    mommy = Mommy(model, fill_null=fill_null)
    return mommy.prepare(**attrs)


def make_many(model, qty=5, **attrs):
    fill_null = None
    if 'fill_null' in attrs:
        fill_null = attrs.pop('fill_null')

    mommy = Mommy(model, fill_null=fill_null)
    return [mommy.make(**attrs) for i in range(qty)]


def prepare_many(model, qty=5, **attrs):
    fill_null = None
    if 'fill_null' in attrs:
        fill_null = attrs.pop('fill_null')

    mommy = Mommy(model, fill_null=fill_null)
    return [mommy.prepare(**attrs) for i in range(qty)]


class Mommy(Base):
    def make_one(self, **kw):
        return super(Mommy, self).make(**kw)
