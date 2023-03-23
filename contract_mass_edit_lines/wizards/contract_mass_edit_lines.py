import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class ContractMassEditLines(models.TransientModel):
    _name = "contract.mass.edit.lines"
    _description = "Mass edit contract lines"

    recurring_next_date = fields.Date("Date of next invoice")
    date_end = fields.Date("End Date")

    def action_mass_edit_lines(self):
        """Update Date of next invoice and End Date"""
        contract_ids = self.env["contract.contract"].browse(
            self._context.get("active_ids")
        )

        lines = contract_ids.mapped("contract_line_ids")
        active_lines = lines.filtered(
            lambda r: r.state not in ["closed", "canceled", "upcoming-close"]
        )

        values = {}

        if self.recurring_next_date:
            values["recurring_next_date"] = self.recurring_next_date

        values["date_end"] = self.date_end

        active_lines.write(values)
