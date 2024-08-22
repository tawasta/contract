from odoo import fields
from odoo import models


class SaleSubscription(models.Model):
    _inherit = "sale.subscription"

    invoice_ref = fields.Char(
        "Customer reference", help="Customer reference for invoices"
    )

    def _prepare_account_move(self, line_ids):
        values = super()._prepare_account_move(line_ids)

        if self.invoice_ref:
            values["ref"] = self.invoice_ref

        return values
