from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    force_split_subscription_lines = fields.Boolean(
        string="Split Subscription Lines by Quantity",
        help="If enabled, one subscription line will be created per unit ordered.",
    )
