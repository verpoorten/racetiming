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
from timing.models.runner import Runner
from timing.models.race import Race
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from timing.document import xls_build
from django.utils.translation import ugettext_lazy as _


@login_required
def build_document(request, race_id):
    a_race = get_object_or_404(Race, id=race_id)
    workingsheets_data = prepare_xls_content(Runner.find_by_race(a_race))
    return xls_build.generate_xls(prepare_xls_parameters_list(request.user, workingsheets_data, a_race))


def prepare_xls_content(records):
    return [_extract_xls_data_from_runner(runner) for runner in records]


def prepare_xls_parameters_list(user, workingsheets_data, a_race):
    return {xls_build.LIST_DESCRIPTION_KEY: "Liste d'activités",
            xls_build.FILENAME_KEY: _('runners'),
            xls_build.USER_KEY: user,
            xls_build.WORKSHEETS_DATA:
                [{xls_build.CONTENT_KEY: workingsheets_data,
                  xls_build.HEADER_TITLES_KEY: [str(_('lastname')),
                                                str(_('firstname')),
                                                "{} - {} {} {}".format(str(_('number_small')), str(a_race.description), str(a_race.distance), str(a_race.unit)),
                                                str(_('category')),
                                                str(_('status'))

                                                ],
                  xls_build.WORKSHEET_TITLE_KEY: "{} {} {}".format(_('runners'), a_race.distance, a_race.unit)
                  }
                 ]}


def _extract_xls_data_from_runner(a_runner):
    return [a_runner.last_name, a_runner.first_name, a_runner.number, a_runner.category, get_attention(a_runner.payment_status)]


def get_attention(status):
    if not status:
        return _('unpayed')
    return ''
