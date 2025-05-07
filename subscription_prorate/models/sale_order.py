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

    def _cart_update_order_line(self, product_id, quantity, order_line, **kwargs):
        res = super()._cart_update_order_line(
            product_id, quantity, order_line, **kwargs
        )

        # Trigger a compute when updating cart
        res._compute_prorated_period()

        return res

    def _get_existing_subscription(self):
        partner = self.partner_id
        if not partner:
            partner = self.env.user.partner_id

        # Get an existing subscription for this partner
        subscription = (
            self.env["sale.subscription"]
            .sudo()
            .search(
                [
                    ("partner_id", "=", partner.id),
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

            if period < 0:
                # If next invoice date is in the past, period would be negative
                period = 0

            if period == 0:
                # Don't give 100% discount on 0 period
                discount = 0
            else:
                # Each elapsed month will give 8.33% discount
                discount = 100 / 12 * (12 - period)

            if discount < 0:
                # If the next invoice date is in the past, we'll get a negative discount
                discount = 0

        return discount, period, period_name
