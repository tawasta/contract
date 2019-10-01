# -*- coding: utf-8 -*-
from odoo import api, models, fields


class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'

    description = fields.Text(
        string='Description',
        help='Internal notes'
    )

    @api.multi
    def _prepare_sale(self):
        # Super will handle ensure_one() and other validation
        res = super(AccountAnalyticAccount, self)._prepare_sale()

        # Add description to writable values
        if self.description:
            res['description'] = self.description

        return res

    @api.multi
    def _prepare_invoice(self):
        # Super will handle ensure_one() and other validation
        res = super(AccountAnalyticAccount, self)._prepare_invoice()

        # Add description to writable values
        if self.description:
            res['description'] = self.description

        return res
