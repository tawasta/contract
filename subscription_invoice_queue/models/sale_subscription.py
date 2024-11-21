import logging
from datetime import date
from odoo import _
from odoo import models

_logger = logging.getLogger(__name__)


class SaleSubscription(models.Model):
    _inherit = "sale.subscription"

    def cron_subscription_management(self):
        # Overwrite function to allow using queue
        today = date.today()
        for subscription in self.search([]):
            job_desc = _(
                "Generate invoice for subscription '{}'".format(subscription.name)
            )

            if subscription.in_progress:
                if (
                    subscription.recurring_next_date == today
                    and subscription.sale_subscription_line_ids
                ):
                    try:
                        subscription.with_delay(description=job_desc).generate_invoice()
                    except Exception:
                        _logger.exception("Error on subscription invoice generate")
                if not subscription.recurring_rule_boundary:
                    if subscription.date == today:
                        subscription.action_close_subscription()

            else:
                if subscription.date_start == today:
                    subscription.action_start_subscription()
                    subscription.with_delay(description=job_desc).generate_invoice()
