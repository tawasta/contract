from odoo import models


class ContractLine(models.Model):
    _inherit = "contract.line"

    def _check_last_date_invoiced(self):
        # Records where the check should be skipped
        skip = self.filtered(
            lambda r: r.last_date_invoiced
            and r.recurring_next_date
            and r.recurring_next_date <= r.last_date_invoiced
        )

        # Records that must be validated by parent constraint
        to_check = self.filtered("last_date_invoiced") - skip

        if to_check:
            return super(ContractLine, to_check)._check_last_date_invoiced()
        # For others, simply return None (implicitly)
        else:
            return None
