from odoo import fields, models


class ContractLineBetterContext(models.Model):

    _inherit = "contract.line"

    variant_company_id = fields.Many2one(
        comodel_name="res.company",
        string="Product variant company",
        related="product_id.variant_company_id",
        store=True,
    )
