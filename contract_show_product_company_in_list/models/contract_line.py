from odoo import api, fields, models


class ContractLine(models.Model):

    _inherit = "contract.line"

    product_variant_company = fields.Many2one(
        string="Variant Company", comodel_name="res.company", compute="_compute_company"
    )

    @api.depends("product_id")
    def _compute_company(self):
        self.product_variant_company = self.product_id.variant_company_id
