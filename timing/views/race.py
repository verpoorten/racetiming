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
from timing.models.race import Race
from timing.forms.race import RaceForm, RaceUpdateForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import get_object_or_404
from timing.views.common import get_common_data
from django.contrib.auth.decorators import login_required


@login_required
def race_list(request):
    r = Race.find_all()
    context = {"races": r}
    context.update(get_common_data())
    return render(request, "race/list.html",
                  context)


@login_required
def race_new(request):
    context = {'form': RaceForm()}
    context.update(get_common_data())
    return render(request, "race/creation.html",
                  context)


@login_required
def race_create(request):
    print('race_create')
    return race_add(request, None)


@login_required
def race_add(request, race_id):
    print('race_add')
    if race_id:
        instance = get_object_or_404(Race, id=race_id)
        page_html = "race/modification.html"
    else:
        instance = None
        page_html = "race/creation.html"

    form = RaceForm(request.POST or None, instance=instance)

    if form.is_valid():
        print('form valid')
        form.save()
        return HttpResponseRedirect(reverse('race_list', ))
    else:
        print('form invalid')
        context = {'form': form}
        context.update(get_common_data())
        return render(request, page_html,
                      context)


@login_required
def race_update(request, race_id):
    a_race = Race.find_by_id(race_id)
    form = RaceUpdateForm(instance=a_race)
    context = {'form': form, 'race': a_race}
    context.update(get_common_data())
    context.update({'race': a_race})
    return render(request, "race/modification.html",
                  context)


@login_required
def start_race(request, race_id):
    a_race = Race.find_by_id(race_id)
    a_race.accurate_race_start = datetime.datetime.now()
    a_race.save()
    context = get_common_data()
    return HttpResponseRedirect(reverse('home', ))


@login_required
def end_race(request, race_id):
    a_race = Race.find_by_id(race_id)
    a_race.ended = True
    a_race.save()
    context = get_common_data()
    return HttpResponseRedirect(reverse('home', ))

