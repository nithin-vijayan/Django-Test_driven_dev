# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from lists.views import home_page
from django.http import HttpRequest
from lists.models import Item, List

# Create your tests here.
class HomePageTest(TestCase):

	def test_home_page_returns_correct_html(self):
		response = self.client.get('/')
		self.assertTemplateUsed(response, 'home.html')

class ItemAndListModelTest(TestCase):

	def test_saving_and_retrieving_items(self):
		first_item = Item()
		list_ = List.objects.create()
		first_item.text = 'The first (ever) list item'
		first_item.list = list_
		first_item.save()

		second_item = Item()
		second_item.text = 'Item the second'
		second_item.list = list_
		second_item.save()

		
		saved_list = List.objects.first()
		self.assertEqual(saved_list, list_)

		saved_items = Item.objects.all()
		self.assertEqual(saved_items.count(), 2)
		
		first_saved_item = saved_items[0]
		second_saved_item = saved_items[1]

		self.assertEqual(first_saved_item.text, 'The first (ever) list item')
		self.assertEqual(first_saved_item.list, list_)
		self.assertEqual(second_saved_item.text, 'Item the second')
		self.assertEqual(second_saved_item.list, list_)

class NewListViewTest(TestCase):

	def test_can_save_a_POST_request(self):
		response = self.client.post('/lists/new', data={'item_text': 'A new list item'})
		self.assertEqual(Item.objects.count(), 1)
		new_item = Item.objects.first()
		self.assertEqual(new_item.text, 'A new list item')

	def test_can_redirect_after_post(self):
		response = self.client.post('/lists/new', data={'item_text': 'A new list item'})
		list_ = List.objects.first()
		self.assertRedirects(response, '/lists/{}/'.format(list_.id))

class ListViewTest(TestCase):

	def test_uses_list_template(self):
		list_ = List.objects.create()
		response = self.client.get('/lists/{}/'.format(list_.id))
		self.assertTemplateUsed(response, 'list.html')

	def test_passes_correct_context_to_list(self):
		other_list = List.objects.create()
		list_ = List.objects.create()
		response = self.client.get('/lists/{}/'.format(list_.id))
		self.assertEqual(response.context['list'], list_)

	def test_displaytest_displays_only_items_for_that_list_all_items(self):
		correct_list = List.objects.create()
		Item.objects.create(text='itemey 1', list=correct_list)
		Item.objects.create(text='itemey 2', list=correct_list)
		
		other_list = List.objects.create()
		Item.objects.create(text='other item 1', list=other_list)
		Item.objects.create(text='other item 2', list=other_list)

		response = self.client.get('/lists/{}/'.format(correct_list.id))

		self.assertContains(response, 'itemey 1')
		self.assertContains(response, 'itemey 1')	
		self.assertNotContains(response, 'other item 1')
		self.assertNotContains(response, 'other item 2')
		
class NewItemTest(TestCase):

	def test_can_save_POST_to_an_existing_list(self):
		other_list = List.objects.create()
		correct_list = List.objects.create()
		
		self.client.post(
			'/lists/{}/add_item'.format(correct_list.id),
			data={'item_text': 'A new item for an existing list'}
		)

		self.assertEqual(Item.objects.count(), 1)
		new_item = Item.objects.first()
		self.assertEqual(new_item.text, 'A new item for an existing list')
		self.assertEqual(new_item.list, correct_list)

	def test_redirects_to_list_view(self):
		other_list = List.objects.create()
		correct_list = List.objects.create()

		response = self.client.post(
			'/lists/{}/add_item'.format(correct_list.id),
			data={'item_text': 'A new item for an existing list'}
		)

		self.assertRedirects(response, '/lists/{}/'.format(correct_list.id))