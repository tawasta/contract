from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def create_subscription(self, lines, subscription_tmpl):
        # Try to find existing subscription
        subscription = self.env["sale.subscription"]
        existing_subscription = subscription.search(
            [
                ("partner_id", "=", self.partner_id.id),
                ("template_id", "=", subscription_tmpl.id),
            ],
            limit=1,
        )

        if existing_subscription:
            subscription_lines = []
            for line in lines:
                subscription_lines.append((0, 0, line.get_subscription_line_values()))

            # Add to existing subscription
            existing_subscription.write(
                {"sale_subscription_line_ids": subscription_lines}
            )
        else:
            # Create a new subscription
            return super().create_subscription(lines, subscription_tmpl)
