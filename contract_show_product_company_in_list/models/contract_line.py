from odoo import api, fields, models


class ContractLine(models.Model):

    _inherit = "contract.line"

    company = fields.Many2one(
        string="Company", comodel_name="res.company", compute="_compute_company"
    )

    @api.depends("product_id")
    def _compute_company(self):
        self.company = self.product_id.variant_company_id
