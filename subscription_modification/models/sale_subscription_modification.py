from odoo import fields
from odoo import models


class SaleSubscription(models.Model):
    _name = "sale.subscription.modification"
    _description = "Subscription Modification"
    _order = "date DESC, id DESC"

    date = fields.Date(required=True)
    description = fields.Text(required=True)
    subscription_id = fields.Many2one(
        string="Subscription",
        comodel_name="sale.subscription",
        required=True,
        ondelete="cascade",
        index=True,
    )
