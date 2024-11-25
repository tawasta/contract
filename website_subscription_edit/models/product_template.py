from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    subscription_change_allowed = fields.Boolean(
        string="Change allowed",
        default=False,
        help="Allows changing subscription product to other variant",
    )
