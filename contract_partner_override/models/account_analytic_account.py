# -*- coding: utf-8 -*-
from odoo import api, models, fields


class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'

    @api.multi
    def _prepare_sale(self):
        # Super will handle ensure_one() and other validation
        res = super(AccountAnalyticAccount, self)._prepare_sale()

        # Add partner_id to writable values
        if self.partner_id:
            res['partner_id'] = self.partner_id.id

        return res

    @api.multi
    def _prepare_invoice(self):
        # Super will handle ensure_one() and other validation
        res = super(AccountAnalyticAccount, self)._prepare_invoice()

        # Add partner_id to writable values
        if self.partner_id:
            res['partner_id'] = self.partner_id.id

        return res
