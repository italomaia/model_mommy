# -*- coding:utf-8 -*-

import sys
from string import letters
from random import choice, randint
from datetime import date
from decimal import Decimal

from generators import Mapper


def make_one(model, **attrs):
    mapper = Mapper(model)
    return mapper.make(attrs)


def make_many(model, qty=5, **attrs):
    mapper = Mapper(model)
    return [mapper.make(attrs) for i in range(qty)]


def prepare_one(model, **attrs):
    mapper = Mapper(model)
    return mapper.make(attrs, commit=False)


def prepare_many(model, **attrs):
    mapper = Mapper(model)
    return [mapper.make(attrs, commit=False) for i in range(qty)]
