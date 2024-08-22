from odoo import fields, models


class SubscriptionLine(models.Model):
    _inherit = "sale.subscription.line"

    partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Related partner",
        compute="_compute_partner_id",
        precompute=True,
        store=True,
    )

    def _compute_partner_id(self):
        for line in self:
            line.partner_id = line.sale_subscription_id.partner_id
