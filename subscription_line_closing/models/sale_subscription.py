from odoo import api
from odoo import fields
from odoo import models


class SaleSubscription(models.Model):
    _inherit = "sale.subscription"

    sale_subscription_closed_line_ids = fields.One2many(
        comodel_name="sale.subscription.line",
        inverse_name="sale_subscription_id",
        domain=[("active", "=", False)],
        context={"active_test": False},
    )

    def write(self, vals):
        res = super().write(vals)

        if "date" in vals:
            # Set end date to all subscription lines that haven't one
            for record in self:
                for line in record.sale_subscription_line_ids.filtered(
                    lambda r: not r.date_end
                ):
                    line.date_end = vals["date"]

        if "start_date" in vals:
            # Set start date to all subscription lines that haven't one
            for record in self:
                for line in record.sale_subscription_line_ids.filtered(
                    lambda r: not r.start_date
                ):
                    line.start_date = vals["start_date"]

        return res

    @api.depends("sale_subscription_line_ids")
    def _compute_total(self):
        res = super()._compute_total()

        for record in self:
            if False not in record.sale_subscription_line_ids.mapped("active"):
                # If there are archived lines, do a recompute
                continue

            recurring_total = amount_tax = 0.0
            for order_line in record.sale_subscription_line_ids.filtered("active"):
                recurring_total += order_line.price_subtotal
                amount_tax += order_line.amount_tax_line_amount
            record.update(
                {
                    "recurring_total": recurring_total,
                    "amount_tax": amount_tax,
                    "amount_total": recurring_total + amount_tax,
                }
            )

        return res
