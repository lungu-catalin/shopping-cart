# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import unittest
import frappe
from shopping_cart.shopping_cart import get_quotation

class TestShoppingCart(unittest.TestCase):
	"""
		Note:
		Shopping Cart == Quotation
	"""
	def setUp(self):
		frappe.set_user("Administrator")
		self.enable_shopping_cart()
		
	def tearDown(self):
		frappe.set_user("Administrator")
		self.disable_shopping_cart()
	
	def test_get_cart_new_user(self):
		self.login_as_new_user()
		
		# test if lead is created and quotation with new lead is fetched
		
	def test_get_cart_lead(self):
		self.login_as_lead()
		
		# test if quotation with lead is fetched
		pass
		
	def test_get_cart_customer(self):
		self.login_as_customer()
		
		# test if quotation with customer is fetched
		quotation = get_quotation()
		self.assertEquals(quotation.doc.quotation_to, "Customer")
		self.assertEquals(quotation.doc.customer, "_Test Customer")
		
	def test_add_to_cart(self):
		# add first item
		pass
		
		# add second item
		pass
		
	def test_update_cart(self):
		# first, add to cart
		self.test_add_to_cart()
		
		# update first item
		pass
		
	def test_remove_from_cart(self):
		# first, add to cart
		self.test_add_to_cart()
		
		# remove first item
		pass
		
		# remove second item
		pass
		
		# NEED CLARIFICATION: should quotation exist after all items are removed?
		pass
		
	def test_add_address(self):
		pass
		
	def test_set_billing_address(self):
		pass
		
	def test_set_shipping_address(self):
		pass
		
	def test_shipping_rule(self):
		self.test_set_shipping_address()
		
		# check if shipping rule changed
		pass
		
	def test_price_list(self):
		self.test_set_billing_address()
		
		# check if price changed
		pass
		
	def test_place_order(self):
		pass

	# helper functions
	def enable_shopping_cart(self):
		settings = frappe.bean("Shopping Cart Settings", "Shopping Cart Settings")

		if len(settings.doclist) > 1:
			settings.doc.enabled = 1
		else:
			settings.doc.fields.update({
				"enabled": 1,
				"company": "_Test Company",
				"default_territory": "_Test Territory Rest Of The World",
				"default_customer_group": "_Test Customer Group",
				"quotation_series": "_T-Quotation-"
			})
			settings.doclist.extend([
				# price lists
				{"doctype": "Shopping Cart Price List", "parentfield": "price_lists", 
					"selling_price_list": "_Test Price List India"},
				{"doctype": "Shopping Cart Price List", "parentfield": "price_lists", 
					"selling_price_list": "_Test Price List Rest of the World"},
			
				# tax masters
				{"doctype": "Shopping Cart Taxes and Charges Master", "parentfield": "sales_taxes_and_charges_masters",
					"sales_taxes_and_charges_master": "_Test India Tax Master"},
				{"doctype": "Shopping Cart Taxes and Charges Master", "parentfield": "sales_taxes_and_charges_masters",
					"sales_taxes_and_charges_master": "_Test Sales Taxes and Charges Master - Rest of the World"},
			
				# shipping rules
				{"doctype": "Shopping Cart Shipping Rule", "parentfield": "shipping_rules",
					"shipping_rule": "_Test Shipping Rule - India"}
			])
		
		settings.save()
		
	def disable_shopping_cart(self):
		settings = frappe.bean("Shopping Cart Settings", "Shopping Cart Settings")
		settings.doc.enabled = 0
		settings.save()
		
	def login_as_new_user(self):
		pass
		
	def login_as_lead(self):
		pass
		
	def login_as_customer(self):
		frappe.set_user("test_contact_customer@example.com")

test_dependencies = ["Sales Taxes and Charges Master", "Price List", "Shipping Rule", "Currency Exchange",
	"Customer Group", "Lead", "Customer", "Contact", "Address"]		
		
test_records = [
	# profiles for cart
	[
		{
			"doctype": "Profile",
			"email": "test_cart_user@example.com",
			"user_type": "Website User",
			"first_name": "Cart User",
			"new_password": "password",
		}
	],
	[
		{
			"doctype": "Profile",
			"email": "test_lead@example.com",
			"user_type": "Cart Lead",
			"first_name": "Cart User",
			"new_password": "password",
		}
	],
	[
		{
			"doctype": "Profile",
			"email": "test_contact_customer@example.com",
			"user_type": "Website User",
			"first_name": "Cart Contact Of Customer",
			"new_password": "password",
		}
	],
]