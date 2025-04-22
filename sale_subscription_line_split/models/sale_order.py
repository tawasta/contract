from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def create_subscription(self, lines, subscription_tmpl):
        # Step 1: Call the core logic first
        result = super().create_subscription(lines, subscription_tmpl)

        # Step 2: Post-process subscriptions
        for subscription in self.subscription_ids:
            new_lines = []

            for line in subscription.sale_subscription_line_ids:
                if (
                    line.product_id.force_split_subscription_lines
                    and line.product_uom_qty > 1
                ):
                    original_qty = int(line.product_uom_qty)

                    # Step 2.1: Set the original line's qty to 1
                    line.product_uom_qty = 1

                    # Step 2.2: Create (qty - 1) new identical lines
                    for _ in range(original_qty - 1):
                        values = line.copy_data()[0]
                        values["product_uom_qty"] = 1
                        new_lines.append((0, 0, values))

            # Step 3: Add new lines in batch
            if new_lines:
                subscription.write({"sale_subscription_line_ids": new_lines})

        return result
