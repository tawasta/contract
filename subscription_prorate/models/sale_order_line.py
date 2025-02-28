from odoo import _, api, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.depends("product_id", "product_uom", "product_uom_qty")
    def _compute_price_unit(self):
        res = super()._compute_price_unit()

        for record in self:
            if record.product_id.subscription_price_prorate:
                (
                    discount,
                    period,
                    period_name,
                ) = record.order_id._get_subscription_prorate_info()

                if discount:
                    record.discount = discount
                    record.name += _(" ({} {})").format(period, period_name)

        return res

    def get_subscription_line_values(self):
        res = super().get_subscription_line_values()

        if self.product_id.subscription_price_prorate:
            # Don't give permanent discount
            res["discount"] = 0

        return res
