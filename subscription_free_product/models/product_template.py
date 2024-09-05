from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    free_subscription_product_id = fields.Many2one(
        comodel_name="product.template",
        string="Free subscription",
        relation="related_free_product_rel",
    )
