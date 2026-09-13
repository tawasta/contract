from odoo import Command, fields
from odoo.tests import tagged

from odoo.addons.account.tests.common import AccountTestInvoicingCommon


@tagged("post_install", "-at_install")
class TestPartnerSubscribableProductsInProgress(AccountTestInvoicingCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.today = fields.Date.context_today(cls.env["res.partner"])

        # subscription_oca gates which products may appear on subscription lines
        cls.product_a.subscribable = True
        cls.product_b.subscribable = True

        cls.pricelist = cls.env["product.pricelist"].create(
            {
                "name": "In progress test pricelist",
                "currency_id": cls.env.company.currency_id.id,
                "company_id": cls.env.company.id,
            }
        )
        cls.subscription_template = cls.env["sale.subscription.template"].create(
            {
                "name": "In progress test template",
                "code": "IN_PROGRESS_TEST",
                "product_ids": [Command.set((cls.product_a | cls.product_b).ids)],
            }
        )
        cls.stage_pre = cls.env.ref("subscription_oca.subscription_stage_draft")
        cls.stage_in_progress = cls.env.ref(
            "subscription_oca.subscription_stage_in_progress"
        )
        cls.stage_closed = cls.env.ref("subscription_oca.subscription_stage_closed")

    # ------------------------------------------------------------- factories

    def _create_subscription(self, partner, in_progress=True):
        subscription = self.env["sale.subscription"].create(
            {
                "name": f"Subscription for {partner.name}",
                "company_id": self.env.company.id,
                "partner_id": partner.id,
                "template_id": self.subscription_template.id,
                "stage_id": self.stage_pre.id,
                "pricelist_id": self.pricelist.id,
                "journal_id": self.company_data["default_journal_sale"].id,
                "date_start": self.today,
            }
        )
        if in_progress:
            # write() is what syncs the in_progress flag from the stage type
            subscription.write({"stage_id": self.stage_in_progress.id})
        return subscription

    def _create_line(self, subscription, partner, product=None):
        return self.env["sale.subscription.line"].create(
            {
                "company_id": self.env.company.id,
                "sale_subscription_id": subscription.id,
                "product_id": (product or self.product_a).id,
                "partner_id": partner.id,
            }
        )

    def _products(self, partner):
        return partner.subscribable_product_ids_in_progress

    # ------------------------------------------------------- basic selection

    def test_no_subscription_lines(self):
        self.assertFalse(self._products(self.partner_a))

    def test_line_on_in_progress_subscription(self):
        subscription = self._create_subscription(self.partner_a)
        self._create_line(subscription, self.partner_a)
        self.assertEqual(self._products(self.partner_a), self.product_a)

    def test_line_on_not_started_subscription(self):
        subscription = self._create_subscription(self.partner_a, in_progress=False)
        self._create_line(subscription, self.partner_a)
        self.assertFalse(self._products(self.partner_a))

    def test_duplicate_products_listed_once(self):
        subscription = self._create_subscription(self.partner_a)
        line = self._create_line(subscription, self.partner_a)
        other = self._create_subscription(self.partner_a)
        self._create_line(other, self.partner_a)
        self.assertEqual(self._products(self.partner_a), self.product_a)

        line.unlink()
        self.assertEqual(self._products(self.partner_a), self.product_a)

    def test_shared_subscription_uses_line_partner(self):
        subscription = self._create_subscription(self.partner_a)
        self._create_line(subscription, self.partner_a, self.product_a)
        self._create_line(subscription, self.partner_b, self.product_b)
        self.assertEqual(self._products(self.partner_a), self.product_a)
        self.assertEqual(self._products(self.partner_b), self.product_b)

    # ------------------------------------------------------------ reactivity

    def test_stage_changes(self):
        subscription = self._create_subscription(self.partner_a, in_progress=False)
        self._create_line(subscription, self.partner_a)
        self.assertFalse(self._products(self.partner_a))

        subscription.write({"stage_id": self.stage_in_progress.id})
        self.assertEqual(self._products(self.partner_a), self.product_a)

        subscription.write({"stage_id": self.stage_closed.id})
        self.assertFalse(self._products(self.partner_a))

        subscription.write({"stage_id": self.stage_in_progress.id})
        self.assertEqual(self._products(self.partner_a), self.product_a)

    def test_line_product_change(self):
        subscription = self._create_subscription(self.partner_a)
        line = self._create_line(subscription, self.partner_a)
        line.product_id = self.product_b
        self.assertEqual(self._products(self.partner_a), self.product_b)

    def test_line_unlink(self):
        subscription = self._create_subscription(self.partner_a)
        line = self._create_line(subscription, self.partner_a)
        self.assertTrue(self._products(self.partner_a))
        line.unlink()
        self.assertFalse(self._products(self.partner_a))

    def test_line_partner_change(self):
        subscription = self._create_subscription(self.partner_a)
        line = self._create_line(subscription, self.partner_a)
        line.partner_id = self.partner_b
        self.assertFalse(self._products(self.partner_a))
        self.assertEqual(self._products(self.partner_b), self.product_a)

    def test_line_moved_to_another_subscription(self):
        not_started = self._create_subscription(self.partner_a, in_progress=False)
        ongoing = self._create_subscription(self.partner_a)
        line = self._create_line(not_started, self.partner_a)
        self.assertFalse(self._products(self.partner_a))
        line.sale_subscription_id = ongoing
        self.assertEqual(self._products(self.partner_a), self.product_a)

    # --------------------------------------------------------------- actions

    def test_action_view_subscription_lines(self):
        action = self.partner_a.action_view_subscription_lines_in_progress()
        self.assertEqual(action["res_model"], "sale.subscription.line")
        self.assertEqual(action["domain"], [("partner_id", "=", self.partner_a.id)])

    # -------------------------------------------------------------- settings

    def test_settings_round_trip(self):
        Settings = self.env["res.config.settings"].sudo()
        self.assertTrue(
            Settings.create({}).show_partner_subscribable_products_in_progress_page
        )
        self.assertTrue(self.partner_a.show_subscribable_products_in_progress_page)

        Settings.create(
            {"show_partner_subscribable_products_in_progress_page": False}
        ).set_values()
        self.assertEqual(
            self.env["ir.config_parameter"]
            .sudo()
            .get_param(
                "partner_subscribable_products_currently_in_progress.show_partner_page"
            ),
            "False",
        )
        self.assertFalse(
            Settings.create({}).show_partner_subscribable_products_in_progress_page
        )
        self.partner_a.invalidate_recordset(
            ["show_subscribable_products_in_progress_page"]
        )
        self.assertFalse(self.partner_a.show_subscribable_products_in_progress_page)

        Settings.create(
            {"show_partner_subscribable_products_in_progress_page": True}
        ).set_values()
        self.partner_a.invalidate_recordset(
            ["show_subscribable_products_in_progress_page"]
        )
        self.assertTrue(self.partner_a.show_subscribable_products_in_progress_page)
