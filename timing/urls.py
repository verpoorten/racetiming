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
from django.conf.urls import url
from timing.views import ranking, runner, race, category, common
from django.conf.urls import url, include
from django.contrib import admin


urlpatterns = [
    url(r'^$', common.index, name='home'),

    url(r'^category/', include([
        url(r'^list/$', category.category_list, name='category_list'),
        url(r'^new/$', category.new, name='new_category'),
        url(r'^add/([0-9]+)/$', category.add, name='add_category'),
        url(r'^race/create/$', category.create, name='create_category'),
        url(r'^update/([0-9]+)/$', category.update, name='update_category'),
        url(r'^delete/([0-9]+)/$', category.delete, name='delete_category'),
    ])),
    url(r'^runner/', include([
        url(r'^list/$', runner.runner_list, name='runner_list'),
        url(r'^new/$', runner.runner_new, name='new_runner'),
        url(r'^add/([0-9]+)/$', runner.runner_add, name='add_runner'),
        url(r'^create/$', runner.runner_create, name='create_runner'),
        url(r'^update/([0-9]+)/$', runner.runner_update, name='update_runner'),
    ])),

    url(r'^race/', include([
        url(r'^list/$', race.race_list, name='race_list'),
        url(r'^new/$', race.race_new, name='new_race'),
        url(r'^add/([0-9]+)/$', race.race_add, name='add_race'),
        url(r'^create/$', race.race_create, name='create_race'),
        url(r'^update/([0-9]+)/$', race.race_update, name='update_race'),
    ])),
    url(r'^ranking/', include([
        url(r'^$', ranking.ranking, name='ranking'),
        url(r'^add/$', ranking.add_ranking, name='add_ranking'),
        url(r'^podium/$', ranking.podium, name='podium'),
        url(r'^delete/([0-9]+)/$', ranking.delete_ranking, name='delete_ranking'),
        url(r'^general/$', ranking.general_ranking, name='general_ranking'),
        url(r'^delete/general/([0-9]+)/$', ranking.delete_on_general, name='delete_ranking_general'),
    ])),
]
