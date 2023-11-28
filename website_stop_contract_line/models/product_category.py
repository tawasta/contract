from odoo import fields, models


class ProductCategory(models.Model):
    _inherit = "product.category"

    allow_cancel = fields.Boolean(
        string="Allow cancel",
        default=False,
    )
