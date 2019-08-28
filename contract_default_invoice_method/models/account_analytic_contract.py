# -*- coding: utf-8 -*-


from odoo import fields, models


class AccountAnalyticContract(models.Model):

    _inherit = 'account.analytic.contract'

    customer_invoice_transmit_method_id = fields.Char(
            string='Customer Invoice Transmission Method',
            related='partner_id.customer_invoice_transmit_method_id.name',
    )
