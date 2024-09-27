from odoo import fields
from odoo import models


class SaleSubscription(models.Model):
    _inherit = "sale.subscription"

    modification_ids = fields.One2many(
        comodel_name="sale.subscription.modification",
        inverse_name="subscription_id",
        string="Modifications",
    )
