from datetime import timedelta

from freezegun import freeze_time

from odoo import Command, fields
from odoo.tests import tagged

from odoo.addons.account.tests.common import AccountTestInvoicingCommon


@tagged("post_install", "-at_install")
class TestPartnerOverdueSubscriptionInvoices(AccountTestInvoicingCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.today = fields.Date.context_today(cls.env["res.partner"])
        cls.yesterday = cls.today - timedelta(days=1)
        cls.next_week = cls.today + timedelta(days=7)

        # subscription_oca gates which products may appear on subscription lines
        cls.product_a.subscribable = True

        cls.pricelist = cls.env["product.pricelist"].create(
            {
                "name": "Overdue test pricelist",
                "currency_id": cls.env.company.currency_id.id,
                "company_id": cls.env.company.id,
            }
        )
        cls.subscription_template = cls.env["sale.subscription.template"].create(
            {
                "name": "Overdue test template",
                "code": "OVERDUE_TEST",
                "product_ids": [Command.set(cls.product_a.ids)],
            }
        )
        cls.subscription_stage = cls.env["sale.subscription.stage"].create(
            {"name": "Overdue test stage"}
        )

    # ------------------------------------------------------------- factories

    def _create_subscription(self, partner, invoices=None):
        subscription = self.env["sale.subscription"].create(
            {
                "name": f"Subscription for {partner.name}",
                "company_id": self.env.company.id,
                "partner_id": partner.id,
                "template_id": self.subscription_template.id,
                "stage_id": self.subscription_stage.id,
                "pricelist_id": self.pricelist.id,
                "journal_id": self.company_data["default_journal_sale"].id,
                "date_start": self.today,
            }
        )
        if invoices:
            # Command.link, not Command.set: set() would unlink invoices from
            # any subscription they already belong to.
            subscription.invoice_ids = [Command.link(inv.id) for inv in invoices]
        return subscription

    def _create_line(self, subscription, partner):
        return self.env["sale.subscription.line"].create(
            {
                "company_id": self.env.company.id,
                "sale_subscription_id": subscription.id,
                "product_id": self.product_a.id,
                "partner_id": partner.id,
            }
        )

    def _create_invoice(self, due_date, post=True, move_type="out_invoice"):
        invoice = self.init_invoice(
            move_type,
            partner=self.partner_a,
            invoice_date=self.today,
            products=self.product_a,
            post=False,
        )
        # Clear the payment term so our explicit due date survives posting
        invoice.write({"invoice_payment_term_id": False, "invoice_date_due": due_date})
        if post:
            invoice.action_post()
        return invoice

    def _pay(self, invoice, amount=None):
        wizard = (
            self.env["account.payment.register"]
            .with_context(active_model="account.move", active_ids=invoice.ids)
            .create({})
        )
        if amount is not None:
            wizard.write({"amount": amount, "payment_difference_handling": "open"})
        wizard.action_create_payments()

    def _flag(self, partner):
        return partner.has_overdue_subscription_invoices

    # ------------------------------------------------------- basic selection

    def test_no_subscription_lines(self):
        self.assertFalse(self._flag(self.partner_a))

    def test_overdue_unpaid_invoice_flags_partner(self):
        invoice = self._create_invoice(self.yesterday)
        subscription = self._create_subscription(self.partner_a, invoice)
        self._create_line(subscription, self.partner_a)
        self.assertTrue(self._flag(self.partner_a))

    def test_invoice_not_yet_due_does_not_flag(self):
        invoice = self._create_invoice(self.next_week)
        subscription = self._create_subscription(self.partner_a, invoice)
        self._create_line(subscription, self.partner_a)
        self.assertFalse(self._flag(self.partner_a))

    def test_invoice_due_today_does_not_flag(self):
        """Boundary: the domain uses `< today`, so due-today is not yet late."""
        invoice = self._create_invoice(self.today)
        subscription = self._create_subscription(self.partner_a, invoice)
        self._create_line(subscription, self.partner_a)
        self.assertFalse(self._flag(self.partner_a))

    def test_draft_invoice_does_not_flag(self):
        invoice = self._create_invoice(self.yesterday, post=False)
        subscription = self._create_subscription(self.partner_a, invoice)
        self._create_line(subscription, self.partner_a)
        self.assertFalse(self._flag(self.partner_a))

    def test_credit_note_does_not_flag(self):
        refund = self._create_invoice(self.yesterday, move_type="out_refund")
        subscription = self._create_subscription(self.partner_a, refund)
        self._create_line(subscription, self.partner_a)
        self.assertFalse(self._flag(self.partner_a))

    def test_partially_paid_overdue_invoice_flags(self):
        invoice = self._create_invoice(self.yesterday)
        subscription = self._create_subscription(self.partner_a, invoice)
        self._create_line(subscription, self.partner_a)

        self._pay(invoice, amount=invoice.amount_total / 2.0)

        self.assertEqual(invoice.payment_state, "partial")
        self.assertTrue(self._flag(self.partner_a))

    def test_mixed_invoices_do_not_cross_match(self):
        """Regression: one paid-and-overdue invoice plus one unpaid-but-current
        invoice on the same subscription must NOT flag the partner.

        A single domain stacking state/payment_state/invoice_date_due on the
        to-many path would match here, because each condition is an independent
        subquery and can be satisfied by a different invoice. The `any` operator
        is what forces one invoice to satisfy all of them.
        """
        overdue_paid = self._create_invoice(self.yesterday)
        self._pay(overdue_paid)
        current_unpaid = self._create_invoice(self.next_week)

        subscription = self._create_subscription(
            self.partner_a, overdue_paid | current_unpaid
        )
        self._create_line(subscription, self.partner_a)

        self.assertIn(overdue_paid.payment_state, ("paid", "in_payment"))
        self.assertEqual(current_unpaid.payment_state, "not_paid")
        self.assertFalse(self._flag(self.partner_a))

    def test_all_line_partners_flagged_on_shared_subscription(self):
        """Intended behaviour: invoices hang off the subscription, so every
        line partner is flagged regardless of who the invoice is addressed to."""
        invoice = self._create_invoice(self.yesterday)
        subscription = self._create_subscription(self.partner_a, invoice)
        self._create_line(subscription, self.partner_a)
        self._create_line(subscription, self.partner_b)

        self.assertTrue(self._flag(self.partner_a))
        self.assertTrue(self._flag(self.partner_b))

    def test_healthy_subscription_does_not_mask_overdue_one(self):
        healthy = self._create_subscription(
            self.partner_a, self._create_invoice(self.next_week)
        )
        self._create_line(healthy, self.partner_a)
        self.assertFalse(self._flag(self.partner_a))

        overdue = self._create_subscription(
            self.partner_a, self._create_invoice(self.yesterday)
        )
        overdue_line = self._create_line(overdue, self.partner_a)
        self.assertTrue(self._flag(self.partner_a))

        overdue_line.unlink()
        self.assertFalse(self._flag(self.partner_a))

    # ------------------------------------------------------------ reactivity

    def test_flag_clears_when_invoice_is_paid(self):
        """Reactivity: no cron run, purely @api.depends on payment_state."""
        invoice = self._create_invoice(self.yesterday)
        subscription = self._create_subscription(self.partner_a, invoice)
        self._create_line(subscription, self.partner_a)
        self.assertTrue(self._flag(self.partner_a))

        self._pay(invoice)
        self.assertFalse(self._flag(self.partner_a))

    def test_flag_clears_when_invoice_reset_to_draft(self):
        invoice = self._create_invoice(self.yesterday)
        subscription = self._create_subscription(self.partner_a, invoice)
        self._create_line(subscription, self.partner_a)
        self.assertTrue(self._flag(self.partner_a))

        invoice.button_draft()
        self.assertFalse(self._flag(self.partner_a))

    def test_flag_reacts_to_due_date_change(self):
        """Explicit write on invoice_date_due triggers immediately. The cron is
        for the other case: the date staying put while today moves past it."""
        invoice = self._create_invoice(self.next_week)
        subscription = self._create_subscription(self.partner_a, invoice)
        self._create_line(subscription, self.partner_a)
        self.assertFalse(self._flag(self.partner_a))

        invoice.invoice_date_due = self.yesterday
        self.assertTrue(self._flag(self.partner_a))

    def test_flag_set_when_line_is_added_to_overdue_subscription(self):
        invoice = self._create_invoice(self.yesterday)
        subscription = self._create_subscription(self.partner_a, invoice)
        self.assertFalse(self._flag(self.partner_b))

        self._create_line(subscription, self.partner_b)
        self.assertTrue(self._flag(self.partner_b))

    def test_flag_clears_when_line_removed(self):
        invoice = self._create_invoice(self.yesterday)
        subscription = self._create_subscription(self.partner_a, invoice)
        line = self._create_line(subscription, self.partner_a)
        self.assertTrue(self._flag(self.partner_a))

        line.unlink()
        self.assertFalse(self._flag(self.partner_a))

    def test_flag_clears_when_invoice_detached_from_subscription(self):
        """Guards the bare `...sale_subscription_id.invoice_ids` depends entry:
        membership changes without any listed subfield changing."""
        invoice = self._create_invoice(self.yesterday)
        subscription = self._create_subscription(self.partner_a, invoice)
        self._create_line(subscription, self.partner_a)
        self.assertTrue(self._flag(self.partner_a))

        invoice.subscription_id = False
        self.assertFalse(self._flag(self.partner_a))

    # ------------------------------------------------------------------ cron

    def test_cron_catches_invoice_that_became_overdue(self):
        """The passage of time is not a dependency — only the cron sees it."""
        invoice = self._create_invoice(self.next_week)
        subscription = self._create_subscription(self.partner_a, invoice)
        self._create_line(subscription, self.partner_a)
        self.assertFalse(self._flag(self.partner_a))

        with freeze_time(self.next_week + timedelta(days=1)):
            self.env["res.partner"]._cron_update_overdue_subscription_invoices()
            self.assertTrue(self._flag(self.partner_a))

    def test_cron_clears_stale_flag(self):
        """The cron's clearing branch, exercised properly.

        Written via SQL deliberately: any ORM route to a stale flag would fire
        @api.depends and clear it before the cron ever runs. This also covers
        the `has_overdue_subscription_invoices = True` branch of the cron's
        candidate domain, since partner_b has no subscription lines at all.
        """
        self.env.cr.execute(
            "UPDATE res_partner SET has_overdue_subscription_invoices = TRUE "
            "WHERE id = %s",
            (self.partner_b.id,),
        )
        self.env["res.partner"].invalidate_model(["has_overdue_subscription_invoices"])
        self.assertTrue(self._flag(self.partner_b))

        self.env["res.partner"]._cron_update_overdue_subscription_invoices()
        self.assertFalse(self._flag(self.partner_b))

    # ----------------------------------------------------------- integration

    def test_subscription_generated_invoice_flags_partner(self):
        """Integration: drive subscription_oca's own invoicing path instead of
        linking invoice_ids by hand.

        Every other test in this class asserts our compute given an assumed
        invoice->subscription link. This one asserts the link itself, so if
        subscription_oca changes how generated invoices attach, it fails here
        rather than silently making the field always False in production.
        """
        subscription = self._create_subscription(self.partner_a)
        self._create_line(subscription, self.partner_a)

        invoice = subscription.create_invoice()

        self.assertTrue(invoice, "create_invoice() produced no move")
        self.assertEqual(invoice.move_type, "out_invoice")
        self.assertIn(
            invoice,
            subscription.invoice_ids,
            "Generated invoice is not linked back through invoice_ids — the "
            "traversal in _get_overdue_partner_ids relies on this",
        )
        self.assertGreater(
            invoice.amount_total,
            0.0,
            "Zero-amount invoice would pass amount_residual > 0 vacuously",
        )

        invoice.write(
            {"invoice_payment_term_id": False, "invoice_date_due": self.yesterday}
        )
        invoice.action_post()
        self.assertTrue(self._flag(self.partner_a))

        self._pay(invoice)
        self.assertFalse(self._flag(self.partner_a))
