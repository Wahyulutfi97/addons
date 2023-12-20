cur_frm.fields.forEach(function(l){ 
	if(!cur_frm.doc.__islocal){
		if (l.df.fieldtype == "Currency" || l.df.fieldname == "in_words" || l.df.fieldname == "payment_schedule" || l.df.fieldname == "taxes"){
			if(frappe.user.has_role("Gudang") && frappe.user.name != "Administrator" ){
				cur_frm.set_df_property(l.df.fieldname, "hidden", 1);
			} 
		}

	}
})

cur_frm.cscript.custom_refresh = function(doc){
	if(!cur_frm.doc.__islocal){
		if(frappe.user.has_role("Gudang") && frappe.user.name != "Administrator"){
			cur_frm.fields_dict.items.grid.set_column_disp("rate", false);
			cur_frm.fields_dict.items.grid.set_column_disp("amount", false);
			cur_frm.fields_dict.items.grid.set_column_disp("price_list_rate", false);
			cur_frm.fields_dict.items.grid.set_column_disp("billed_amt", false);
			cur_frm.fields_dict.items.grid.set_column_disp("valuation_rate", false);
			cur_frm.fields_dict.items.grid.set_column_disp("gross_profit", false);
			cur_frm.fields_dict.items.grid.set_column_disp("blanket_order_rate", false);
		}
	}

	if(doc.jenis_transaksi == "PPN"){

	}

}

frappe.ui.form.on('Sales Order', {
	setup(frm){

		// if(frm.doc.jenis_transaksi == "PPN"){
		// 	if(frm.doc.docstatus == 0 && !frm.doc.taxes_and_charges){
		// 		frm.call({
		// 			method: "erpnext.controllers.accounts_controller.get_taxes_and_charges",
		// 			args: {
		// 				"master_doctype": frappe.meta.get_docfield(frm.doc.doctype, "taxes_and_charges",frm.doc.name).options,
		// 				"master_name": "PPN 11% - D"
		// 			},
		// 			callback: function(r) {
		// 				if(!r.exc) {
		// 					for (let tax of r.message) {
		// 						frm.add_child("taxes", tax);
		// 					}
		// 					// if(frm.doc.shipping_rule && frm.doc.taxes) {
	
		// 					// 	refresh_field("taxes");
		// 					// } else {
		// 					// 	frm.set_value("taxes", r.message);
		// 					// 	frm.cscript.calculate_taxes_and_totals();
		// 					// }
		// 				}
		// 			}
		// 		});
		// 	}
		// }
	},
	refresh(frm) {
		if(frm.doc.jenis_transaksi == "PPN"){
			frm.set_value("naming_series","SO-P-.YY.MM.DD.-.#####");
		}else{
			frm.set_value("naming_series","SO-NP-.YY.MM.DD.-.#####");
		}
		// frm.remove_custom_button("Sales Order","Update Items");
		cur_frm.remove_custom_button(__('Update Items'));
		if(frm.doc.docstatus === 1 && frm.doc.status !== 'Closed'){
			// && flt(frm.doc.per_delivered, 6) < 100 && flt(frm.doc.per_billed, 6) < 100) {
			// frm.add_custom_button(__('Update Items'), () => {
			// 	erpnext.utils.update_child_items({
			// 		frm: frm,
			// 		child_docname: "items",
			// 		child_doctype: "Sales Order Detail",
			// 		cannot_add_row: false,
			// 	})
			// });
		}
        // your code here
        // if(frm.doc.docstatus == 1 && frm.doc.per_billed == 0 && frm.doc.per_delivered == 0)
        // {
        //     frappe.call({
        //         method: "addons.custom_method.sales_order.allow_payment",
        //         args: {
        //             "dt": frm.doc.doctype,
        //             "dn": frm.doc.name
        //         },
        //         callback: function(r) {
        //             frm.set_df_property('payment_schedule', 'allow_on_submit', r.message);
        //         }
        //     });
        // }
    },
	jenis_transaksi: function(frm){
	    if (frm.doc.jenis_transaksi == "PPN"){
	        frm.set_value("taxes_and_charges", "PPN 11% - D");



	        frm.set_value("tax_status","Tax")
	        frm.set_value("naming_series","SO-P-.YY.MM.DD.-.#####");

	    } else if (frm.doc.jenis_transaksi == "Non PPN"){
	    	for (var i = frm.doc.taxes.length - 1; i >= 0; i--) {
	    		frappe.model.set_value(cur_frm.doc.taxes[i].doctype,cur_frm.doc.taxes[i].name,"rate",0)
	    	}
	        frm.set_value("taxes_and_charges",null);
	        frm.set_value("taxes",null);
	        frm.refresh_field("taxes");

	        frm.set_value("tax_status","Non Tax")
	        frm.set_value("naming_series","SO-NP-.YY.MM.DD.-.#####");
	    }
	},
});


cur_frm.add_fetch("item","item_name","item_name")
cur_frm.add_fetch("customer","source","source")
frappe.ui.form.on('Biaya Order Item', {

	item: function(frm,cdt,cdn){
		if(locals[cdt][cdn].item && locals[cdt][cdn].biaya){
			frappe.call({
				method: "frappe.client.get",
				args: {
					doctype: "Item",
					name: locals[cdt][cdn].item
				},
				callback: function (data) {
					if(data){
						if(data.message["biaya_account"]){
							let item_code = locals[cdt][cdn].item
							let biaya = locals[cdt][cdn].biaya
							let account = data.message["biaya_account"]
							let check = 0
							for(var row in cur_frm.doc.taxes){
								if(cur_frm.doc.taxes[row].item_name == item_code){
									check = 1
									cur_frm.doc.taxes[row].tax_amount = biaya
								}
							}
							if(check == 0){
								var d = frappe.model.add_child(cur_frm.doc, "Sales Taxes and Charges", "taxes")
								d.charge_type = "Actual"
								d.account_head = account
								d.item_name = item_code
								d.tax_amount = biaya
								d.description = "Biaya Item"
							}
							

							frm.refresh_fields()
						}
					} 
				}
			})
		}
	},
	biaya: function(frm,cdt,cdn){
		if(locals[cdt][cdn].item && locals[cdt][cdn].biaya){
			frappe.call({
				method: "frappe.client.get",
				args: {
					doctype: "Item",
					name: locals[cdt][cdn].item
				},
				callback: function (data) {
					if(data){
						if(data.message["biaya_account"]){
							let item_code = locals[cdt][cdn].item
							let biaya = locals[cdt][cdn].biaya
							let account = data.message["biaya_account"]
							let check = 0
							for(var row in cur_frm.doc.taxes){
								if(cur_frm.doc.taxes[row].item_name == item_code){
									check = 1
									cur_frm.doc.taxes[row].tax_amount = biaya
								}
							}
							if(check == 0){
								var d = frappe.model.add_child(cur_frm.doc, "Sales Taxes and Charges", "taxes")
								d.charge_type = "Actual"
								d.account_head = account
								d.item_name = item_code
								d.tax_amount = biaya
								d.description = "Biaya Item"
							}
							

							frm.refresh_fields()
						}
					} 
				}
			})
		}
	}
});
