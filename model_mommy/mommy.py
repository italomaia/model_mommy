# -*- coding:utf-8 -*-

from .base import Mommy


def make_one(model, **attrs):
    """
    Creates a persisted instance from a given model its associated models.

    Fields from the model instance are filled with random valid data
    according with each type.

    Keyword arguments:
    fill_null -- set to True and no field shall be null. Set to false for
    otherwise. Do not set and some null fields will be null, some won't.

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

    Fields from the model instance are filled with random valid data
    according with each type.

    Keyword arguments:
    fill_null -- set to True and no field shall be null. Set to false for
    otherwise. Do not set and some null fields will be null, some won't.

    """
    fill_null = None
    if 'fill_null' in attrs:
        fill_null = attrs.pop('fill_null')

    mommy = Mommy(model, fill_null=fill_null)
    return mommy.prepare(**attrs)


def make_many(model, qty=5, **attrs):
    """
    Thin wrapper around make_one. Makes a list of model instances.

    Fields from the model instance are filled with random valid data
    according with each type.

    Keyword arguments:
    fill_null -- set to True and no field shall be null. Set to false for
    otherwise. Do not set and some null fields will be null, some won't.
    qty -- how many instances you want.

    """
    return [make_one(model, **attrs) for i in range(qty)]


def prepare_many(model, qty=5, **attrs):
    """
    Thin wrapper around prepare_one. Makes a list of model instances,
    but do not persist any.

    Fields from the model instance are filled with random valid data
    according with each type.

    Keyword arguments:
    fill_null -- set to True and no field shall be null. Set to false for
    otherwise. Do not set and some null fields will be null, some won't.
    qty -- how many instances you want.

    """
    return [prepare_one(model, **attrs) for i in range(qty)]
