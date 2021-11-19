from odoo import fields, models


class Contract(models.Model):
    _inherit = "contract.contract"

    purchase_pricelist_id = fields.Many2one(
        comodel_name="product.pricelist", string="Cost pricelist"
    )
