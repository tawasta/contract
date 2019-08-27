# -*- coding: utf-8 -*-


from odoo import api, models


class AccountAnalyticAccount(models.Model):

    _inherit = 'account.analytic.account'

    @api.onchange('partner_id')
    def contract_name_onchange(self):
        for record in self:
            record.name = record.partner_id.display_name
