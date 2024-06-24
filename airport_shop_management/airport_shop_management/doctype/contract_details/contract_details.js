// Copyright (c) 2024, geethanjali and contributors
// For license information, please see license.txt

frappe.ui.form.on("Contract Details", {
	onload:async function(frm) {
        console.log('refresh')
        var rentAmount = await frappe.db.get_single_value('Airline Settings', 'default_rent_amount');
        console.log(rentAmount);
        if (rentAmount > 0) {
            frm.set_value('rent_amount', rentAmount);
            frm.set_df_property('rent_amount', 'read_only', 1);
            frm.refresh_field('rent_amount')
        }
        frm.set_query('shop', function() {
            return {
                filters: {
                    status: 'Available'
                }
            };
        });
       
	},
});
