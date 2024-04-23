from odoo import fields, models


class ContractLine(models.Model):
    _inherit = "contract.line"

    partner_invoice_id = fields.Many2one(
        comodel_name="res.partner",
        string="Invoice Address",
        related="contract_id.partner_invoice_id",
        readonly=True,
    )
