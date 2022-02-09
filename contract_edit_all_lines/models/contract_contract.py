from odoo import api
from odoo import fields
from odoo import models


class Contract(models.Model):

    _inherit = "contract.contract"

    set_recurring_next_date = fields.Date(
        string="Set invoice date", help="Set next invoice date for all lines"
    )

    @api.onchange("set_recurring_next_date")
    def onchange_set_recurring_next_date(self):
        for record in self:
            if record.line_recurrence and record.set_recurring_next_date:
                record.contract_line_ids.write(
                    {"recurring_next_date": record.set_recurring_next_date}
                )
                # Set the helper field as empty to prevent misunderstandings
                record.set_recurring_next_date = False
