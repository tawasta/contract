# -*- coding: utf-8 -*-


from odoo import fields, models


class AccountAnalyticInvoiceLine(models.Model):

    _inherit = 'account.analytic.invoice.line'

    analytic_id_partner_shipping_id = fields.Many2one(
        comodel_name='res.partner',
        string='Partner',
        related='analytic_account_id.partner_shipping_id',
        store=True,
    )
