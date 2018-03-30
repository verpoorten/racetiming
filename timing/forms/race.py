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
from django import forms
from timing.models.race import Race
from timing.forms.utils.datefield import DateTimePickerInput


class RaceForm(forms.ModelForm):

    race_start = forms.SplitDateTimeField(widget=DateTimePickerInput(),
                                          required=False)

    class Meta:
        model = Race
        fields = ['description', 'distance', 'unit', 'race_start', 'price', 'bank_account', 'presale_price', 'current',
                  'pre_registration']


class RaceUpdateForm(forms.ModelForm):

    race_start = forms.SplitDateTimeField(widget=DateTimePickerInput(),
                                          required=False)

    class Meta:
        model = Race
        fields = ['description',  'distance', 'unit', 'race_start', 'price', 'bank_account', 'presale_price',
                  'current', 'pre_registration']

    def __init__(self, *args, **kwargs):
        super(RaceUpdateForm, self).__init__(*args, **kwargs)
