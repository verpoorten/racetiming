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
from django.shortcuts import render
from timing.models.runner import Runner
from timing.models.ranking import Ranking
from timing.models.race import Race
from timing.forms.ranking import RankingForm
from django.shortcuts import get_object_or_404
from timing.views.common import get_common_data
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext as _
from django.utils import timezone
from timing.business.ranking import get_nb_finishers_by_club_order_by_desc_nb, get_podium_by_race_category


@login_required
def ranking(request):
    context = {'form': RankingForm(),
               'rankings': Ranking.find_all_order('-accurate_time')}
    context.update(get_common_data())
    context.update({'started_races': Race.find_started_race()})
    return render(request, "ranking/ranking.html",
                  context)


@login_required
def add_ranking(request):
    form = RankingForm(request.POST or None)
    context = {'form': form, 'rankings': Ranking.find_all().order_by('-checkin')}
    if form.is_valid():
        a_runner = Runner.find_by_number_started_race(request.POST.get('number', None))
        if a_runner:
            a_new_ranking = Ranking(runner=a_runner,
                                    checkin=timezone.now())
            # an_existing_ranking = Ranking.find_by_runner(a_runner)
            # if an_existing_ranking:
            #     a_new_ranking.attention = True
            #
            # a_new_ranking.accurate_time = a_new_ranking.checkin - a_runner.race.accurate_race_start
            a_new_ranking.save()
        else:
            message =_('runner_not_started_race')
            context.update({'message': message})
    context.update(get_common_data())
    context.update({'started_races': Race.find_started_race()})
    return render(request, "ranking/ranking.html",
                  context)


@login_required
def podium(request):
    context = {'results': get_podium_by_race_category(Race.find_all())}
    context.update(get_common_data())
    return render(request, "ranking/podium.html",
                  context)


@login_required
def delete_ranking(request, ranking_id):
    delete(ranking_id)
    return HttpResponseRedirect(reverse('ranking', ))


def delete(ranking_id):
    ranking_to_delete = get_object_or_404(Ranking,
                                          id=ranking_id)
    if ranking_to_delete:
        ranking_to_delete.delete()


@login_required
def general_ranking(request, race_id):
    a_race = get_object_or_404(Race, id=race_id)

    if a_race:
        expected_runners = Runner.find_by_race(a_race)
        rankings = Ranking.find_by_race(a_race).order_by('checkin')
        runner_without_result = get_runner_without_result(rankings, expected_runners)
        context = {'rankings': rankings,
                   'race': a_race,
                   'runner_without_result': runner_without_result}
        context.update(get_common_data())
        return render(request, "ranking/general.html",
                      context)


@login_required
def delete_on_general(request, ranking_id):
    delete(ranking_id)
    return HttpResponseRedirect(reverse('general_ranking', ))


def get_runner_without_result(rankings, expected_runners):
    runner_without_results = []
    for runner in expected_runners:
        has_ranking = False
        for r in rankings:
            if r.runner == runner:
                has_ranking = True
                break
        if not has_ranking:
            runner_without_results.append(runner)

    return runner_without_results


def check_time_difference(t1, t2):
    t1_date = datetime(
        t1.year,
        t1.month,
        t1.day,
        t1.hour,
        t1.minute,
        t1.second)

    t2_date = datetime(
        t2.year,
        t2.month,
        t2.day,
        t2.hour,
        t2.minute,
        t2.second)

    t_elapsed = t1_date - t2_date

    return t_elapsed


@login_required
def by_club(request):
    context = {'clubs': get_nb_finishers_by_club_order_by_desc_nb()}
    context.update(get_common_data())

    return render(request, "ranking/by_club.html",
                  context)

