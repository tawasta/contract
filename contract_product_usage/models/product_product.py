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
        for record in self:
            contract_line_ids = self.env["contract.line"].search(
                [("product_id", "=", record.id)]
            )
            contract_ids = contract_line_ids.mapped("contract_id")

            record.contract_ids = contract_ids
            record.contract_line_ids = contract_line_ids
