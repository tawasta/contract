from odoo import _

from odoo.addons.subscription_oca.models.sale_subscription import SaleSubscription


def generate_invoice(self):
    invoice_number = ""
    msg_static = _("Created invoice with reference")  # noqa: F841
    if self.template_id.invoicing_mode in ["draft", "invoice", "invoice_send"]:
        invoice = self.create_invoice()
        if self.template_id.invoicing_mode != "draft":
            invoice.action_post()
            mail_template = self.template_id.invoice_mail_template_id
            invoice.with_context(force_send=True)._generate_pdf_and_send_invoice(
                mail_template
            )
            invoice_number = invoice.name
            message_body = (  # noqa: F841
                f"<b>{msg_static}</b> "
                f"<a href=# data-oe-model=account.move data-oe-id={invoice.id}>"
                f"{invoice_number}"
                "</a>"
            )

    if self.template_id.invoicing_mode == "sale_and_invoice":
        order_id = self.create_sale_order()
        order_id.action_confirm()
        order_id.action_lock()
        new_invoice = order_id._create_invoices()
        new_invoice.action_post()
        new_invoice.invoice_origin = order_id.name + ", " + self.name
        invoice_number = new_invoice.name
        message_body = (  # noqa: F841
            "<b>%s</b> <a href=# data-oe-model=account.move data-oe-id=%d>%s</a>"
            % (msg_static, new_invoice.id, invoice_number)
        )
    if not invoice_number:
        invoice_number = _("To validate")
        message_body = f"<b>{msg_static}</b> {invoice_number}"  # noqa: F841
    self.calculate_recurring_next_date(self.recurring_next_date)


SaleSubscription.generate_invoice = generate_invoice
