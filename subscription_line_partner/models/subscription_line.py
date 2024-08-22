from odoo import fields, models


class SubscriptionLine(models.Model):
    _inherit = "sale.subscription.line"

    partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Related partner",
    )
