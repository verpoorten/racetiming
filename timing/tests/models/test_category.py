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
from timing.models.category import Category
from timing.tests.factories.category import CategoryFactory
from timing.models.enums import gender
import datetime
from django.utils import timezone


class CategoryTest(TestCase):

    def test_get_category_by_date(self):
        yr = timezone.now().year
        self.assertIsNone(Category.get_category_by_date(None, None))
        self.assertIsNone(Category.get_category_by_date(None, None))

        a_female = gender.FEMALE
        a_category = CategoryFactory(gender=a_female,
                                     start_date=datetime.date(yr, 1, 1),
                                     end_date=datetime.date(yr+1, 12, 31))
        self.assertEqual(Category.get_category_by_date(datetime.date(yr, 1, 10), a_female), a_category)

    def test_find_all(self):
        self.assertCountEqual(Category.find_all(), [])
        categories = []
        cpt = 1
        while cpt < 4:
            categories.append(CategoryFactory())
            cpt = cpt + 1

        self.assertCountEqual(Category.find_all(), categories)

    def test_find_by_id(self):
        self.assertIsNone(Category.find_by_id(-1))
        a_category = CategoryFactory()
        self.assertEqual(Category.find_by_id(a_category.id), a_category)
