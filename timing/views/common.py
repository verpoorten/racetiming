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
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login as django_login
from django.utils import translation
from django.shortcuts import redirect


@login_required
def index(request):
    return render(request, "home.html",
                  get_common_data())


def get_common_data():
    return {"current_races": Race.find_all_current()}


def login(request):
    return django_login(request)


def profile_lang_edit(request, ui_language):
    print('profile_lang_edit')
    translation.activate(ui_language)
    print(translation.LANGUAGE_SESSION_KEY)
    request.session[translation.LANGUAGE_SESSION_KEY] = ui_language
    print(ui_language)
    return redirect(request.META['HTTP_REFERER'])