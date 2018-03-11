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
from timing.forms.runner import RunnerInlineForm
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext as _
from django.conf import settings
from website.views import jogging


def add_registration(request):
    print('add_registration')
    form = RunnerInlineForm(request.POST or None)
    print(request.POST)
    msg = None
    if form.is_valid():
        print('valid')
        race_id = request.POST.get('race', None)
        price = None
        bank_account = None
        if race_id:
            print('raciqsdqfqdf')
            race = get_object_or_404(Race, id=race_id)
            if race:
                if race.bank_account:
                    bank_account = race.bank_account
                if race.price:
                    price = race.price
                if bank_account and price:
                    print(bank_account)
                    print(price)
                    msg = "{}.".format((_('registration_confirmation')
                                                             % (race.presale_price,
                                                                race.bank_account)))
        form.save()
    else:
        print('invalid')
        msg = _('')
        msg = "{}.".format((_('error_registration')
                            % (settings.EMAIL)))
    print(msg)
    context = jogging.get_common_data()
    context.update({'confirmation_message': msg})
    return render(request, "public/registration_confirmation.html",
                  context)


