# -*- coding: utf-8 -*-
from odoo import api, models, fields


class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'

    comment = fields.Text(
        string='Comment',
        help='Comment for invoice. This will be sent to customer'
    )

    @api.multi
    def _prepare_sale(self):
        # Super will handle ensure_one() and other validation
        res = super(AccountAnalyticAccount, self)._prepare_sale()

        # Add comment to writable values
        if self.comment:
            res['comment'] = self.comment

        return res

    @api.multi
    def _prepare_invoice(self):
        # Super will handle ensure_one() and other validation
        res = super(AccountAnalyticAccount, self)._prepare_invoice()

        # Add comment to writable values
        if self.comment:
            res['comment'] = self.comment

        return res
