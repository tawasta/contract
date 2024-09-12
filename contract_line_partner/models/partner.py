from odoo import api, fields, models


class Partner(models.Model):
    _inherit = "res.partner"

    contract_line_ids = fields.One2many(
        comodel_name="contract.line", inverse_name="partner_id", string="Contract lines"
    )
