from odoo import api, fields, models


class SubscriptionLine(models.Model):
    _inherit = "sale.subscription.line"

    purchase_price = fields.Float(
        string="Cost",
        compute="_compute_purchase_price",
        store=True,
        readonly=False,
        digits="Product Price",
    )

    def _get_purchase_price(self):
        self.ensure_one()
        return self.product_id.standard_price

    @api.depends("product_id")
    def _compute_purchase_price(self):
        for line in self:
            line.purchase_price = line._get_purchase_price()

    def _prepare_account_move_line(self):
        res = super()._prepare_account_move_line()

        res["purchase_price"] = self.purchase_price

        return res
