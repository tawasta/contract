from odoo import fields
from odoo import models
from odoo import _


class SaleSubscription(models.Model):
    _inherit = "sale.subscription"

    sale_subscription_closed_line_ids = fields.One2many(
        comodel_name="sale.subscription.line",
        inverse_name="sale_subscription_id",
        domain=[("active", "=", False)],
        context={"active_test": False},
    )

    def recompute_total(self):
        for record in self:
            record._compute_total()
