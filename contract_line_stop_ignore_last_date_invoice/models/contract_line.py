from odoo import models


class ContractLine(models.Model):
    _inherit = "contract.line"

    def _check_last_date_invoiced(self):
        for rec in self.filtered("last_date_invoiced"):
            # Calling the validator multiple times is not the most optimal way
            # to do this, but this will allow us to skip just one of the constraints
            if rec.date_end and rec.date_end < rec.last_date_invoiced:
                # Skip this constraint
                continue

            # Check other constraints
            super()._check_last_date_invoiced()
