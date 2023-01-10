from odoo import fields, models


class AccountMove(models.Model):

    _inherit = "account.move"

    contract_id_origin = fields.Many2one(
        "contract.contract",
        related="line_ids.contract_line_id.contract_id",
        string="Contract",
    )
