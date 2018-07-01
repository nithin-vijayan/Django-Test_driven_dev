# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.urls import resolve
from lists.views import home_page

# Create your tests here.
class SmokeTest(TestCase):

	def test_roo_url_resolve_to_homepage(self):
		found = resolve('/')
		self.assertEqual(found.func, home_page)