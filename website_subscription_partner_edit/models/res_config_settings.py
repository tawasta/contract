from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    subscription_show_current_invoice_address = fields.Boolean(
        related="website_id.subscription_show_current_invoice_address",
        readonly=False,
    )
    subscription_edit_invoice_address = fields.Boolean(
        related="website_id.subscription_edit_invoice_address",
        readonly=False,
    )
