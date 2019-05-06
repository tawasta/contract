# -*- coding: utf-8 -*-


from odoo import fields, models


class AccountAnalyticContract(models.Model):

    _inherit = 'account.analytic.contract'

    partner_invoice_id_street = fields.Char(
        string='Street',
        related='partner_invoice_id.street',
    )

    partner_invoice_id_street2 = fields.Char(
        string='Street2',
        related='partner_invoice_id.street2',
    )

    partner_invoice_id_zip = fields.Char(
        string='Zip',
        related='partner_invoice_id.zip',
    )

    partner_invoice_id_city = fields.Char(
        string='City',
        related='partner_invoice_id.city',
    )
