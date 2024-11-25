from odoo import api, fields, models


class SubscriptionLine(models.Model):
    _inherit = "sale.subscription.line"

    partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Related partner",
    )

    upgrade_allowed = fields.Boolean(
        string="Upgrade Allowed",
        compute="_compute_upgrade_allowed",
        compute_sudo=True,
    )

    def _compute_upgrade_allowed(self):
        for line in self:
            base_condition = line.active or not line.date_end
            change_condition = (
                line.product_id.product_tmpl_id.subscription_change_allowed
            )
            line.upgrade_allowed = base_condition and change_condition
