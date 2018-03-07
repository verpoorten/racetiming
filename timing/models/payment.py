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


class Payment(models.Model):
    runner = models.OneToOneField('Runner', on_delete=models.DO_NOTHING)
    payment_date = models.DateTimeField(blank=True, null=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return "{} {}".format(self.runner, self.status)

    def find_by_runner(a_runner):
        try:
            return Payment.objects.get(runner=a_runner)
        except:
            None

