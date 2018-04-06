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
from timing.models.race import Race
from timing.models.ranking import Ranking


def get_nb_finishers_by_club_order_by_desc_nb():
    clubs = Ranking.find_clubs()
    club_finishers = []
    for a_club in clubs:
        nb_finishers = len(Ranking.find_by_club(a_club.get('runner__club')))
        club_finishers.append({'club': a_club.get('runner__club'), 'nb': nb_finishers})
    return sorted(club_finishers, key=lambda t: t.get('nb'), reverse=True)


def get_podium_by_race_category(races):
    results = []

    for a_race in races:
        rankings = Ranking.find_by_race(a_race)
        categories = _get_race_finisher_categories(rankings)
        for a_category in categories:
            rankings = Ranking.find_by_category_race(a_category, a_race).order_by('checkin')
            finishers = _get_first_finishers_by_race_and_category(rankings)
            results.append({"race": a_race, "category": a_category, "finishers": list(finishers)})
    return results


def _get_first_finishers_by_race_and_category(rankings):
    finishers = []
    cpt = 0
    for a_ranking in rankings:
        if a_ranking.runner not in finishers:
            a_runner = a_ranking.runner
            a_runner.time_race=a_ranking.accurate_time
            finishers.append(a_runner)
            cpt = cpt + 1
            if cpt == 3:
                break
    return finishers


def _get_race_finisher_categories(rankings):
    categories = []
    if rankings:
        for ranking in rankings:
            if ranking.runner.category not in categories:
                categories.append(ranking.runner.category)
    return categories
