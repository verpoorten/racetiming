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
from django.utils.translation import ugettext as _
from timing.models.category import Category
from timing.models.payment import Payment
from timing.models.enums import gender
from django.db.models.functions import Lower
from django.contrib import admin


class RunnerAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'category', 'race')


class Runner(models.Model):
    GENDER_CHOICES = (
        ('F', _('female')),
        ('M', _('male')))

    last_name = models.CharField(max_length=50, db_index=True, verbose_name=_('lastname'))
    first_name = models.CharField(max_length=50, db_index=True, verbose_name=_('firstname'))
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    gender = models.CharField(max_length=1, blank=True, null=True, choices=gender.GENDER_CHOICES, default=None,
                              verbose_name=_('gender'))
    birth_date = models.DateField(blank=True, null=True, verbose_name=_('birth_date'))
    number = models.IntegerField(unique=True, verbose_name=_('number'), blank=True, null=True)
    category = models.ForeignKey('Category', blank=True, null=True, on_delete=models.DO_NOTHING,
                                 verbose_name=_('category'))
    race = models.ForeignKey('Race', blank=True, null=True, on_delete=models.DO_NOTHING, verbose_name=_('race'))
    medical_consent = models.BooleanField(default=False, verbose_name=_('medical_consent'))

    def __str__(self):
        return "{}, {}".format(self.last_name, self.first_name)

    def save(self, *args, **kwargs):
        if self.birth_date and self.gender:
            self.category = Category.get_category_by_date(self.birth_date, self.gender)
        super(Runner, self).save(*args, **kwargs)

    @staticmethod
    def find_all():
        return Runner.objects.all().order_by(Lower('last_name'), Lower('first_name'))

    def find_by_id(an_id):
        try:
            return Runner.objects.get(pk=an_id)
        except Runner.DoesNotExist:
            None

    def find_by_number(a_number):
        try:
            return Runner.objects.get(number=a_number)
        except Runner.DoesNotExist:
            None

    def find_by_number_started_race(a_number):
        try:
            res = Runner.objects.get(number=a_number)
            if res.race.accurate_race_start:
                return res
            return None
        except Runner.DoesNotExist:
            None

    def find_by_race(a_race):
        return Runner.objects.filter(race=a_race).order_by('last_name', 'first_name')

    @property
    def payment_status(self):
        pay = Payment.find_by_runner(self)
        if pay:
            return pay.status
        return False
