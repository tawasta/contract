
from odoo import api, models


class AccountAnalyticAccount(models.Model):

    _inherit = 'account.analytic.account'

    @api.onchange('partner_id', 'recurring_invoice_line_ids')
    def contract_name_onchange(self):
        lines = self.recurring_invoice_line_ids
        product_name = lines[0].product_id.name if lines else ""
        self.name = "%s%s%s" % (self.partner_id.display_name, ' - ' if
                                product_name else '', product_name)
