# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe
from shopping_cart.shopping_cart.cart import get_address_docs

no_cache = 1
no_sitemap = 1

@frappe.whitelist()
def get_addresses():
	return [d.fields for d in get_address_docs()]
