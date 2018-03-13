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
from timing.models.race import Race
from timing.tests.factories.race import RaceFactory
from timing.models.enums import gender
import datetime
from django.utils import timezone


class RaceTest(TestCase):
    def test_find_by_id(self):
        self.assertIsNone(Race.find_by_id(-1))
        a_race = RaceFactory()
        self.assertEqual(Race.find_by_id(a_race.id), a_race)

    def test_find_all(self):
        self.assertCountEqual(Race.find_all(), [])
        races = []
        cpt = 1
        while cpt < 4:
            races.append(RaceFactory(race_start=datetime.date(timezone.now().year, 1, cpt) ))
            cpt = cpt + 1

        self.assertCountEqual(Race.find_all(), races)

    def test_find_all_current(self):

        race_1 = RaceFactory(current=True)
        race_2 = RaceFactory(current=False)
        race_3 = RaceFactory(current=True)
        self.assertCountEqual(Race.find_all_current(), [race_1, race_3])

    def test_find_all_current_pre_registration(self):
        race_1 = RaceFactory(current=True, pre_registration=False, ended=True)
        self.assertCountEqual(Race.find_all_current_pre_registration(), [])
        race_1.pre_registration=True
        race_1.save()
        self.assertCountEqual(Race.find_all_current_pre_registration(), [])
        race_1.ended=False
        race_1.save()
        self.assertCountEqual(Race.find_all_current_pre_registration(), [race_1])

    def test_find_ended_race(self):
        self.assertCountEqual(Race.find_ended_race(), [])
        race_1 = RaceFactory(current=False, ended=False)
        self.assertCountEqual(Race.find_ended_race(), [])
        race_1.current = True
        race_1.save()
        self.assertCountEqual(Race.find_ended_race(), [])
        race_1.ended = True
        race_1.save()
        self.assertCountEqual(Race.find_ended_race(), [race_1])





