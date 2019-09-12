# -*- coding: utf-8 -*-


from odoo import fields, models


class AccountAnalyticContract(models.Model):

    _inherit = 'account.analytic.contract'

    cancel_reason = fields.Char(
        string='Cancellation Reason',
        help='The reason for terminating the contract.',
    )
