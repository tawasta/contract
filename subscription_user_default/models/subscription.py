from odoo import api, models, _
from odoo.exceptions import ValidationError


class SaleSubscription(models.Model):
    _inherit = "sale.subscription"

    @api.model_create_multi
    def create(self, vals_list):
        # Hae oletuskäyttäjän ID järjestelmäasetuksista
        default_user_id = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("sale_subscription.default_user_id")
        )

        if default_user_id:
            try:
                # Muuta default_user_id kokonaisluvuksi
                default_user_id = int(default_user_id)
            except ValueError:
                raise ValidationError(_("The default user ID is not a valid integer."))

            # Varmista, että käyttäjä on olemassa
            user = self.env["res.users"].sudo().browse(default_user_id)
            if not user.exists():
                raise ValidationError(
                    _("The user with ID %s does not exist.") % default_user_id
                )

            # Päivitä jokaisen `vals`-sanakirjan `user_id`
            for vals in vals_list:
                vals["user_id"] = default_user_id

        # Käytä core-logiikkaa kaikille muille käsittelyille
        return super(SaleSubscription, self).create(vals_list)
