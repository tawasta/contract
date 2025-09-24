# -*- coding: utf-8 -*-
from odoo import api, fields, models


class SaleSubscription(models.Model):
    _inherit = "sale.subscription"

    unit_price = fields.Monetary(
        string="Unit Price",
        compute="_compute_unit_price",
        store=True,
        readonly=True,
        currency_field="currency_id",
        help="Sum of price_unit from all subscription lines (no quantities or taxes).",
    )

    @api.depends("sale_subscription_line_ids", "sale_subscription_line_ids.price_unit")
    def _compute_unit_price(self):
        for rec in self:
            total = 0.0
            for line in rec.sale_subscription_line_ids:
                # exact requirement: take price_unit from the line
                total += line.price_unit or 0.0
            rec.unit_price = total
