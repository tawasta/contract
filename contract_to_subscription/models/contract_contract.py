from odoo import fields
from odoo import models
from odoo import _
from odoo.exceptions import ValidationError


class Contract(models.Model):
    _inherit = "contract.contract"

    subscription_id = fields.Many2one(
        comodel_name="sale.subscription",
        string="Related subscription",
        readonly=True,
        copy=False,
    )
    subscription_template_id = fields.Many2one(
        comodel_name="sale.subscription.template",
        string="Subscription template",
        help="Use this subscription template for creating a subscription",
    )

    def action_migrate_to_subscription(self):
        for record in self:
            record._migrate_to_subscription()

    def _migrate_to_subscription(self):
        self.ensure_one()

        if self.subscription_id:
            # Already linked to a subscription
            raise ValidationError(
                _("Already linked to subscription '%s'", self.subscription_id.name)
            )

        if not self.subscription_template_id:
            raise ValidationError(
                _("Please set a subscription template before creating a subscription")
            )

        sale_order = self.env["sale.order"]

        if hasattr(sale_order, "contract_id"):
            sale_order_id = sale_order.search(
                [("contract_id", "=", self.id)], limit=1
            ).id
        else:
            sale_order_id = False

        # Get the first stage
        stage_id = (
            self.env["sale.subscription.stage"]
            .search([], order="sequence ASC", limit=1)
            .id
        )

        # Create a new subscription with initial values
        subscription_values = {
            # Name and code could be overridden,
            # but it might be better to let subscription create it
            # "code": self.code,
            # "name": self.name,
            "company_id": self.company_id.id,
            "currency_id": self.currency_id.id,
            "date": self.date_end,
            "date_start": self.date_start,
            "description": self.note,
            "fiscal_position_id": self.fiscal_position_id.id,
            "in_progress": True,
            "journal_id": self.journal_id.id,
            "message_follower_ids": self.message_follower_ids,
            "partner_id": self.partner_id.id,
            "pricelist_id": self.pricelist_id.id,
            "recurring_next_date": self.recurring_next_date,
            "sale_order_id": sale_order_id,
            "stage_id": stage_id,
            # "tag_ids": TODO,
            "template_id": self.subscription_template_id.id,
            "user_id": self.user_id.id,
        }

        subscription_id = self.env["sale.subscription"].create(subscription_values)

        # Link existing invoices to subscription
        self._get_related_invoices().write({"subscription_id": subscription_id.id})

        # Link created subscription to contract
        self.subscription_id = subscription_id

        # Create subscription lines
        subscription_line = self.env["sale.subscription.line"]
        for line in self.contract_line_ids:
            line_values = {
                "company_id": line.company_id.id,
                "currency_id": line.currency_id.id,
                # "discount": line.discount,
                "name": line.name,
                "price_unit": line.price_unit,
                "product_id": line.product_id.id,
                "product_uom_qty": line.quantity,
                "sale_subscription_id": subscription_id.id,
                # "tax_ids": TODO
            }
            subscription_line.create(line_values)

        # Archive the contract
        self.active = False
