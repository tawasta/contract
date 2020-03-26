# -*- coding: utf-8 -*-
from odoo import api, models, fields


class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'

    agreement_identifier = fields.Char(
        string='Agreement identifier',
        size=70,
    )

    @api.multi
    def _prepare_sale(self):
        # Super will handle ensure_one() and other validation
        res = super(AccountAnalyticAccount, self)._prepare_sale()

        # Add agreement_identifier to writable values
        if self.agreement_identifier:
            res['agreement_identifier'] = self.agreement_identifier

        return res

    @api.multi
    def _prepare_invoice(self):
        # Super will handle ensure_one() and other validation
        res = super(AccountAnalyticAccount, self)._prepare_invoice()

        # Add agreement_identifier to writable values
        if self.agreement_identifier:
            res['agreement_identifier'] = self.agreement_identifier

        return res
