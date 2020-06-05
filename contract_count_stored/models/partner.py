# -*- coding: utf-8 -*-
from odoo import models, fields


class Partner(models.Model):
    _inherit = 'res.partner'

    active_contract_ids = fields.One2many(
        comodel_name='account.analytic.account',
        inverse_name='partner_id',
        string='Contracts',
        domain=['|',
                ('date_end', '=', False),
                ('date_end', '>=', fields.Date.today())
                ],
    )
