from odoo import _
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
        for subscription in self.search([("date", "<=", fields.Date.today())]):
            # Close subscriptions
            subscription._action_close_subscription()

        return res
