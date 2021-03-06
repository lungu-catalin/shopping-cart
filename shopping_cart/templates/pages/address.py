# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import json

import frappe
from shopping_cart.shopping_cart.cart import get_lead_or_customer, update_cart_address

no_cache = 1
no_sitemap = 1

def get_context(context):
	def _get_fields(fieldnames):
		return [frappe._dict(zip(["label", "fieldname", "fieldtype", "options"], 
				[df.label, df.fieldname, df.fieldtype, df.options]))
			for df in frappe.get_doctype("Address", processed=True).get({"fieldname": ["in", fieldnames]})]
	
	docname = doc = None
	title = "New Address"
	if frappe.form_dict.name:
		bean = frappe.bean("Address", frappe.form_dict.name)
		docname = bean.doc.name
		doc = bean.doc.fields
		title = bean.doc.name
	
	return {
		"doc": doc,
		"meta": frappe._dict({
			"left_fields": _get_fields(["address_title", "address_type", "address_line1", "address_line2",
				"city", "state", "pincode", "country"]),
			"right_fields": _get_fields(["email_id", "phone", "fax", "is_primary_address",
				"is_shipping_address"])
		}),
		"docname": docname,
		"title": title
	}
	
@frappe.whitelist()
def save_address(fields, address_fieldname=None):
	party = get_lead_or_customer()
	fields = json.loads(fields)
	
	if fields.get("name"):
		bean = frappe.bean("Address", fields.get("name"))
	else:
		bean = frappe.bean({"doctype": "Address", "__islocal": 1})
	
	bean.doc.fields.update(fields)
	
	party_fieldname = party.doctype.lower()
	bean.doc.fields.update({
		party_fieldname: party.name,
		(party_fieldname + "_name"): party.fields[party_fieldname + "_name"]
	})
	bean.ignore_permissions = True
	bean.save()
	
	if address_fieldname:
		update_cart_address(address_fieldname, bean.doc.name)
	
	return bean.doc.name
