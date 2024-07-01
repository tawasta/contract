from odoo import models


class ContractLine(models.Model):
    _inherit = "contract.line"

    def _check_last_date_invoiced(self):
        for rec in self.filtered("last_date_invoiced"):
            # Skip the check for next invoice date / recurring next date
            if (
                rec.recurring_next_date
                and rec.recurring_next_date <= rec.last_date_invoiced
            ):
                # Skip this constraint
                continue

            # Check other constraints
            super()._check_last_date_invoiced()
