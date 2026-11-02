from odoo import fields, models


class Product(models.Model):
    _inherit = "product.product"

    contract_ids = fields.Many2many(
        string="Contracts",
        comodel_name="contract.contract",
        compute="_compute_contract_ids",
    )
    contract_line_ids = fields.Many2many(
        string="Contract Lines",
        comodel_name="contract.line",
        compute="_compute_contract_ids",
    )

    def _compute_contract_ids(self):
        Line = self.env["contract.line"]
        domain = [("product_id", "in", self.ids)]
        by_product = Line.search(domain).grouped("product_id")
        for record in self:
            lines = by_product.get(record, Line)
            record.contract_line_ids = lines
            record.contract_ids = lines.contract_id
