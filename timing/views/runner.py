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
from timing.forms.runner import RunnerForm, RunnerUpdateForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import get_object_or_404
from timing.views.common import get_common_data
from django.contrib.auth.decorators import login_required


@login_required
def runner_list(request):
    r = Runner.find_all()
    context = {"runners": r}
    context.update(get_common_data())
    return render(request, "runner/list.html",
                  context)


@login_required
def runner_new(request):
    context = {'form': RunnerForm()}
    context.update(get_common_data())
    return render(request, "runner/creation.html",
                  context)


@login_required
def runner_create(request):
    return runner_add(request, None)


@login_required
def runner_add(request, runner_id):
    if runner_id:
        instance = get_object_or_404(Runner, id=runner_id)
        form = RunnerUpdateForm(request.POST or None, instance=instance)
        page_html = "runner/modification.html"
    else:
        instance = None
        form = RunnerForm(request.POST or None, instance=instance)

        page_html = "runner/creation.html"

    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('runner_list', ))
    else:
        context = {'form': form, 'runner': instance}
        context.update(get_common_data())
        return render(request, page_html,
                      context)


@login_required
def runner_update(request, runner_id):
    a_runner = Runner.find_by_id(runner_id)
    context = {'form': RunnerUpdateForm(instance=a_runner), 'runner': a_runner}
    context.update(get_common_data())
    return render(request, "runner/modification.html",
                  context)
