from odoo import models


class SaleSubscription(models.Model):
    _inherit = "sale.subscription"

    def generate_invoice(self):
        res = super().generate_invoice()

        tmpl_name = (
            "subscription_invoice_notify.mail_template_invoice_notify_responsible"  # noqa: E501
        )

        for subscription in self:
            responsible_user = subscription.user_id or self.env.ref("base.user_root")
            # Fetch all invoices related to the subscription
            invoices = subscription.invoice_ids.sorted(
                key=lambda r: r.id,
                reverse=True,
            )
            if invoices:
                template = self.env.ref(tmpl_name)
                template.send_mail(
                    subscription.id,
                    force_send=True,
                    email_values={
                        "email_to": responsible_user.email,
                    },
                )

        return res
