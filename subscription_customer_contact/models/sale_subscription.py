from odoo import fields, models


class SaleSubscription(models.Model):
    _inherit = "sale.subscription"

    customer_contact_id = fields.Many2one(
        comodel_name="res.partner",
        string="Customer Contact",
        help="Primary customer contact for this subscription.",
    )

    def _prepare_account_move(self, line_ids):
        values = super()._prepare_account_move(line_ids)
        if self.customer_contact_id:
            values["customer_contact_id"] = self.customer_contact_id.id
        return values
