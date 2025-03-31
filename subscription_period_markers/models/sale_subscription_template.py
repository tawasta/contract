from odoo import models, fields


class SaleSubscriptionTemplate(models.Model):
    _inherit = "sale.subscription.template"

    auto_period_markers = fields.Boolean(
        string="Add period markers",
        help="Auto-add period markers to new subscription lines",
        default=False,
    )

    auto_period_markers_text = fields.Char(
        string="Period markers",
        help="Added automatically to subscription lines. "
        "You can use markers '#START#' and '#END#'",
        default="(#START# - #END#)",
    )
