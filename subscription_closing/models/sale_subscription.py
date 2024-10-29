from odoo import api
from odoo import fields
from odoo import models


class SaleSubscription(models.Model):
    _inherit = "sale.subscription"

    def write(self, vals):
        res = super().write(vals)

        if "date" in vals and hasattr(self.env["sale.subscription.line"], "date_end"):
            # Set end date to all subscription lines that haven't ended already
            for record in self:
                record.sale_subscription_line_ids.write(
                    {
                        "date_end": vals["date"],
                        "active": False,
                    }
                )

        return res

    def cron_subscription_management(self):
        res = super().cron_subscription_management()
        for subscription in self.search([("date", "<=", fields.Date.today())]):
            # Close subscriptions
            if subscription.in_progress:
                stage = subscription.stage_id
                closed_stage = self.env["sale.subscription.stage"].search(
                    [("type", "=", "post")], limit=1
                )
                if stage != closed_stage:
                    subscription.stage_id = closed_stage
                    # Auto-archive
                    # self.active = False

        return res
