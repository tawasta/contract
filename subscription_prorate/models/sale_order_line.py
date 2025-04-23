from odoo import _, api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    prorated_period = fields.Integer()
    prorated_period_name = fields.Char()

    @api.depends("product_id", "product_uom", "product_uom_qty")
    def _compute_price_unit(self):
        res = super()._compute_price_unit()

        for record in self:
            if record.order_id and record.product_id.subscription_price_prorate:
                (
                    discount,
                    period,
                    period_name,
                ) = record.order_id._get_subscription_prorate_info()

                if discount:
                    record._compute_name()
                    line_name = _("{} ({} {})").format(record.name, period, period_name)

                    vals = {
                        "name": line_name,
                        "discount": discount,
                        "prorated_period": period,
                        "prorated_period_name": period_name,
                    }

                    record.write(vals)
        return res

    def get_subscription_line_values(self):
        res = super().get_subscription_line_values()

        if self.product_id.subscription_price_prorate:
            # Don't give permanent discount
            res["discount"] = 0

        return res
