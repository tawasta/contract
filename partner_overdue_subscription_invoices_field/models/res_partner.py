import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = "res.partner"

    has_overdue_subscription_invoices = fields.Boolean(
        string="Has Overdue Subscription Invoices?",
        compute="_compute_has_overdue_subscription_invoices",
        store=True,
        readonly=True,
        tracking=True,
        help="At least one posted subscription invoice for this partner is past "
        "its due date and not fully paid. Refreshed when invoices change and "
        "nightly by a scheduled action.",
    )

    @api.depends(
        "subscription_line_ids",
        "subscription_line_ids.sale_subscription_id",
        "subscription_line_ids.sale_subscription_id.invoice_ids",
        "subscription_line_ids.sale_subscription_id.invoice_ids.state",
        "subscription_line_ids.sale_subscription_id.invoice_ids.payment_state",
        "subscription_line_ids.sale_subscription_id.invoice_ids.invoice_date_due",
        "subscription_line_ids.sale_subscription_id.invoice_ids.amount_residual",
    )
    def _compute_has_overdue_subscription_invoices(self):
        overdue_ids = self._get_overdue_partner_ids(self)
        for partner in self:
            partner.has_overdue_subscription_invoices = partner.id in overdue_ids

    # ------------------------------------------------------------- internals

    @api.model
    def _get_overdue_move_domain(self):
        """Domain on account.move for finding overdue, still-unpaid invoices."""
        today = fields.Date.context_today(self)

        # payment_state values that count as "still owing money".
        unpaid_payment_states = ("not_paid", "partial")

        return [
            ("move_type", "=", "out_invoice"),
            ("state", "=", "posted"),
            ("payment_state", "in", unpaid_payment_states),
            ("amount_residual", ">", 0.0),
            ("invoice_date_due", "!=", False),
            ("invoice_date_due", "<", today),
        ]

    @api.model
    def _get_overdue_partner_ids(self, partners=None):
        """Get set of all partner ids with at least one overdue
        subscription-related invoice. The `any` operator requires a single invoice to
        satisfy every condition in domain.
        """
        domain = [
            ("sale_subscription_id.invoice_ids", "any", self._get_overdue_move_domain())
        ]
        if partners is not None:
            domain.append(("partner_id", "in", partners.ids))
        groups = (
            self.env["sale.subscription.line"]
            .sudo()
            ._read_group(domain, groupby=["partner_id"])
        )
        return {partner.id for (partner,) in groups if partner}

    # ------------------------------------------------------------------ cron

    @api.model
    def _cron_update_overdue_subscription_invoices(self):
        """Cron refresh — catches invoices that became overdue purely through
        the passage of time, which no @api.depends can detect."""
        candidates = self.sudo().search(
            [
                "|",
                ("has_overdue_subscription_invoices", "=", True),
                ("subscription_line_ids", "!=", False),
            ]
        )
        if not candidates:
            return
        field = self._fields["has_overdue_subscription_invoices"]

        self.env.add_to_compute(field, candidates)
        candidates.flush_recordset(["has_overdue_subscription_invoices"])

        _logger.info(
            "Refreshed has_overdue_subscription_invoices on %s partners",
            len(candidates),
        )
