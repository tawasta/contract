from odoo import api, fields, models


class ContractLine(models.Model):

    _inherit = "contract.line"

    product_variant_company = fields.Many2one(
        string="Variant Company", comodel_name="res.company", compute="_compute_company"
    )

    @api.depends("product_id")
    def _compute_company(self):
        for line in self:
            if line.product_id.variant_company_id:
                line.product_variant_company = line.product_id.variant_company_id.id
