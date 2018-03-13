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
from django.utils import timezone

NUMBER_1000 = 1000
NUMBER_1001 = 1001
NUMBER_1002 = 1002
NUMBER_1003 = 1003


class RunnerTest(TestCase):

    def test_find_all(self):
        self.assertCountEqual(Runner.find_all(), [])
        runners = []
        cpt = 1
        while cpt < 4:
            runners.append(RunnerFactory(number=cpt))
            cpt = cpt + 1

        self.assertCountEqual(Runner.find_all(), runners)

    def test_find_by_id(self):
        self.assertIsNone(Runner.find_by_id(-1))
        a_runner = RunnerFactory(number=NUMBER_1003)
        self.assertEqual(Runner.find_by_id(a_runner.id), a_runner)

    def test_find_by_number(self):
        yr = timezone.now().year
        self.assertIsNone(Runner.find_by_number(None))
        self.assertIsNone(Runner.find_by_number(-1))
        a_runner = RunnerFactory(number=NUMBER_1001)
        self.assertEqual(Runner.find_by_number(NUMBER_1001), a_runner)

    def test_find_by_number_started_race_no_result(self):
        self.assertIsNone(Runner.find_by_number_started_race(None))
        self.assertIsNone(Runner.find_by_number_started_race(-1))
        a_runner = RunnerFactory(number=None)
        self.assertIsNone(Runner.find_by_number_started_race(NUMBER_1000))
        a_runner.number = NUMBER_1000
        a_runner.save()
        self.assertIsNone(Runner.find_by_number_started_race(NUMBER_1000))

    def test_find_by_number_started_race(self):
        a_race = RaceFactory(accurate_race_start=timezone.now())
        a_runner = RunnerFactory(number=NUMBER_1002, race=a_race)
        self.assertEqual(Runner.find_by_number_started_race(NUMBER_1002), a_runner)