# -*- coding: utf-8 -*-
from odoo import models, fields


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    agreement_identifier = fields.Char(
        string='Agreement identifier',
        size=70,
    )
