# -*- coding: utf-8 -*-
from odoo import api, models, fields


class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'

    reference = fields.Char(
        string='Order reference',
        copy=False,
        help="The partner order reference of this contract",
    )

    @api.multi
    def _prepare_sale(self):
        # Super will handle ensure_one() and other validation
        res = super(AccountAnalyticAccount, self)._prepare_sale()

        # Add reference to writable values
        if self.reference:
            res['reference'] = self.reference

        # Add code to writable values
        if self.code:
            res['name'] = self.code

        return res

    @api.multi
    def _prepare_invoice(self):
        # Super will handle ensure_one() and other validation
        res = super(AccountAnalyticAccount, self)._prepare_invoice()

        # Add reference to writable values
        if self.reference:
            res['reference'] = self.reference

        # Add code to writable values
        if self.code:
            res['name'] = self.code

        return res
