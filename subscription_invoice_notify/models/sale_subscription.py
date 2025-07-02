from odoo import models, _


class SaleSubscription(models.Model):
    _inherit = "sale.subscription"

    def generate_invoice(self):
        super().generate_invoice()

        for subscription in self:
            responsible_user = subscription.user_id or self.env.ref("base.user_root")
            # Hae kaikki tilaukseen liittyvät laskut
            invoices = subscription.invoice_ids.sorted(key=lambda r: r.id, reverse=True)
            if invoices:
                template = self.env.ref(
                    "subscription_invoice_notify.mail_template_invoice_notify_responsible"
                )
                template.send_mail(
                    subscription.id,
                    force_send=True,
                    email_values={
                        "email_to": responsible_user.email,
                    },
                )
