from odoo import models


class SaleSubscription(models.Model):
    _inherit = "sale.subscription"

    def _portal_can_edit_invoice_ref(self):
        """Whether the logged-in user may edit the customer reference in the
        portal: the subscription is billed to their own commercial entity or
        one of its addresses. The portal record rule also shows subscriptions
        to their followers, who must not change the reference."""
        self.ensure_one()
        commercial_partner = self.env.user.commercial_partner_id
        # An archived invoice address still belongs to the customer
        return bool(
            self.env["res.partner"]
            .with_context(active_test=False)
            .search_count(
                [
                    ("id", "=", self.partner_id.id),
                    ("id", "child_of", commercial_partner.id),
                ]
            )
        )
