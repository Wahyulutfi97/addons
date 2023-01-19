cur_frm.add_fetch("item","item_name","item_name")

cur_frm.fields.forEach(function(l){ 
	if(!cur_frm.doc.__islocal){
		if (l.df.fieldname == "lead_name" 
			|| l.df.fieldname == "lead_owner"
			|| l.df.fieldname == "company_name" 
			|| l.df.fieldname == "status"  
			|| l.df.fieldname == "email_id"  
			|| l.df.fieldname == "gender"  
			|| l.df.fieldname == "nomor_whatsapp_1"  
			|| l.df.fieldname == "kota"  
			|| l.df.fieldname == "sales_yang_menghandle" 
			|| l.df.fieldname == "source"   
		){
			if(!frappe.user.has_role("Gatekeeper")){
				cur_frm.set_df_property(l.df.fieldname, "read_only", 1);
			} 
		}

	}
})