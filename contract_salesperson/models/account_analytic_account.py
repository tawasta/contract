# -*- coding: utf-8 -*-
from odoo import api, models, fields


class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'

    @api.multi
    def _prepare_sale(self):
        # Super will handle ensure_one() and other validation
        res = super(AccountAnalyticAccount, self)._prepare_sale()

        # Add salesperson to writable values
        if self.user_id:
            res['user_id'] = self.user_id.id

        return res

    @api.multi
    def _prepare_invoice(self):
        # Super will handle ensure_one() and other validation
        res = super(AccountAnalyticAccount, self)._prepare_invoice()

        # Add salesperson to writable values
        if self.user_id:
            res['user_id'] = self.user_id.id

        return res
