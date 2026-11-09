from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    show_partner_subscribable_products_in_progress_page = fields.Boolean(
        string="Show Subscribed Products on Contacts",
        help="Show a page listing the subscribable products of the contact's "
        "ongoing subscriptions on the contact form",
    )

    @api.model
    def get_values(self):
        res = super().get_values()
        res.update(
            show_partner_subscribable_products_in_progress_page=self.env[
                "ir.config_parameter"
            ]
            .sudo()
            .get_param(
                "partner_subscribable_products_currently_in_progress.show_partner_page",
                "True",
            )
            == "True"
        )
        return res

    def set_values(self):
        super().set_values()
        self.env["ir.config_parameter"].sudo().set_param(
            "partner_subscribable_products_currently_in_progress.show_partner_page",
            str(self.show_partner_subscribable_products_in_progress_page),
        )
        return True
