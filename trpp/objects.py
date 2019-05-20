'''
Internal types that represent parts of a parsed plan.
'''

from collections import namedtuple

Plan = namedtuple('Plan', ('title', 'weights', 'days'))
WeightInfo = namedtuple('WeightInfo', ('name', 'weight'))
Day = namedtuple('Day', ('title', 'exercises'))
Exercise = namedtuple('Exercise', ('name', 'blocks'))
RatioSetBlock = namedtuple('RatioSetBlock', ('ratio', 'reps', 'count'))
SimpleSetBlock = namedtuple('SimpleSetBlock', ('reps', 'count'))
