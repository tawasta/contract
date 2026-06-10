from odoo import models


class ResPartner(models.Model):
    _inherit = "res.partner"

    # has_subscriptions = fields.Boolean(
    #     string="Has active subscriptions"
    #     compute="_compute_has_subscriptions"
    # )

    # def _compute_has_subscriptions(self):
    #     if len(self.get_subscription_info()) > 0:
    #         self.has_subscriptions = True
    #     else:
    #         self.has_subscriptions = False

    def get_subscription_info(self):
        """Subscription data for the membership report"""
        self.ensure_one()
        company = self.company_id or self.env.company

        # Get those subscriptions whose products have been configured to be listed
        # on the print
        lines = (
            self.env["sale.subscription.line"]
            .sudo()
            .search(
                [
                    ("sale_subscription_id.partner_id", "=", self.id),
                    ("sale_subscription_id.stage_id.type", "=", "in_progress"),
                    (
                        "product_id.product_tmpl_id",
                        "in",
                        company.member_certificate_shown_subscription_product_ids.ids,
                    ),
                ]
            )
        )
        return [{"name": line.product_id.display_name} for line in lines]

    def _can_print_member_certificate(self):
        """Whether the portal button is shown / printing is allowed for this
        partner. Override in other modules as needed."""
        self.ensure_one()

        ongoing_subscriptions = (
            self.env["sale.subscription.line"]
            .sudo()
            .search(
                [
                    ("sale_subscription_id.partner_id", "=", self.id),
                    ("sale_subscription_id.stage_id.type", "=", "in_progress"),
                ]
            )
        )

        company = self.company_id or self.env.company
        return bool(
            company.member_certificate_allow_portal_printing and ongoing_subscriptions
        )
