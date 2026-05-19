from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    subscription_api_check_count_as_active = fields.Boolean(
        string="API Check: Count as Having an Active Subscription",
        default=False,
        help="When checked, an ongoing subscription line for this product makes the "
        "related partner be considered as having an active membership by the "
        "subscription-status check API.",
    )
