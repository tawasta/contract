from odoo import fields, models


class AccountAnalyticAccount(models.Model):

    _inherit = "account.analytic.account"

    products = fields.Many2one(
        "product.product",
        string="Product",
        related="recurring_invoice_line_ids.product_id",
    )
