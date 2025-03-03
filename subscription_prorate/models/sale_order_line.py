from odoo import _, api, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.depends("product_id", "product_uom", "product_uom_qty")
    def _compute_price_unit(self):
        res = super()._compute_price_unit()

        if not self.product_id.subscription_price_prorate:
            return res

        discount, period, period_name = self.order_id._get_subscription_prorate_info()

        if discount:
            self.discount = discount
            self.name += _(" ({} {})").format(period, period_name)

        return res

    def get_subscription_line_values(self):
        res = super().get_subscription_line_values()

        if self.product_id.subscription_price_prorate:
            # Don't give permanent discount
            res["discount"] = 0

        return res
