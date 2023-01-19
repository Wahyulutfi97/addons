// Copyright (c) 2020, DAS and contributors
// For license information, please see license.txt

frappe.ui.form.on('Form Komplain', {
	// refresh: function(frm) {

	// }
});

cur_frm.set_query("nomor_so", "sales_order", function(doc, cdt, cdn) {
	var d = locals[cdt][cdn];
	return{
		filters: [
			['Sales Order', 'customer', '=', doc.customer]
		]
	}
});

cur_frm.cscript.custom_sla = function(doc){
	if(doc.sla){
		if(doc.sla == "1 Bulan (Komplain Mesin Besar)"){
			doc.tanggal_sla = frappe.datetime.add_days(frappe.datetime.get_today(),30)
			refresh_field("tanggal_sla")
		}
		else if(doc.sla == "2 Minggu (Komplain Mesin Kecil)"){
			doc.tanggal_sla = frappe.datetime.add_days(frappe.datetime.get_today(),14)
			refresh_field("tanggal_sla")
		}
		else if(doc.sla == "1 Minggu (Komplain Bisa Dipandu Tanpa Kunjungan)"){
			doc.tanggal_sla = frappe.datetime.add_days(frappe.datetime.get_today(),7)
			refresh_field("tanggal_sla")
		}
	}
}
cur_frm.add_fetch("customer","customer_name","nama");
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
					doc.no_hp = r["message"][0][3]

					refresh_field("nama")
					refresh_field("kota")
					refresh_field("no_hp")
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
