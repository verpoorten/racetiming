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
from django.test import TestCase
from timing.models.race import Race
from timing.forms.race import RaceUpdateForm
from timing.models.enums.unit import KM


class RaceFormTest(TestCase):
    def test_race_form_invalid(self):
        missing_data = {'description': 'une description', }
        form = RaceUpdateForm(
            data=missing_data)
        self.assertFalse(form.is_valid())

    def test_race_form_valid(self):
        mandatory_fields = {'description': 'une description',
                            'distance': 10,
                            'unit': KM,
                            'price': 6,
                            'bank_account': 'BE 36999'}
        form = RaceUpdateForm(
            data=mandatory_fields)

        self.assertTrue(form.is_valid())
        r = form.save()
        races = Race.find_all()

        self.assertCountEqual(races, [r])
        self.assertFalse(r.current)
        self.assertFalse(r.ended)
        self.assertFalse(r.pre_registration)
        self.assertEqual(r.description, mandatory_fields.get('description'))
        self.assertEqual(r.distance, mandatory_fields.get('distance'))
        self.assertEqual(r.unit, mandatory_fields.get('unit'))
        self.assertEqual(r.price, mandatory_fields.get('price'))
        self.assertEqual(r.bank_account, mandatory_fields.get('bank_account'))
        self.assertIsNone(r.presale_price)
