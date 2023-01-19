// Copyright (c) 2020, DAS and contributors
// For license information, please see license.txt

frappe.ui.form.on('Customer Care', {
	// refresh: function(frm) {

	// }

});

cur_frm.set_query("nomor_so", "sales_order_table", function(doc, cdt, cdn) {
	var d = locals[cdt][cdn];
	return{
		filters: [
			['Sales Order', 'customer', '=', doc.customer]
		]
	}
});

cur_frm.set_query("item_code", function(doc) {
	var filter = ""
	for(var row in doc.sales_order_table){
		filter=filter+doc.sales_order_table[row].nomor_so+"|"
	}
	return {
		query: "addons.addons.doctype.customer_care.customer_care.get_so_items",
		filters: { 'sales_order': filter }
	}
});

cur_frm.add_fetch("item_code","item_name","item_name");
cur_frm.add_fetch("customer","customer_name","customer_name");
cur_frm.cscript.custom_customer = function(doc){
	if(doc.customer){
		frappe.call({
			method: "addons.addons.doctype.customer_care.customer_care.get_customer_details",
			args: {
				customer: doc.customer
			},
			callback: function(r) {
				if(r["message"]){
					doc.nama = r["message"][0][0]
					doc.kota = r["message"][0][1]
					doc.alamat =  r["message"][0][2]
					doc.no_hp = r["message"][0][3]
					doc.email = r["message"][0][4]

					refresh_field("nama")
					refresh_field("kota")
					refresh_field("alamat")
					refresh_field("no_hp")
					refresh_field("email")
				}
				

			}
		});
	}
}

cur_frm.set_query("customer", function(doc, cdt, cdn) {
	return {
		query:"addons.addons.doctype.customer_care.customer_care.get_customer_query",
	}
});
