from datetime import datetime

from odoo import _, fields, models


class SubscriptionLineChangeProductVariant(models.TransientModel):
    _name = "subscription.line.change.product.variant"

    old_product_id = fields.Many2one("product.product", string="Previous membership")
    product_id = fields.Many2one(
        "product.product",
        domain="[('id', 'in', available_variants)]",
        string="New membership",
    )
    sale_subscription_line = fields.Many2one("sale.subscription.line", readonly=True)
    sale_subscription_id = fields.Many2one("sale.subscription", readonly=True)
    available_variants = fields.Many2many("product.product")
    next_invoice_date_update = fields.Date("Next invoice date")

    def change_product_variant(
        self,
        sale_subscription_id=None,
        new_product_id=None,
        sale_subscription_line=None,
    ):
        """This function creates a new sale.subscription line and a new invoice with
        appropriate values based on a chosen product and the old sale.subscription
        line."""

        sale_subscription = sale_subscription_id or self.sale_subscription_id
        sale_subscription_line = sale_subscription_line or self.sale_subscription_line
        product = new_product_id or self.product_id
        old_product = sale_subscription_line and sale_subscription_line.product_id
        now_date = datetime.now()

        new_line_price = 0
        old_line_price = 0

        # Get price for a product
        if sale_subscription.pricelist_id:
            new_line_price = sale_subscription.pricelist_id._get_product_price(
                product=product,
                quantity=sale_subscription_line.product_uom_qty,
                partner=sale_subscription.partner_id.id,
                date=now_date,
            )

            old_line_price = sale_subscription.pricelist_id._get_product_price(
                product=old_product,
                quantity=sale_subscription_line.product_uom_qty,
                partner=sale_subscription.partner_id.id,
                date=now_date,
            )

        # Check the price difference and set the new price for invoice line
        # to zero, if the difference is negative
        new_line_price = new_line_price - old_line_price
        new_line_price = 0 if new_line_price < 0 else new_line_price

        sale_subscription_line.update(
            {
                "product_id": product.id,
                "price_unit": product.lst_price,
                "name": product.display_name,
                "sale_subscription_id": sale_subscription.id,
            }
        )

        # Create a new invoice with a new sale_subscription line information
        line_values = []

        account_move_line = sale_subscription_line._prepare_account_move_line()

        # Set invoice line's price as the difference between old sale.subscription
        # line's and new sale_subscription line's price based on sale.subscription's pricelist
        # rule.
        account_move_line["price_unit"] = new_line_price

        line_values.append((0, 0, account_move_line))
        invoice_vals = sale_subscription._prepare_account_move(line_values)

        invoice_id = (
            self.env["account.move"]
            .sudo()
            .with_context(default_move_type="out_invoice", journal_type="sale")
            .create(invoice_vals)
        )

        sale_subscription_modification_model = self.env[
            "sale.subscription.modification"
        ]

        description = "'{}'{}'{}'".format(
            old_product.display_name, " has been changed to ", product.display_name
        )

        log_vals = {
            "date": now_date,
            "description": description,
            "subscription_id": sale_subscription.id,
        }

        sale_subscription_modification_model.create(log_vals)

        sale_subscription.write({"invoice_ids": [(4, invoice_id.id)]})

        return invoice_id
