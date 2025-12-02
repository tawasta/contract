from odoo import models


class SaleSubscription(models.Model):
    _inherit = "sale.subscription"

    def _prepare_account_move(self, line_ids):
        res = super()._prepare_account_move(line_ids)

        res["company_id"] = self.company_id.id

        return res
