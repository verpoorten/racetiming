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
from django.utils import timezone
from timing.tests.factories.runner import RunnerFactory
import factory.fuzzy


def generate_start_date(runner):
    return datetime.date(timezone.now().year, 9, 30)


class RankingFactory(factory.DjangoModelFactory):

    class Meta:
        model = 'timing.Ranking'

    runner = factory.SubFactory(RunnerFactory)
    checkin = factory.LazyAttribute(generate_start_date)
    attention = False
    accurate_time = None
