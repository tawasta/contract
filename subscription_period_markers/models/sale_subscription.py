from odoo import models, fields


class SaleSubscription(models.Model):
    _inherit = "sale.subscription"

    recurring_invoicing_type = fields.Selection(
        [("pre-paid", "Pre-paid"), ("post-paid", "Post-paid")],
        default="pre-paid",
        string="Invoicing type",
        help=(
            "Specify if the invoice must be generated at the beginning "
            "(pre-paid) or end (post-paid) of the period."
        ),
    )
