from __future__ import unicode_literals
import frappe
import json
import frappe.utils
from frappe.utils import cstr, flt, getdate, cint, nowdate, add_days, get_link_to_form
from frappe import _
from six import string_types
from frappe.model.utils import get_fetch_values
from frappe.model.mapper import get_mapped_doc
from erpnext.stock.stock_balance import update_bin_qty, get_reserved_qty
from frappe.desk.notifications import clear_doctype_notifications
from frappe.contacts.doctype.address.address import get_company_address
from erpnext.controllers.selling_controller import SellingController
# from frappe.automation.doctype.auto_repeat.auto_repeat import get_next_schedule_date
from erpnext.selling.doctype.customer.customer import check_credit_limit
from erpnext.selling.doctype.sales_order.sales_order import SalesOrder
from erpnext.stock.doctype.item.item import get_item_defaults
from erpnext.setup.doctype.item_group.item_group import get_item_group_defaults
from erpnext.manufacturing.doctype.production_plan.production_plan import get_items_for_material_requests
from erpnext.accounts.party import get_party_account
from erpnext.accounts.doctype.sales_invoice.sales_invoice import validate_inter_company_party, update_linked_doc,\
	unlink_inter_company_doc


@frappe.whitelist()
def make_purchase_order2(source_name, target_doc=None, skip_item_mapping=False):
	
	def set_missing_values(source, target):
		# target.supplier = supplier
		target.apply_discount_on = ""
		target.additional_discount_percentage = 0.0
		target.discount_amount = 0.0
		target.inter_company_order_reference = ""
		target.jenis_transaksi = source.jenis_transaksi
		target.tax_status = source.tax_status

		# default_price_list = frappe.get_value("Supplier", supplier, "default_price_list")
		# if default_price_list:
		# 	target.buying_price_list = default_price_list

		if any( item.delivered_by_supplier==1 for item in source.items):
			if source.shipping_address_name:
				target.shipping_address = source.shipping_address_name
				target.shipping_address_display = source.shipping_address
			else:
				target.shipping_address = source.customer_address
				target.shipping_address_display = source.address_display

			target.customer_contact_person = source.contact_person
			target.customer_contact_display = source.contact_display
			target.customer_contact_mobile = source.contact_mobile
			target.customer_contact_email = source.contact_email

		else:
			target.customer = ""
			target.customer_name = ""

		target.run_method("set_missing_values")
		target.run_method("calculate_taxes_and_totals")

	def update_item(source, target, source_parent):
		target.schedule_date = source.delivery_date
		target.qty = flt(source.qty) - flt(source.ordered_qty)
		target.stock_qty = (flt(source.qty) - flt(source.ordered_qty)) * flt(source.conversion_factor)
		target.project = source_parent.project

	target_doc = get_mapped_doc("Sales Order", source_name, {
			"Sales Order": {
				"doctype": "Purchase Order",
				"field_no_map": [
					"address_display",
					"contact_display",
					"contact_mobile",
					"contact_email",
					"contact_person",
					"taxes_and_charges"
				],
				"validation": {
					"docstatus": ["=", 1]
				}
			},
			"Sales Order Item": {
				"doctype": "Purchase Order Item",
				"field_map":  [
					["name", "sales_order_item"],
					["parent", "sales_order"],
					["stock_uom", "stock_uom"],
					["uom", "uom"],
					["conversion_factor", "conversion_factor"],
					["delivery_date", "schedule_date"]
		 		],
				"field_no_map": [
					"rate",
					"price_list_rate"
				],
				"postprocess": update_item
			}
		}, target_doc, set_missing_values)

	if target_doc.jenis_transaksi == "Non PPN":
		target_doc.taxes_and_charges = ""
		target_doc.taxes = []

	return target_doc


