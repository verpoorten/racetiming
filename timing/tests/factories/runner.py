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
from timing.tests.factories.category import CategoryFactory
from timing.tests.factories.race import RaceFactory
import factory.fuzzy

def generate_start_date(runner):
    return datetime.date(timezone.now().year, 9, 30)



class RunnerFactory(factory.DjangoModelFactory):
    class Meta:
        model = 'timing.Runner'


    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    gender =  factory.Iterator(GENDER_CHOICES,
                               getter=operator.itemgetter(0))
    birth_date = factory.LazyAttribute(generate_start_date)
    number = factory.fuzzy.FuzzyInteger(1, 5)
    category = factory.SubFactory(CategoryFactory)
    race = factory.SubFactory(RaceFactory)
    medical_consent = False
