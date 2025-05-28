from odoo import models


class SaleSubscription(models.Model):
    _inherit = "sale.subscription"

    def _split_lines(self, subscriptions):
        for subscription in subscriptions:
            new_lines = []
            for line in subscription.sale_subscription_line_ids:
                if (
                    line.product_id.force_split_subscription_lines
                    and line.product_uom_qty > 1
                ):
                    original_qty = int(line.product_uom_qty)
                    line.product_uom_qty = 1

                    for _ in range(original_qty - 1):
                        values = line.copy_data()[0]
                        values["product_uom_qty"] = 1
                        new_lines.append((0, 0, values))

            if new_lines:
                subscription.write({"sale_subscription_line_ids": new_lines})

    def write(self, vals):
        old_line_ids = {line.id for line in self.sale_subscription_line_ids}
        res = super().write(vals)

        new_lines = self.sale_subscription_line_ids.filtered(
            lambda li: li.id not in old_line_ids
        )
        affected_subs = self.filtered(
            lambda s: any(
                line.product_id.force_split_subscription_lines
                and line.product_uom_qty > 1
                for line in new_lines
            )
        )
        self._split_lines(affected_subs)
        return res

    def create(self, vals):
        record = super().create(vals)
        self._split_lines(record)
        return record
