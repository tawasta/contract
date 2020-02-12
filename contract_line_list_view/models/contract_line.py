from odoo import fields, models


class ContractLineBetterContext(models.Model):

    _inherit = "contract.line"

    partner_id = fields.Many2one(
        string="Member",
        comodel_name="res.partner",
        related="contract_id.partner_id",
        store=True,
    )
