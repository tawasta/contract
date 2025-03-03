from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    subscription_price_prorate = fields.Boolean(
        "Subscription prorate",
        help="When purchasing new subscription, "
        "prorate price according to an existing subscription",
    )
