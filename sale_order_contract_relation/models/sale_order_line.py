from odoo import fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    contract_line_id = fields.Many2one(
        string="Contract line", comodel_name="contract.line", readonly=1, copy=False
    )
