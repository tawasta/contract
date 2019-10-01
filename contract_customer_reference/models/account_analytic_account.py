# -*- coding: utf-8 -*-
from odoo import api, models, fields


class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'

    customer_reference = fields.Char(
        string='Customer reference',
        copy=False,
        help="The customer reference of this contract",
    )

    order_reference = fields.Char(
        string='Order reference',
        copy=False,
        help="The order reference or order number of this contract",
    )

    @api.multi
    def _prepare_sale(self):
        # Super will handle ensure_one() and other validation
        res = super(AccountAnalyticAccount, self)._prepare_sale()

        # Add reference to writable values
        if self.order_reference:
            res['reference'] = self.order_reference
        else:
            res['reference'] = False

        # Add code to writable values
        if self.code:
            res['origin'] = self.code

        # Add customer reference to writable values
        if self.customer_reference:
            res['name'] = self.customer_reference

        return res

    @api.multi
    def _prepare_invoice(self):
        # Super will handle ensure_one() and other validation
        res = super(AccountAnalyticAccount, self)._prepare_invoice()

        # Add reference to writable values
        if self.order_reference:
            res['reference'] = self.order_reference

        # Add code to writable values
        if self.code:
            res['origin'] = self.code

        # Add customer reference to writable values
        if self.customer_reference:
            res['name'] = self.customer_reference

        return res
