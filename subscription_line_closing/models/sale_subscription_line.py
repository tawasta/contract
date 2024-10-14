from odoo import fields
from odoo import models
from odoo import _


class SaleSubscriptionLine(models.Model):
    _inherit = "sale.subscription.line"

    active = fields.Boolean(default=True)
    date_end = fields.Date("End date", help="When subscription line ended or will end")

    def action_stop(self):
        for record in self:
            record.write(
                {
                    "active": False,
                    "date_end": fields.Date.today(),
                }
            )
            msg = _("Stopped subscription line '%s'", record.name)
            subscription = record.sale_subscription_id

            subscription.modification_add(msg)
            subscription._compute_total()

    def action_start(self):
        for record in self:
            record.write(
                {
                    "active": True,
                    "date_end": False,
                }
            )
            msg = _("Started subscription line '%s'", record.name)
            subscription = record.sale_subscription_id

            subscription.modification_add(msg)
            subscription._compute_total()
