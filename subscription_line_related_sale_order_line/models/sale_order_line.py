from odoo import fields
from odoo import models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def get_subscription_line_values(self):
        res = super().get_subscription_line_values()
        res["sale_order_line_id"] = self.id

        return res
