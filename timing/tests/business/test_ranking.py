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
from timing.tests.factories.race import RaceFactory
from timing.tests.factories.ranking import RankingFactory
from timing.tests.factories.runner import RunnerFactory
from timing.tests.factories.category import CategoryFactory
from django.utils import timezone
from timing.business.ranking import get_nb_finishers_by_club_order_by_desc_nb, _get_race_finisher_categories, _get_first_finishers_by_race_and_category
import datetime
from timing.models.enums.gender import MALE, FEMALE

CLUB1 = "Club1"
CLUB2 = "Club2"


class RankingTest(TestCase):
    def setUp(self):
        now = timezone.now()
        self.active_race_10km = RaceFactory(current=True,
                                       accurate_race_start=now)
        self.active_race_5km = RaceFactory(current=True,
                                      accurate_race_start=now)
        self.active_race_no_ranking = RaceFactory(current=True,
                                             accurate_race_start=now)
        self.category_female_a3 = CategoryFactory(start_date=datetime.date(1800, 1, 1), end_date=datetime.date(1958, 12, 31),
                                             gender=FEMALE)
        self.category_female_a2 = CategoryFactory(start_date=datetime.date(1959, 1, 1), end_date=datetime.date(1980, 12, 31),
                                             gender=FEMALE)
        self.category_female_a1 = CategoryFactory(start_date=datetime.date(1981, 1, 1), end_date=datetime.date(2020, 12, 31),
                                             gender=FEMALE)
        self.category_female_v3 = CategoryFactory(start_date=datetime.date(1800, 1, 1), end_date=datetime.date(1958, 12, 31),
                                             gender=MALE)
        self.category_female_v2 = CategoryFactory(start_date=datetime.date(1959, 1, 1), end_date=datetime.date(1980, 12, 31),
                                             gender=MALE)
        self.category_female_v1 = CategoryFactory(start_date=datetime.date(1981, 1, 1), end_date=datetime.date(2020, 12, 31),
                                             gender=MALE)

    def test_get_first_finishers_by_race_and_category(self):
        cpt = 1
        rankings = []
        finishers_expected = []
        while cpt <= 10:
            a_runner = RunnerFactory(race=self.active_race_10km, birth_date=datetime.date(1948, 12, 31), gender=FEMALE, number=cpt)
            if cpt <= 3:
                finishers_expected.append(a_runner)
            rankings.append(RankingFactory(runner=a_runner, checkin=timezone.now()))
            cpt += 1
        self.assertCountEqual(_get_first_finishers_by_race_and_category(rankings), finishers_expected)

    def test_get_race_finisher_categories(self):
        a_runner_a3 = RunnerFactory(race=self.active_race_10km, birth_date=datetime.date(1948, 12, 31), gender=FEMALE, number=1)
        a_runner_a2 = RunnerFactory(race=self.active_race_10km, birth_date=datetime.date(1968, 12, 31), gender=FEMALE, number=2)
        a_runner_a1 = RunnerFactory(race=self.active_race_10km, birth_date=datetime.date(1998, 12, 31), gender=FEMALE, number=3)

        a_runner_v3 = RunnerFactory(race=self.active_race_10km, birth_date=datetime.date(1948, 12, 31), gender=MALE, number=4)
        a_runner_v2 = RunnerFactory(race=self.active_race_10km, birth_date=datetime.date(1968, 12, 31), gender=MALE, number=5)
        a_runner_v1 = RunnerFactory(race=self.active_race_10km, birth_date=datetime.date(1998, 12, 31), gender=MALE, number=6)

        self.assertCountEqual(_get_race_finisher_categories(None), [])
        a_ranking_a3 = RankingFactory(runner=a_runner_a3, checkin=timezone.now())

        self.assertCountEqual(_get_race_finisher_categories([a_ranking_a3]), [a_runner_a3.category])
        a_ranking_a2 = RankingFactory(runner=a_runner_a2, checkin=timezone.now())
        a_ranking_a1 = RankingFactory(runner=a_runner_a1, checkin=timezone.now())
        self.assertCountEqual(_get_race_finisher_categories([a_ranking_a3,a_ranking_a2,a_ranking_a1]), [a_runner_a3.category, a_runner_a2.category, a_runner_a1.category])
        a_ranking_v3 = RankingFactory(runner=a_runner_v3, checkin=timezone.now())
        self.assertCountEqual(_get_race_finisher_categories([a_ranking_a3,a_ranking_a2,a_ranking_a1, a_ranking_v3]),
                              [a_runner_a3.category, a_runner_a2.category, a_runner_a1.category, a_runner_v3.category])

    def test_get_nb_finishers_by_club_order_by_desc_nb(self):
        cpt = 1
        while cpt <= 5:
            a_runner = RunnerFactory(race=self.active_race_10km, number=cpt, club=CLUB1)
            RankingFactory(runner=a_runner, checkin=timezone.now())

            a_runner = RunnerFactory(race=self.active_race_5km, number=cpt+10, club=CLUB2)
            RankingFactory(runner=a_runner, checkin=timezone.now())

            RunnerFactory(race=self.active_race_no_ranking, number=cpt+100, club="Club3")

            cpt += 1

        while cpt <= 8:
            a_runner = RunnerFactory(race=self.active_race_10km, number=cpt, club=CLUB1)
            if cpt < 8:
                RankingFactory(runner=a_runner, checkin=timezone.now())
            cpt += 1

        expected_nb_of_finishers_for_club1 = 7
        expected_nb_of_finishers_for_club2 = 5
        data = get_nb_finishers_by_club_order_by_desc_nb()
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0].get('club'), CLUB1)
        self.assertEqual(data[1].get('club'), CLUB2)
        self.assertEqual(data[0].get('nb'), expected_nb_of_finishers_for_club1)
        self.assertEqual(data[1].get('nb'), expected_nb_of_finishers_for_club2)



