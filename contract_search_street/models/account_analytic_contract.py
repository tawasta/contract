# -*- coding: utf-8 -*-


from odoo import fields, models


class AccountAnaluticContract(models.Model):

    _inherit = 'account.analytic.contract'

    partner_id_street = fields.Char(
        string='Street',
        related='partner_id.street',
    )
