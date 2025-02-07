from datetime import timedelta

from odoo import api
from odoo import fields
from odoo import models
from odoo import _


class SaleSubscriptionLine(models.Model):
    _inherit = "sale.subscription.line"

    active = fields.Boolean(default=True)
    date_start = fields.Date("Start date", help="When subscription line will start")
    date_end = fields.Date("End date", help="When subscription line ended or will end")

    @api.model
    def create(self, vals):
        if not vals.get("date_start"):
            # Use today as default start date
            vals["date_start"] = fields.Date.today().isoformat()
        res = super().create(vals)

        return res

    def write(self, vals):
        if "date_start" in vals:
            date_start = vals.get("date_start")
            today = fields.Date.today()
            if isinstance(date_start, str):
                today = today.isoformat()

            if date_start and today < date_start:
                # Archive lines that haven't started yet
                vals["active"] = False
        res = super().write(vals)

        return res

    def action_stop(self, immediate=False):
        # Stop subscription lines
        today = fields.Date.today()
        for record in self:
            vals = {}
            date_end = record.date_end
            if not date_end and record.sale_subscription_id.recurring_next_date:
                date_end = record.sale_subscription_id.recurring_next_date - timedelta(
                    days=1
                )

                vals["date_end"] = date_end

            if immediate:
                # End immediately
                date_end = today

            if date_end and date_end <= today:
                # Line has ended, set it as inactive
                vals["active"] = False

            record.write(vals)

            msg = _("Stopped subscription line '%s'", record.name)
            subscription = record.sale_subscription_id

            subscription.modification_add(msg)
            subscription._compute_total()

    def action_start(self, immediate=True):
        # Start subscription lines

        for record in self:
            if immediate:
                date_start = fields.Date.today().isoformat()
            else:
                date_start = record.sale_subscription_id.recurring_next_date

            vals = {
                "active": True,
                "date_end": False,
            }

            if not record.date_start:
                # Add start date if there is no existing one
                vals["date_start"] = date_start

            record.write(vals)
            msg = _("Started subscription line '%s'", record.name)
            subscription = record.sale_subscription_id

            subscription.modification_add(msg)
            subscription._compute_total()

    def action_cron_stop(self):
        # Stop all ended lines
        records = self.search([("date_end", "<=", fields.Date.today())])
        for record in records:
            record.action_stop()

    def action_cron_start(self):
        # Open all started lines
        today = fields.Date.today()
        records = self.search(
            [
                ("active", "=", False),
                ("date_start", ">=", today),
                "|",
                ("date_end", "=", False),
                ("date_end", ">", today),
            ]
        )
        for record in records:
            record.action_start()
