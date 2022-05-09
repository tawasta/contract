from odoo import models


class ContractLine(models.Model):

    _inherit = "contract.line"

    def _prepare_value_for_stop(self, date_end, manual_renew_needed):
        res = super(ContractLine, self)._prepare_value_for_stop(
            date_end, manual_renew_needed
        )

        if manual_renew_needed and self.recurring_next_date > date_end:
            # We can't stop the contract without recurring next date,
            # if last invoice date is before end date
            res["date_end"] = self.last_date_invoiced

            # Set next invoice date to False - never create another invoice
            # after stopping the contract
            res["recurring_next_date"] = False

        return res
