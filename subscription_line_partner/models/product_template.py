from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    subscription_commercial = fields.Boolean(
        "Commercial subscription",
        help="Always link this product subscription line to commercial entity, if possible",
        default=False,
    )
