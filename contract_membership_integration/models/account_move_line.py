from odoo import models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    def _get_computed_name(self):
        res = super()._get_computed_name()

        if self.contract_line_id:
            res = f"{self.contract_line_id.contract_id.name} / {res}"

        # If the product is a membership product, add the period
        if self.product_id.membership:
            res = f"{res} {self.product_id.membership_date_from.year}"

        return res
