# -*- coding: utf-8 -*-
from odoo import models, fields


class Partner(models.Model):
    _inherit = 'res.partner'

    contract_count_stored = fields.Integer(
        string='Contract count',
        store=True,
        compute='_compute_contract_count_stored',
    )

    def _compute_contract_count_stored(self):
        for record in self:
            record.contract_count_stored = record.contract_count

    def cron_compute_contract_count_stored(self):
        self.search(
            [],
            order='write_date',
            limit=100,
        )._compute_contract_count_stored()
