from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def create_subscription(self, lines, subscription_tmpl):
        res = super().create_subscription(lines, subscription_tmpl)

        if (
            self.partner_id != self.partner_invoice_id
            and self.partner_invoice_id.is_company
        ):
            # Use invoice address as partner for the new subscription
            # The create_subscription() doesn't return the created subscription,
            # and we have to refer to subscription_ids
            self.subscription_ids.write({"partner_id": self.partner_invoice_id})

            lines = self.subscription_ids.mapped("sale_subscription_line_ids")
            commercial_lines = lines.filtered(
                lambda r: r.product_id.subscription_commercial
            )

            # Set commercial product lines partner to be invoice address
            commercial_lines.write({"partner_id": self.partner_invoice_id})

        return res
