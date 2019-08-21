# -*- coding: utf-8 -*-


from odoo import fields, models


class AccountAnaluticContract(models.Model):

    _inherit = 'account.analytic.contract'

    partner_id_street_search = fields.Char(
        string='Street',
        related='partner_id.parent_id.street',
    )
