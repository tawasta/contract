from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    allow_subscription_invites = fields.Boolean(
        string="Allow Subscription Invitations",
        default=False,
        help="If unchecked, users cannot send invitations related to this product.",
    )
