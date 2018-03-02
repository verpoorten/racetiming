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
from timing.models.category import Category
from timing.forms.category import CategoryForm, CategoryUpdateForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import get_object_or_404

def category_list(request):
    r = Category.find_all()
    print(r)
    return render(request, "category/list.html",
                  {"categories": r})

def new(request):
    print('runner_new')
    return render(request, "category/creation.html",
                  {'form': CategoryForm()})
def create(request):
    return add(request, None)


def add(request, an_id):
    print(an_id)
    print('runner_add')
    if an_id:
        instance = get_object_or_404(Category, id=an_id)
        page_html= "category/modification.html"
    else:
        instance = None
        page_html= "category/creation.html"


    form =CategoryForm(request.POST or None, instance=instance)
    if form.is_valid():
        print('valid')
        new_runner = form.save()
        return HttpResponseRedirect(reverse('category_list', ))
    else:
        print('invlid')
        return render(request, page_html,
                      {'form': form})


def update(request, runner_id):
    print('runner_update {}'.format(runner_id))
    a_runner = Category.find_by_id(runner_id)
    return render(request, "category/modification.html",
                  {'form': CategoryUpdateForm(instance=a_runner),
                   'category': a_runner})

def delete(request, an_id):
    instance = get_object_or_404(Category, id=an_id)
    if instance:
        instance.delete()
    return HttpResponseRedirect(reverse('category_list', ))
