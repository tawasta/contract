from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    has_subscriptions = fields.Boolean(compute="_compute_has_subscriptions")

    def _compute_has_subscriptions(self):
        if len(self.get_subscription_info()) > 0:
            self.has_subscriptions = True
        else:
            self.has_subscriptions = False

    def get_subscription_info(self):
        self.ensure_one()

        lines = self.env["sale.subscription.line"].search(
            [
                ("sale_subscription_id.partner_id", "=", self.id),
                ("sale_subscription_id.stage_id.type", "=", "in_progress"),
            ]
        )

        return [{"name": line.product_id.display_name} for line in lines]
