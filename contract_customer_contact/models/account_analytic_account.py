from odoo import api, models


class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'

    @api.multi
    def _prepare_sale(self):
        # Super will handle ensure_one() and other validation
        res = super(AccountAnalyticAccount, self)._prepare_sale()

        # Add customer_contact to writable values
        if self.partner_contact_id:
            res['customer_contact'] = self.partner_contact_id.id

        return res

    @api.multi
    def _prepare_invoice(self):
        # Super will handle ensure_one() and other validation
        res = super(AccountAnalyticAccount, self)._prepare_invoice()

        # Add customer contact to writable values
        if self.partner_contact_id:
            res['customer_contact'] = self.partner_contact_id.id

        return res
