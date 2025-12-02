from odoo import models


class SaleSubscriptionLine(models.Model):
    _inherit = "sale.subscription.line"

    def _prepare_account_move_line(self):
        res = super()._prepare_account_move_line()

        # Company-aware accounting account
        account = (
            self.product_id.with_company(self.company_id).property_account_income_id
            or self.product_id.with_company(
                self.company_id
            ).categ_id.property_account_income_categ_id
        )

        res["account_id"] = account.id

        return res
