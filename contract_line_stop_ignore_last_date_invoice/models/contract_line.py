from odoo import models


class ContractLine(models.Model):
    _inherit = "contract.line"

    def _check_last_date_invoiced(self):
        # Records for which we skip the check
        skip = self.filtered(
            lambda r: r.recurring_next_date
            and r.recurring_next_date <= r.last_date_invoiced
        )

        # Records that still need validation
        to_check = self - skip

        if to_check:
            return super(ContractLine, to_check)._check_last_date_invoiced()
        else:
            return None
