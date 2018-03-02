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


class Race(models.Model):
    description = models.CharField(max_length=150, db_index=True)
    distance = models.DecimalField(max_digits=5, decimal_places=2)
    unit = models.CharField(max_length=30, choices=unit.UNIT_CHOICES, default='KM')
    race_date = models.DateField()
    race_start = models.TimeField(blank=True, null=True)
    current = models.BooleanField(default=False)

    def __str__(self):
        return "{}".format(self.description)

    def find_by_id(an_id):
        try:
            return Race.objects.get(pk=an_id)
        except:
            None

    def find_all():
        return Race.objects.all().order_by('race_date', 'race_start')


    def find_all_current():
        return Race.objects.filter(current=True).order_by('race_date', 'race_start')
