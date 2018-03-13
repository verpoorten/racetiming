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
from timing.models.runner import Runner
from timing.models.payment import Payment
from django.shortcuts import get_object_or_404
from timing.views.common import get_common_data
from django.contrib.auth.decorators import login_required
from django.utils import timezone


@login_required
def payment_list(request):
    r = Runner.find_all()
    context = {"runners": r}
    context.update(get_common_data())
    return render(request, "payment/list.html",
                  context)


@login_required
def payed(request, runner_id):
    a_runner = get_object_or_404(Runner, id=runner_id)

    payment = Payment.find_by_runner(a_runner)
    if payment:
        payment.status = True
    else:
        payment = Payment(runner=a_runner, status=True,
                          payment_date=timezone.now())
    payment.save()

    r = Runner.find_all()
    context = {"runners": r}
    context.update(get_common_data())
    return render(request, "payment/list.html",
                  context)
