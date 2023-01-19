
cur_frm.fields.forEach(function(l){ 
	if(!cur_frm.doc.__islocal){
		if (l.df.fieldtype == "Currency" || l.df.fieldname == "in_words" || l.df.fieldname == "payment_schedule" || l.df.fieldname == "taxes"){
			if(frappe.user.has_role("Gudang")){
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

}

frappe.ui.form.on('Purchase Order', {
	jenis_transaksi: function(frm){
	    if (frm.doc.jenis_transaksi == "PPN"){
	        frm.set_value("taxes_and_charges","PPN 11% - D");
	        frm.set_value("tax_status","Tax")
	        frm.set_value("naming_series","PUR-ORD-P-.YYYY.-");

	    } else if (frm.doc.jenis_transaksi == "Non PPN"){
	    	for (var i = frm.doc.taxes.length - 1; i >= 0; i--) {
	    		frappe.model.set_value(cur_frm.doc.taxes[i].doctype,cur_frm.doc.taxes[i].name,"rate",0)
	    	}
	        frm.set_value("taxes_and_charges",null);
	        frm.set_value("taxes",null);
	        frm.refresh_field("taxes");

	        frm.set_value("tax_status","Non Tax")
	        frm.set_value("naming_series","PUR-ORD-NP-.YYYY.-");
	    }
	},
	validate: function(frm){
	    if (frm.doc.jenis_transaksi == "PPN"){
	        frm.set_value("tax_status","Tax")
	        frm.set_value("naming_series","PUR-ORD-P-.YYYY.-");

	    } else if (frm.doc.jenis_transaksi == "Non PPN"){
	        frm.set_value("tax_status","Non Tax")
	        frm.set_value("naming_series","PUR-ORD-NP-.YYYY.-");
	    }
	}
})