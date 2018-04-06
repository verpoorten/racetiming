##############################################################################
#
#    Racetiming is an application designed to manage ranking during running
#    competition.
#
#    Copyright (C) 2018 Leïla Verpoorten
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    A copy of this license - GNU General Public License - is available
#    at the root of the source code of this program.  If not,
#    see http://www.gnu.org/licenses/.
#
##############################################################################
import datetime
import factory
import factory.fuzzy
import string
from django.utils import timezone
import operator
from timing.models.enums.gender import GENDER_CHOICES


def generate_start_date(category):
    return datetime.date(timezone.now().year, 9, 30)


def generate_end_date(cateogry):
    return datetime.date(timezone.now().year+1, 9, 30)


class CategoryFactory(factory.DjangoModelFactory):
    class Meta:
        model = 'timing.Category'

    label = factory.Sequence(lambda n: 'Category - %d' % n)
    start_date = factory.LazyAttribute(generate_start_date)
    end_date = factory.LazyAttribute(generate_end_date)
    gender = factory.Iterator(GENDER_CHOICES, getter=operator.itemgetter(0))

