from odoo import models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    def _get_computed_name(self):
        res = super()._get_computed_name()

        if self.contract_line_id:
            res = f"{self.contract_line_id.contract_id.name} / {res}"

        return res
