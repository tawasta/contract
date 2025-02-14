import logging
import math

from odoo import _, fields, models

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _calculate_last_date_invoiced(self):
        last_date_invoiced = self._get_existing_membership_last_date_invoiced()
        if last_date_invoiced:
            res = last_date_invoiced
        else:
            res = super()._calculate_last_date_invoiced()

        return res

    def _get_existing_subscription(self):
        self.ensure_one()

        # Get an existing subscription for this partner
        subscription = (
            self.env["sale.subscription"]
            .sudo()
            .search(
                [
                    ("partner_id", "=", self.partner_id.id),
                ],
                order="recurring_next_date",
                limit=1,
            )
        )

        return subscription

    def _get_existing_subscription_next_invoice_date(self):
        self.ensure_one()

        existing_subscription = self._get_existing_subscription()
        next_date = existing_subscription.recurring_next_date

        return next_date

    def _get_subscription_prorate_info(self):
        self.ensure_one()

        next_date = self._get_existing_subscription_next_invoice_date()
        date_today = fields.Date().today()

        if not next_date:
            next_date = date_today

        # TODO: configurable method (days, month)
        prorate_method = "month"
        # TODO: configurable rounding (floor, round, ceil)
        prorate_rounding = "ceil"

        days_difference = next_date - date_today
        days = days_difference.days
        if days > 0 and prorate_method == "month":
            # If the next invoice date is the same day as today,
            # count it as the same month
            days -= 1

        discount = 0

        if prorate_method == "month":
            period_name = _("months")
            period = days / 30

            if prorate_rounding == "ceil":
                period = math.ceil(period)

            if period > 11:
                # Pre-invoicing over 11 months is not supported
                period = 0

            discount = 100 / 12 * period
            if discount < 0:
                # If the next invoice date is in the past, we'll get a negative discount
                discount = 0

        return discount, period, period_name
