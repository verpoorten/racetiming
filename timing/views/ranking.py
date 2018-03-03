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


def ranking(request):
    return render(request, "ranking/ranking.html",
                  {'form': RankingForm(),
                   'rankings': Ranking.find_all().order_by('-checkin')})


def add_ranking(request):
    form = RankingForm(request.POST or None)
    if form.is_valid():
        print('is valid')
        a_runner = Runner.find_by_number(request.POST.get('number', None))
        an_existing_ranking = Ranking.find_by_runner(a_runner)
        a_new_ranking = Ranking(runner=a_runner, checkin=datetime.datetime.now())
        if an_existing_ranking:
            a_new_ranking.attention = True
        a_new_ranking.save()
    return render(request, "ranking/ranking.html",
                  {'form': form,
                   'rankings': Ranking.find_all().order_by('checkin')})


def podium(request):
    resultats = []
    races = Race.find_all()
    for r in races:
        print(r)
        rankings = Ranking.find_by_race(r)

        cats = []
        for ranking in rankings:
            if ranking.runner.category not in cats:
                cats.append(ranking.runner.category)

        for c in cats:
            rankings = Ranking.find_by_category_race(c, r).order_by('checkin')
            runners = []
            cpt = 0
            for rank in rankings:
                if rank.runner not in runners:
                    runners.append(rank.runner)
                    cpt = cpt + 1
                    if cpt == 3:
                        break

            resultats.append({"race": r, "category": c, "runners": list(runners)})

    return render(request, "ranking/podium.html",
                  {'results': resultats})


def delete_ranking(request, ranking_id):
    delete(ranking_id)
    return HttpResponseRedirect(reverse('ranking', ))


def delete(ranking_id):
    ranking_to_delete = get_object_or_404(Ranking,
                                          id=ranking_id)
    if ranking_to_delete:
        ranking_to_delete.delete()


def general_ranking(request):
    return render(request, "ranking/general.html",
                  {'rankings': Ranking.find_all().order_by('checkin')})


def delete_on_general(request, ranking_id):
    delete(ranking_id)
    return HttpResponseRedirect(reverse('general_ranking', ))