@frappe.whitelist()
def make_delivery_note_2(source_name, target_doc=None, skip_item_mapping=False):
	# frappe.msgprint("DN BARU")
	def set_missing_values(source, target):
		target.ignore_pricing_rule = 1
		target.run_method("set_missing_values")
		target.run_method("set_po_nos")
		target.run_method("calculate_taxes_and_totals")

		if source.company_address:
			target.update({'company_address': source.company_address})
		else:
			# set company address
			target.update(get_company_address(target.company))

		if target.company_address:
			target.update(get_fetch_values("Delivery Note", 'company_address', target.company_address))

	def update_item(source, target, source_parent):
		target.base_amount = (flt(source.qty) - flt(source.delivered_qty)) * flt(source.base_rate)
		target.amount = (flt(source.qty) - flt(source.delivered_qty)) * flt(source.rate)
		target.qty = flt(source.qty) - flt(source.delivered_qty)

		item = get_item_defaults(target.item_code, source_parent.company)
		item_group = get_item_group_defaults(target.item_code, source_parent.company)

		if item:
			target.cost_center = frappe.db.get_value("Project", source_parent.project, "cost_center") \
				or item.get("buying_cost_center") \
				or item_group.get("buying_cost_center")

	mapper = {
		"Sales Order": {
			"doctype": "Delivery Note",
			"validation": {
				"docstatus": ["=", 1]
			}
		},
		"Sales Taxes and Charges": {
			"doctype": "Sales Taxes and Charges",
			"add_if_empty": True
		},
		"Sales Team": {
			"doctype": "Sales Team",
			"add_if_empty": True
		},
		"Biaya Order Item": {
			"doctype": "DN Biaya Order Item",
			"add_if_empty": True
		}
	}

	if not skip_item_mapping:
		mapper["Sales Order Item"] = {
			"doctype": "Delivery Note Item",
			"field_map": {
				"rate": "rate",
				"name": "so_detail",
				"parent": "against_sales_order",
			},
			"postprocess": update_item,
			"condition": lambda doc: abs(doc.delivered_qty) < abs(doc.qty) and doc.delivered_by_supplier!=1
		}

	target_doc = get_mapped_doc("Sales Order", source_name, mapper, target_doc, set_missing_values)
	
	so_doc = frappe.get_doc("Sales Order",source_name)
	if so_doc.jenis_transaksi == "PPN":
		target_doc.naming_series = "SJ-P-.YY.-.MM.-.#####"
		target_doc.tax_status = "Tax"
	else:
		target_doc.naming_series = "SJ-N-.YY.-.MM.-.#####"
		target_doc.tax_status = "Non Tax"

	return target_doc

