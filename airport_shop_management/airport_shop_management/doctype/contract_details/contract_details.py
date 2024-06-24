# Copyright (c) 2024, geethanjali and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import sendmail
from frappe.model.document import Document
from frappe.website.website_generator import WebsiteGenerator
from datetime import datetime, date


class ContractDetails(WebsiteGenerator):
    def on_submit(self):
        shop = frappe.get_doc("Shop", self.shop)
        shop.status = "Booked"
        shop.save()
        
# for update the status of the shop
# Run bench execute airport_shop_management.airport_shop_management.doctype.contract_details.contract_details.status_updation
@frappe.whitelist(allow_guest=True)
def status_updation():
    contract_details = frappe.get_all("Contract Details", filters={"docstatus":1})
    for i in contract_details:
        contract = frappe.get_doc("Contract Details", i.name)
        try:
            fr_date = contract.from_date
            to_date = contract.date_of_expiry
            from_date = datetime.strptime(str(fr_date), "%Y-%m-%d").date()
            to_date = datetime.strptime(str(to_date), "%Y-%m-%d").date()
            today = date.today()
            if from_date == today:
                shop = frappe.get_last_doc("Shop", filters={'name': contract.shop, 'status': 'Booked'})
                shop.status = "Occupied"
                shop.save()
            if to_date == today:
                shop = frappe.get_last_doc("Shop", filters={'name': contract.shop, 'status': 'Occupied'})
                shop.status = "Available"
                shop.save()
        except Exception as e:
            frappe.errprint(e)
            pass
