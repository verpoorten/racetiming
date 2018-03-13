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
from __future__ import unicode_literals

from django.db import models
from timing.models.enums import unit
from django.utils.translation import ugettext as _
from timing.models.runner import Runner
from timing.models.ranking import Ranking


class Race(models.Model):
    description = models.CharField(max_length=150, db_index=True, verbose_name=_('description'))
    distance = models.DecimalField(max_digits=5, decimal_places=2, verbose_name=_('distance'))
    unit = models.CharField(max_length=30, choices=unit.UNIT_CHOICES, default='KM', verbose_name=_('unit'))
    race_start = models.DateTimeField(blank=True, null=True, verbose_name=_('race_start'))
    accurate_race_start = models.DateTimeField(blank=True, null=True, verbose_name=_('time'))
    current = models.BooleanField(default=False, verbose_name=_('current'))
    price = models.DecimalField(max_digits=5, decimal_places=2, verbose_name=_('price'))
    pre_registration = models.BooleanField(default=False, verbose_name=_('pre-registration'))
    presale_price = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True,
                                        verbose_name=_('presale_price'))
    bank_account = models.CharField(max_length=30, verbose_name=_('bank_account'))
    ended = models.BooleanField(default=False, verbose_name=_('ended'))

    def __str__(self):
        return "{}".format(self.description)

    @property
    def runners_expected(self):
        return len(Runner.find_by_race(self))

    @property
    def runners_arrived(self):
        available_ranking = []
        rankings = Ranking.find_by_race(self)
        for r in rankings:
            if r.runner not in available_ranking:
                available_ranking.append(r.runner)

        return len(available_ranking)

    def find_by_id(an_id):
        try:
            return Race.objects.get(pk=an_id)
        except:
            None

    def find_all():
        return Race.objects.all().order_by('race_start')

    def find_all_current():
        return Race.objects.filter(current=True).order_by('race_start')

    def find_all_current_pre_registration():
        return Race.objects.filter(current=True, pre_registration=True, ended=False).order_by('race_start')

    def find_started_race():
        races = Race.objects.filter(current=True).order_by('race_start')
        races_started = []
        for r in races:
            if r.accurate_race_start:
                races_started.append(r)
        return races_started

    def find_ended_race():
        return Race.objects.filter(current=True, ended=True).order_by('race_start')
