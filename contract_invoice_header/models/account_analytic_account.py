# -*- coding: utf-8 -*-
from odoo import api, models, fields


class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'

    invoice_header = fields.Char(
        string='Invoice header',
    )

    @api.multi
    def _prepare_sale(self):
        # Super will handle ensure_one() and other validation
        res = super(AccountAnalyticAccount, self)._prepare_sale()

        # Add invoice_header to writable values
        if self.invoice_header:
            res['header_text'] = self.invoice_header

        return res

    @api.multi
    def _prepare_invoice(self):
        # Super will handle ensure_one() and other validation
        res = super(AccountAnalyticAccount, self)._prepare_invoice()

        # Add invoice_header to writable values
        if self.invoice_header:
            res['header_text'] = self.invoice_header

        return res
