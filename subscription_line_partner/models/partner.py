from odoo import api, fields, models


class Partner(models.Model):
    _inherit = "res.partner"

    subscription_line_ids = fields.One2many(
        comodel_name="sale.subscription.line",
        inverse_name="partner_id",
        string="Subscription lines",
        domain=[("sale_subscription_id.in_progress", "=", True)],
    )
