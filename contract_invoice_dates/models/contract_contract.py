from odoo import api, fields, models


class Contract(models.Model):

    _inherit = "contract.contract"

    recurring_next_date_synchronized = fields.Boolean(
        "Invoicing synchronized",
        help="The recurring next invoice dates for all active lines are in sync",
        compute="_compute_recurring_next_date_synchronized",
        store=True,
        copy=False,
    )

    @api.depends(
        "contract_line_ids.recurring_next_date",
        "contract_line_ids.is_canceled",
    )
    def _compute_recurring_next_date_synchronized(self):
        for record in self:
            next_dates = record.contract_line_ids.filtered(
                lambda line: (
                    line.recurring_next_date
                    and not line.is_canceled
                    and (not line.display_type or line.is_recurring_note)
                )
            ).mapped("recurring_next_date")

            if all(next_date == next_dates[0] for next_date in next_dates):
                in_sync = True
            else:
                in_sync = False

            record.recurring_next_date_synchronized = in_sync
