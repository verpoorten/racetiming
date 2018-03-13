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

import datetime

from django.db import models


class Ranking(models.Model):
    runner = models.ForeignKey('Runner', on_delete=models.DO_NOTHING, blank=True, null=True)
    checkin = models.DateTimeField(blank=True, null=True)
    attention = models.BooleanField(default=False)
    accurate_time = models.DurationField(blank=True, null=True)

    @property
    def race_time(self):
        if self.runner:
            total_min = diff_in_minutes(self.runner.race.race_start, self.checkin.time())

            min = total_min % 60
            hrs = (total_min - min) / 60
            return "{}:{}".format(int(hrs), format(int(min), '02d'))

        else:
            return ''

    @property
    def general_ranking(self):
        return get_ranking(Ranking.find_by_race(self.runner.race).order_by('accurate_time'), self.runner)

    @property
    def category_ranking(self):
        if self.runner:
            return get_ranking(Ranking.find_by_category_race(self.runner.category, self.runner.race), self.runner)
        return None

    @property
    def duplicated(self):
        if self.runner:
            rankings = Ranking.find_by_runner(self.runner)
            if rankings and len(rankings) > 1:
                return True
        return False

    def __str__(self):
        return "{}, {}".format(self.runner, self.checkin)

    def find_all():
        return Ranking.objects.all()

    def find_by_category(a_category):
        return Ranking.objects.filter(runner__category=a_category).order_by('checkin')

    def find_by_runner(a_runner):
        return Ranking.objects.filter(runner=a_runner)

    def find_by_race(a_race):
        return Ranking.objects.filter(runner__race=a_race)

    def find_by_category_race(cat, a_race):
        results = Ranking.objects.filter(runner__category=cat, runner__race=a_race).order_by('accurate_time')
        return results

    def save(self, *args, **kwargs):
        an_existing_ranking = Ranking.find_by_runner(self.runner)
        if an_existing_ranking:
            self.attention = True
        if self.checkin and self.runner.race.accurate_race_start:
            self.accurate_time = self.checkin - self.runner.race.accurate_race_start

        super(Ranking, self).save(*args, **kwargs)


    def find_all_order(field_order):
        return Ranking.objects.all().order_by(field_order)

def diff_in_minutes(start, end):
    startdelta = datetime.timedelta(hours=start.hour, minutes=start.minute, seconds=start.second)
    enddelta = datetime.timedelta(hours=end.hour, minutes=end.minute, seconds=end.second)
    return (enddelta - startdelta).seconds / 60


def get_ranking(result_for_category, the_runner):
    if the_runner:
        cpt = 1
        for r in result_for_category:
            if r.runner == the_runner:
                return cpt
            cpt = cpt + 1
    else:
        return None
