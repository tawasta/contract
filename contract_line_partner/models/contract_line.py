from odoo import fields, models


class ContractLine(models.Model):
    _inherit = "contract.line"

    partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Related partner",
    )