@frappe.whitelist()
def make_sales_invoice_2(source_name, target_doc=None, ignore_permissions=False):
	# cek payment schdule yg blum di gunakan
	# so_payment = frappe.db.sql(""" SELECT ps.name, ps.invoice_date, ps.invoice_portion
	# 		FROM `tabPayment Schedule` ps 
	# 		WHERE ps.parent="{}" AND ps.name NOT IN (SELECT payment_schedule_name FROM `tabSales Invoice` WHERE docstatus = 1 AND payment_schedule_name IS NOT NULL)
	# 		ORDER BY ps.idx limit 1 """.format(source_name), as_dict=1)

	# payment_schdule = so_payment[0] if so_payment and so_payment[0] else {}

	def postprocess(source, target):
		set_missing_values(source, target)
		# Get the advance paid Journal Entries in Sales Invoice Advance
		if target.get("allocate_advances_automatically"):
			target.set_advances()

		# target.payment_schedule_name = payment_schdule.name

	def set_missing_values(source, target):
		target.flags.ignore_permissions = True
		target.run_method("set_missing_values")
		target.run_method("set_po_nos")
		target.run_method("calculate_taxes_and_totals")

		if source.company_address:
			target.update({"company_address": source.company_address})
		else:
			# set company address
			target.update(get_company_address(target.company))

		if target.company_address:
			target.update(get_fetch_values("Sales Invoice", "company_address", target.company_address))

		# set the redeem loyalty points if provided via shopping cart
		if source.loyalty_points and source.order_type == "Shopping Cart":
			target.redeem_loyalty_points = 1

		target.debit_to = get_party_account("Customer", source.customer, source.company)

	def update_item(source, target, source_parent):
		target.amount = flt(source.amount) - flt(source.billed_amt)
		target.base_amount = target.amount * flt(source_parent.conversion_rate)
		target.qty = (
			target.amount / flt(source.rate)
			if (source.rate and source.billed_amt)
			else source.qty - source.returned_qty
		)

		# portion = flt(source.amount) * (payment_schdule.invoice_portion/100)
		# amount = flt(source.amount) - flt(source.billed_amt)
		# target.amount = portion if amount > portion and portion is not 0 else amount
		# target.base_amount = target.amount * flt(source_parent.conversion_rate)
		# target.qty = (
		# 	target.amount / flt(source.rate)
		# 	if (source.rate and (source.billed_amt or payment_schdule.invoice_portion))
		# 	else source.qty - source.returned_qty
		# )

		if source_parent.project:
			target.cost_center = frappe.db.get_value("Project", source_parent.project, "cost_center")
		if target.item_code:
			item = get_item_defaults(target.item_code, source_parent.company)
			item_group = get_item_group_defaults(target.item_code, source_parent.company)
			cost_center = item.get("selling_cost_center") or item_group.get("selling_cost_center")

			if cost_center:
				target.cost_center = cost_center

	# def update_schedule(source, target, source_parent):
	# 	# if source.name == list_payment['name'] if source.name not in list_payment.keys() else None
	# 	target.invoice_portion = 100
		
	doclist = get_mapped_doc(
		"Sales Order",
		source_name,
		{
			"Sales Order": {
				"doctype": "Sales Invoice",
				"field_map": {
					"party_account_currency": "party_account_currency",
					"payment_terms_template": "payment_terms_template",
				},
				"field_no_map": ["payment_terms_template"],
				"validation": {"docstatus": ["=", 1]},
			},
			"Sales Order Item": {
				"doctype": "Sales Invoice Item",
				"field_map": {
					"name": "so_detail",
					"parent": "sales_order",
				},
				"postprocess": update_item,
				"condition": lambda doc: doc.qty
				and (doc.base_amount == 0 or abs(doc.billed_amt) < abs(doc.amount)),
			},
			"Biaya Order Item": {
				"doctype": "SI Biaya Order Item",
				"add_if_empty": True
			},
			# "Payment Schedule": {
			# 	"doctype": "Payment Schedule",
			# 	"postprocess": update_schedule,
			# 	"condition": lambda doc: doc.name == payment_schdule.name if 'name' in payment_schdule.keys() else True, 
			# 	"add_if_empty": True,
			# },
			"Sales Taxes and Charges": {"doctype": "Sales Taxes and Charges", "add_if_empty": True},
			"Sales Team": {"doctype": "Sales Team", "add_if_empty": True},
		},
		target_doc,
		postprocess,
		ignore_permissions=ignore_permissions,
	)

	automatically_fetch_payment_terms = cint(
		frappe.db.get_single_value("Accounts Settings", "automatically_fetch_payment_terms")
	)
	if automatically_fetch_payment_terms:
		doclist.set_payment_schedule()

	doclist.set_onload("ignore_price_list", True)

	so_doc = frappe.get_doc("Sales Order",source_name)
	if so_doc.jenis_transaksi == "PPN":
		doclist.naming_series = "FJ-P-.YY.-.MM.-.#####"
		doclist.tax_status = "Tax"
	else:
		doclist.naming_series = "FJ-N-.YY.-.MM.-.#####"
		doclist.tax_status = "Non Tax"

	return doclist

