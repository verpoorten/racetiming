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
import factory
import factory.fuzzy
import operator
from timing.models.enums.unit import UNIT_CHOICES


class RaceFactory(factory.DjangoModelFactory):
    class Meta:
        model = 'timing.Race'

    description = factory.Sequence(lambda n: 'description - %d' % n)

    distance = factory.fuzzy.FuzzyDecimal(0, 100)
    unit = factory.Iterator(UNIT_CHOICES, getter=operator.itemgetter(0))
    race_start = None
    accurate_race_start = None
    current = False
    price = 0
    pre_registration = False
    presale_price = None
    bank_account = factory.Sequence(lambda n: 'bank - %d' % n)
    ended = False

