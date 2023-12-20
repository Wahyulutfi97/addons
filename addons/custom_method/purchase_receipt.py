# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt


import frappe
from frappe import _, throw
from frappe.desk.notifications import clear_doctype_notifications
from frappe.model.mapper import get_mapped_doc
from frappe.utils import cint, flt, getdate, nowdate
from six import iteritems

import erpnext
from erpnext.accounts.utils import get_account_currency
from erpnext.assets.doctype.asset.asset import get_asset_account, is_cwip_accounting_enabled
from erpnext.assets.doctype.asset_category.asset_category import get_asset_category_account
from erpnext.buying.utils import check_on_hold_or_closed_status
from erpnext.controllers.buying_controller import BuyingController
from erpnext.stock.doctype.delivery_note.delivery_note import make_inter_company_transaction

form_grid_templates = {"items": "templates/form_grid/item_grid.html"}

def get_returned_qty_map(purchase_receipt):
	"""returns a map: {so_detail: returned_qty}"""
	returned_qty_map = frappe._dict(
		frappe.db.sql(
			"""select pr_item.purchase_receipt_item, abs(pr_item.qty) as qty
		from `tabPurchase Receipt Item` pr_item, `tabPurchase Receipt` pr
		where pr.name = pr_item.parent
			and pr.docstatus = 1
			and pr.is_return = 1
			and pr.return_against = %s
	""",
			purchase_receipt,
		)
	)

	return returned_qty_map

def get_invoiced_qty_map(purchase_receipt):
	"""returns a map: {pr_detail: invoiced_qty}"""
	invoiced_qty_map = {}

	for pr_detail, qty in frappe.db.sql(
		"""select pr_detail, qty from `tabPurchase Invoice Item`
		where purchase_receipt=%s and docstatus=1""",
		purchase_receipt,
	):
		if not invoiced_qty_map.get(pr_detail):
			invoiced_qty_map[pr_detail] = 0
		invoiced_qty_map[pr_detail] += qty

	return invoiced_qty_map

@frappe.whitelist()
def make_purchase_invoice_2(source_name, target_doc=None):
	# frappe.msgprint("PREC new")
	from erpnext.accounts.party import get_payment_terms_template

	doc = frappe.get_doc("Purchase Receipt", source_name)
	returned_qty_map = get_returned_qty_map(source_name)
	invoiced_qty_map = get_invoiced_qty_map(source_name)

	def set_missing_values(source, target):
		if len(target.get("items")) == 0:
			frappe.throw(_("All items have already been Invoiced/Returned"))

		doc = frappe.get_doc(target)
		doc.payment_terms_template = get_payment_terms_template(
			source.supplier, "Supplier", source.company
		)
		doc.run_method("onload")
		doc.run_method("set_missing_values")
		doc.run_method("calculate_taxes_and_totals")
		doc.set_payment_schedule()

	def update_item(source_doc, target_doc, source_parent):
		target_doc.qty, returned_qty = get_pending_qty(source_doc)
		if frappe.db.get_single_value(
			"Buying Settings", "bill_for_rejected_quantity_in_purchase_invoice"
		):
			target_doc.rejected_qty = 0
		target_doc.stock_qty = flt(target_doc.qty) * flt(
			target_doc.conversion_factor, target_doc.precision("conversion_factor")
		)
		returned_qty_map[source_doc.name] = returned_qty

	def get_pending_qty(item_row):
		qty = item_row.qty
		if frappe.db.get_single_value(
			"Buying Settings", "bill_for_rejected_quantity_in_purchase_invoice"
		):
			qty = item_row.received_qty
		pending_qty = qty - invoiced_qty_map.get(item_row.name, 0)
		returned_qty = flt(returned_qty_map.get(item_row.name, 0))
		if returned_qty:
			if returned_qty >= pending_qty:
				pending_qty = 0
				returned_qty -= pending_qty
			else:
				pending_qty -= returned_qty
				returned_qty = 0
		return pending_qty, returned_qty

	doclist = get_mapped_doc(
		"Purchase Receipt",
		source_name,
		{
			"Purchase Receipt": {
				"doctype": "Purchase Invoice",
				"field_map": {
					"supplier_warehouse": "supplier_warehouse",
					"is_return": "is_return",
					"bill_date": "bill_date",
				},
				"validation": {
					"docstatus": ["=", 1],
				},
			},
			"Purchase Receipt Item": {
				"doctype": "Purchase Invoice Item",
				"field_map": {
					"name": "pr_detail",
					"parent": "purchase_receipt",
					"purchase_order_item": "po_detail",
					"purchase_order": "purchase_order",
					"is_fixed_asset": "is_fixed_asset",
					"asset_location": "asset_location",
					"asset_category": "asset_category",
				},
				"postprocess": update_item,
				"filter": lambda d: get_pending_qty(d)[0] <= 0
				if not doc.get("is_return")
				else get_pending_qty(d)[0] > 0,
			},
			"Purchase Taxes and Charges": {"doctype": "Purchase Taxes and Charges", "add_if_empty": True},
		},
		target_doc,
		set_missing_values,
	)

	doclist.set_onload("ignore_price_list", True)

	so_doc = frappe.get_doc("Purchase Receipt",source_name)
	if so_doc.jenis_transaksi == "PPN":
		doclist.naming_series = "ACC-PINV-P-.YYYY.-"
		doclist.tax_status = "Tax"
	else:
		doclist.naming_series = "ACC-PINV-NP-.YYYY.-"
		doclist.tax_status = "Non Tax"

	return doclist