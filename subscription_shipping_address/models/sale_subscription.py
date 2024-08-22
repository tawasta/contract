from odoo import fields
from odoo import models


class SaleSubscription(models.Model):
    _inherit = "sale.subscription"

    partner_shipping_id = fields.Many2one(
        comodel_name="res.partner",
        string="Delivery address",
    )

    def _prepare_account_move(self, line_ids):
        values = super()._prepare_account_move(line_ids)

        if self.partner_shipping_id:
            values["partner_shipping_id"] = self.partner_shipping_id.id

        return values
