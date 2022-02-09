from dateutil.relativedelta import relativedelta
from odoo import api
from odoo import models


class ContractAbstractContractLine(models.AbstractModel):
    _inherit = "contract.abstract.contract.line"

    @api.depends("next_period_date_start")
    def _compute_recurring_next_date(self):
        for rec in self:
            if rec.last_date_invoiced and rec.recurring_next_date:
                rec.last_date_invoiced = rec.recurring_next_date + relativedelta(
                    days=-1
                )

        return super()._compute_recurring_next_date()
