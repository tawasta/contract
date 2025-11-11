from odoo import models


class SaleSubscriptionLine(models.Model):
    _inherit = "sale.subscription.line"

    NAME_SUFFIX = " (#START# - #END#)"

    def _compute_name(self):
        result = super()._compute_name()

        for rec in self:
            if rec.product_id and rec.name:
                name = rec.name.strip()
                if self.NAME_SUFFIX not in name:
                    rec.name = f"{name}{self.NAME_SUFFIX}"

        return result
