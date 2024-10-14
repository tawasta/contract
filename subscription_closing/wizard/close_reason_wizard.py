from odoo import fields, models


class CloseSubscriptionWizard(models.TransientModel):
    _inherit = "close.reason.wizard"

    date_end = fields.Date(
        "End date", help="When the subscription will end", default=fields.Date.today()
    )

    def button_confirm(self):
        if self.date_end <= fields.Date.today():
            # End immediately
            super().button_confirm
        else:
            # Set the end date and reason
            sale_subscription = self.env["sale.subscription"].browse(
                self.env.context["active_id"]
            )
            values = {
                "recurring_rule_boundary": False,
                "close_reason_id": self.close_reason_id.id,
                "date": self.date_end,
            }
            sale_subscription.write(values)
