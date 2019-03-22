from odoo import api, models


class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'

    @api.multi
    def _prepare_sale(self):
        # Super will handle ensure_one() and other validation
        res = super(AccountAnalyticAccount, self)._prepare_sale()

        # Add invoice address id to writable values
        if self.partner_invoice_id:
            res['partner_invoice_id'] = self.partner_invoice_id.id

        return res