@frappe.whitelist()
def make_purchase_order_2(source_name, selected_items=None, target_doc=None):
	if not selected_items:
		return

	if isinstance(selected_items, string_types):
		selected_items = json.loads(selected_items)

	items_to_map = [
		item.get("item_code")
		for item in selected_items
		if item.get("item_code") and item.get("item_code")
	]
	items_to_map = list(set(items_to_map))

	def is_drop_ship_order(target):
		drop_ship = True
		for item in target.items:
			if not item.delivered_by_supplier:
				drop_ship = False
				break

		return drop_ship

	def set_missing_values(source, target):
		target.supplier = ""
		target.apply_discount_on = ""
		target.additional_discount_percentage = 0.0
		target.discount_amount = 0.0
		target.inter_company_order_reference = ""
		target.shipping_rule = ""
		# frappe.msgprint(source.jenis_transaksi)

		if is_drop_ship_order(target):
			target.customer = source.customer
			target.customer_name = source.customer_name
			target.shipping_address = source.shipping_address_name
		else:
			target.customer = target.customer_name = target.shipping_address = None

		target.run_method("set_missing_values")
		target.run_method("calculate_taxes_and_totals")

	def update_item(source, target, source_parent):
		target.schedule_date = source.delivery_date
		target.qty = flt(source.qty) - (flt(source.ordered_qty) / flt(source.conversion_factor))
		target.stock_qty = flt(source.stock_qty) - flt(source.ordered_qty)
		target.project = source_parent.project

	def update_item_for_packed_item(source, target, source_parent):
		target.qty = flt(source.qty) - flt(source.ordered_qty)

	# po = frappe.get_list("Purchase Order", filters={"sales_order":source_name, "supplier":supplier, "docstatus": ("<", "2")})
	doc = get_mapped_doc(
		"Sales Order",
		source_name,
		{
			"Sales Order": {
				"doctype": "Purchase Order",
				"field_no_map": [
					"address_display",
					"contact_display",
					"contact_mobile",
					"contact_email",
					"contact_person",
					"taxes_and_charges",
					"shipping_address",
					"terms",
				],
				"validation": {"docstatus": ["=", 1]},
			},
			"Sales Order Item": {
				"doctype": "Purchase Order Item",
				"field_map": [
					["name", "sales_order_item"],
					["parent", "sales_order"],
					["stock_uom", "stock_uom"],
					["uom", "uom"],
					["conversion_factor", "conversion_factor"],
					["delivery_date", "schedule_date"],
				],
				"field_no_map": [
					"rate",
					"price_list_rate",
					"item_tax_template",
					"discount_percentage",
					"discount_amount",
					"supplier",
					"pricing_rules",
				],
				"postprocess": update_item,
				"condition": lambda doc: doc.ordered_qty < doc.stock_qty
				and doc.item_code in items_to_map
				and not is_product_bundle(doc.item_code),
			},
			"Packed Item": {
				"doctype": "Purchase Order Item",
				"field_map": [
					["name", "sales_order_packed_item"],
					["parent", "sales_order"],
					["uom", "uom"],
					["conversion_factor", "conversion_factor"],
					["parent_item", "product_bundle"],
					["rate", "rate"],
				],
				"field_no_map": [
					"price_list_rate",
					"item_tax_template",
					"discount_percentage",
					"discount_amount",
					"supplier",
					"pricing_rules",
				],
				"postprocess": update_item_for_packed_item,
				"condition": lambda doc: doc.parent_item in items_to_map,
			},
		},
		target_doc,
		set_missing_values,
	)

	set_delivery_date(doc.items, source_name)

	so_doc = frappe.get_doc("Sales Order",source_name)
	if so_doc.jenis_transaksi == "PPN":
		doc.naming_series = 'PUR-ORD-P-.YYYY.-'
		doc.tax_status = "Tax"
	else:
		doc.naming_series = 'PUR-ORD-NP-.YYYY.-'
		doc.taxes_and_charges = ''
		doc.taxes = []
		doc.tax_status = "Non Tax"

	return doc

@frappe.whitelist()
def allow_payment(dt, dn):
    
    delivery_note = frappe.db.exists("Delivery Note Item", {'against_sales_order' : dn, 'docstatus': ['<', 2]})
    sinv = frappe.db.exists("Sales Invoice Item", {'sales_order' : dn, 'docstatus': ['<', 2]})
    
    return 0 if delivery_note or sinv else 1

def is_product_bundle(item_code):
	return frappe.db.exists("Product Bundle", item_code)


def set_delivery_date(items, sales_order):
	delivery_dates = frappe.get_all(
		"Sales Order Item", filters={"parent": sales_order}, fields=["delivery_date", "item_code"]
	)

	delivery_by_item = frappe._dict()
	for date in delivery_dates:
		delivery_by_item[date.item_code] = date.delivery_date

	for item in items:
		if item.product_bundle:
			item.schedule_date = delivery_by_item[item.product_bundle]

def validate_payment_schedule_so(self, method): 
	self.meta.get_field("payment_schedule").allow_on_submit = 1
	base_grand_total = self.get("base_rounded_total") or self.base_grand_total
	grand_total = self.get("rounded_total") or self.grand_total

	for d in self.get("payment_schedule"):
		d.meta.get_field("base_payment_amount").allow_on_submit = 1
		d.meta.get_field("payment_amount").allow_on_submit = 1
		d.meta.get_field("outstanding").allow_on_submit = 1
		
		if d.invoice_portion:
			d.payment_amount = flt(
				grand_total * flt(d.invoice_portion / 100), d.precision("payment_amount")
			)
			d.base_payment_amount = flt(
				base_grand_total * flt(d.invoice_portion / 100), d.precision("base_payment_amount")
			)
			d.outstanding = d.payment_amount
		elif not d.invoice_portion:
			d.base_payment_amount = flt(
				d.payment_amount * self.get("conversion_rate"), d.precision("base_payment_amount")
			)
	self.flags.ignore_validate_update_after_submit = True