from odoo import _
from odoo import fields
from odoo import models


class SaleSubscription(models.Model):
    _inherit = "sale.subscription"

    def _action_close_subscription(self):
        for record in self:
            if record.in_progress:
                stage = record.stage_id
                closed_stage = self.env["sale.subscription.stage"].search(
                    [("type", "=", "post")], limit=1
                )
                if stage != closed_stage:
                    values = {
                        "stage_id": closed_stage.id,
                        "date": fields.Date.today().isoformat(),
                        # Auto-archive
                        # "active": False
                    }
                    record.write(values)

                msg = _("Stopped subscription '%s'", record.name)
                record.modification_add(msg)

    def cron_subscription_management(self):
        res = super().cron_subscription_management()

        closed_stage = self.env["sale.subscription.stage"].search(
            [("type", "=", "post")], limit=1
        )

        subscriptions = self.search(
            [
                ("stage_id", "!=", closed_stage.id),
            ]
        )

        for subscription in subscriptions:
            subscription_ended = (
                subscription.date and subscription.date <= fields.Date.today()
            )
            if subscription_ended or not subscription.sale_subscription_line_ids:
                # Close ended subscriptions and subscriptions without active lines
                subscription._action_close_subscription()

        return res
