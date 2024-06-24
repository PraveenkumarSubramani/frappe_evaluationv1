
import frappe
from frappe.model.document import Document
from frappe import sendmail
from frappe.model.document import Document

#for sending email to the tenant for payment due
@frappe.whitelist()
def send_payment_due_email():
    all_tenant = frappe.get_all("Contract Details")
    reminder = frappe.db.get_single_value("Airline Settings", "rent__reminder")
    for i in all_tenant:
        if reminder == 1:
            contract = frappe.get_doc("Contract Details", i.name)
            tenant = frappe.get_doc("Tenant Information", contract.tenant)
            tenant_email = tenant.email_id
            try:
                due_date = frappe.db.get_single_value("Airline Settings", "month_due_date")
                date = frappe.utils.getdate(frappe.utils.nowdate()).replace(day=due_date)
                # Compose the email subject and message
                subject = "Payment Due Reminder"
                message = f"Dear {tenant.tenant_name},\n\nThis is a reminder that your payment is due on{date}.\n\nPlease make the payment as soon as possible.\n\nThank you,\nThe Airport Shop Management Team"
                # Send the email
                sendmail(recipients=tenant_email, subject=subject, message=message)
            except Exception as e:
                frappe.msgprint(e)
                pass
            
# Run  bench execute airport_shop_management.airport_shop_management.doctype.cron.cron.send_payment_due_email