from odoo import _, fields, models
from odoo.exceptions import ValidationError


class Contract(models.Model):
    _inherit = "contract.contract"

    set_recurring_next_date = fields.Date(
        string="New Date of Next Invoice", help="Set next invoice date for all lines"
    )

    def set_recurring_next_date_for_lines(self):
        """
        Iterate through all the contract lines and set their Date of Next Invoice
        according to user selection
        """

        self.ensure_one()

        if not self.set_recurring_next_date:
            raise ValidationError(_("Please select a date"))

        if not self.line_recurrence:
            raise ValidationError(
                _(
                    "'Recurrence at line level?' must be enabled to use this functionality"
                )
            )

        self.contract_line_ids.write(
            {"recurring_next_date": self.set_recurring_next_date}
        )
        # Set the helper field back to empty to prevent misunderstandings
        self.set_recurring_next_date = False
