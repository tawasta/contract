from odoo import api
from odoo import fields
from odoo import models


class SaleSubscription(models.Model):
    _inherit = "sale.subscription"

    def action_close_subscription(self):
        res = super().action_close_subscription()

        stage = self.stage_id
        closed_stage = self.env["sale.subscription.stage"].search(
            [("type", "=", "post")], limit=1
        )
        if stage != closed_stage:
            self.stage_id = closed_stage
            self.active = False

        return res
