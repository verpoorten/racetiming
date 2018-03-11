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
from timing.models.runner import Runner
from timing.forms.utils.datefield import DatePickerInput, DATE_FORMAT
from timing.models.enums import gender
from django.utils.translation import ugettext as _


class RunnerForm(forms.ModelForm):
    birth_date = forms.DateField(widget=DatePickerInput(format=DATE_FORMAT),
                                 input_formats=[DATE_FORMAT, ],
                                 required=False)

    class Meta:
        model = Runner
        fields = ['first_name', 'last_name', 'gender', 'birth_date', 'number', 'race']

    def __init__(self, *args, **kwargs):
        super(forms.ModelForm, self).__init__(*args, **kwargs)
        self.fields['number'].required = True



class RunnerUpdateForm(forms.ModelForm):
    birth_date = forms.DateField(widget=DatePickerInput(format=DATE_FORMAT),
                                 input_formats=[DATE_FORMAT, ],
                                 required=False)

    class Meta:
        model = Runner
        fields = ['first_name', 'middle_name', 'last_name', 'gender', 'birth_date', 'number', 'category', 'race']

    def __init__(self, *args, **kwargs):
        super(RunnerUpdateForm, self).__init__(*args, **kwargs)
        self.fields['category'].widget.attrs['disabled'] = 'disabled'


class RunnerInlineForm(forms.ModelForm):
    birth_date = forms.DateField(widget=DatePickerInput(format=DATE_FORMAT),
                                 input_formats=[DATE_FORMAT, ],
                                 required=True)
    gender = forms.ChoiceField(choices=gender.GENDER_CHOICES, required=True)

    race = forms.ModelChoiceField(queryset=Race.find_all_current_pre_registration(),
                                  widget=forms.Select(), required=True, empty_label=None)

    class Meta:
        model = Runner
        fields = ['first_name', 'last_name', 'gender', 'birth_date', 'race',  'medical_consent']

    def __init__(self, *args, **kwargs):
        super(forms.ModelForm, self).__init__(*args, **kwargs)
        self.fields['birth_date'].label = _('birth_date')
        self.fields['gender'].label = _('gender')
        self.fields['race'].label = _('race')
        self.fields['medical_consent'].widget.attrs['required'] = 'required'
        self.fields['medical_consent'].error_messages = {'required': _('medical_agreement')}
        self.fields['medical_consent'].widget.attrs.update({'class' : 'marginr-10'})