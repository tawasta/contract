from odoo import api
from odoo import fields
from odoo import models


class SaleSubscription(models.Model):
    _inherit = "sale.subscription"

    def cron_subscription_management(self):
        res = super().cron_subscription_management()
        for subscription in self.search([("date", "<=", fields.Date.today())]):
            # Close subscriptions
            if subscription.in_progress:
                stage = subscription.stage_id
                closed_stage = self.env["sale.subscription.stage"].search(
                    [("type", "=", "post")], limit=1
                )
                print(stage)
                print(closed_stage)
                if stage != closed_stage:
                    subscription.stage_id = closed_stage
                    # self.active = False

        return res
