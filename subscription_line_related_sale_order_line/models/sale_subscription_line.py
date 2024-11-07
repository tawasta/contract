from odoo import fields
from odoo import models


class SaleSubscriptionLine(models.Model):
    _inherit = "sale.subscription.line"

    sale_order_id = fields.Many2one(
        comodel_name="sale.order",
        string="Sale order",
        related="sale_order_line_id.order_id",
    )

    sale_order_line_id = fields.Many2one(
        comodel_name="sale.order.line",
        string="Sale order line",
        readonly=1,
    )
