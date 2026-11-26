from odoo import fields, models


class Website(models.Model):
    _inherit = "website"

    subscription_show_current_invoice_address = fields.Boolean(
        string="Show current invoice address",
        help="Mark the invoice address currently used by the subscription "
        "in the portal address selection.",
    )
    subscription_edit_invoice_address = fields.Boolean(
        string="Allow editing invoice addresses",
        help="Let portal users edit their existing invoice addresses in the "
        "subscription address selection, with the same restrictions as in "
        "the checkout.",
    )
