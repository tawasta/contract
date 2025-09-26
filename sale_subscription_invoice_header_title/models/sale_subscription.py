from odoo import fields, models


class SaleSubscription(models.Model):
    _inherit = "sale.subscription"

    header_text = fields.Char(string="Header text")

    def _prepare_account_move(self, line_ids):
        values = super()._prepare_account_move(line_ids)
        if self.header_text:
            values["header_text"] = self.header_text
        return values
