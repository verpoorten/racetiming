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
from timing.models.enums import gender


class Category(models.Model):
    label = models.CharField(max_length=50, db_index=True)
    start_date = models.DateField()
    end_date = models.DateField()
    gender = models.CharField(max_length=1, blank=True, null=True, choices=gender.GENDER_CHOICES, default=None)

    def __str__(self):
        return self.label


    @property
    def get_period(self):
        return "{} - {}".format(self.start_date, self.end_date)


    @staticmethod
    def find_category_by_date(birth_date, a_gender):
        try:
            return Category.objects.filter(start_date__lte=birth_date,
                                           end_date__gte=birth_date,
                                           gender=a_gender).first()
        except:
            None

    def find_by_id(an_id):
        try:
            return Category.objects.get(pk=an_id)
        except:
            None

    def find_all():
        return Category.objects.all().order_by('start_date', 'gender')
