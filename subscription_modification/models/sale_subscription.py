from odoo import fields
from odoo import models


class SaleSubscription(models.Model):
    _inherit = "sale.subscription"

    modification_ids = fields.One2many(
        comodel_name="sale.subscription.modification",
        inverse_name="subscription_id",
        string="Modifications",
    )

    def modification_add(self, description, date=False):
        # Helper for adding modifications
        if not date:
            date = fields.Date.today()

        modification = self.env["sale.subscription.modification"]

        for record in self:
            values = {
                "subscription_id": record.id,
                "description": description,
                "date": date,
            }
            modification.create(values)
