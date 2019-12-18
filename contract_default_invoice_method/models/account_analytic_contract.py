# -*- coding: utf-8 -*-


from odoo import fields, models


class AccountAnalyticContract(models.Model):

    _inherit = 'account.analytic.contract'

    customer_invoice_transmit_method_id = fields.Many2one(
        comodel_name='transmit.method',
        related='partner_id.customer_invoice_transmit_method_id',
    )
