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
from django.shortcuts import render
from timing.models.race import Race
from timing.models.runner import Runner
from timing.models.payment import Payment
from timing.forms.runner import RunnerInlineForm


def index(request):
    context = get_common_data()
    # context.update({'registration_number': Payment.get_number_by_status(True) })
    context.update({'registration_number': len(Runner.find_all())})
    return render(request, "public/home.html",
                  context)

def information(request):
    return render(request, "public/information.html",
                  get_common_data())

def rules(request):
    return render(request, "public/rules.html",
                  get_common_data())

def contact(request):
    return render(request, "public/contact.html",
                  get_common_data())

def pre_registration(request):
    context = get_common_data()
    context.update({'runners': Runner.find_all(), 'last_update' : Payment.last_update()})

    return render(request, "public/pre-registration.html",
                  context)

def registration(request):
    context = {'form': RunnerInlineForm()}
    context.update(get_common_data())
    return render(request, "public/registration.html",
                  context)


def get_common_data():
    return {"races_preregistration": Race.find_all_current_pre_registration(),
            'races_ended': Race.find_ended_race()}