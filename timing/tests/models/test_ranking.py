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
from django.test import TestCase
from timing.models.runner import Runner
from timing.tests.factories.race import RaceFactory
from timing.tests.factories.runner import RunnerFactory
from timing.tests.factories.ranking import RankingFactory
from django.utils import timezone

NUMBER_1000 = 1000
NUMBER_1001 = 1001
NUMBER_1002 = 1002
NUMBER_1003 = 1003


class RankingTest(TestCase):

    def test_duplicated(self):
        a_race = RaceFactory()
        a_runner = RunnerFactory(race=a_race)
        ranking_1 = RankingFactory(runner=a_runner)
        ranking_2 = RankingFactory(runner=a_runner)


