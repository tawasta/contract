from odoo import api, fields, models


class SaleSubscriptionLine(models.Model):
    _inherit = "sale.subscription.line"

    def change_product_variant(
        self,
        sale_subscription_id=None,
        new_product_id=None,
        sale_subscription_line=None,
    ):
        """This function is callable inside other models."""
        if sale_subscription_id and new_product_id and sale_subscription_line:
            self.env["subscription.line.change.product.variant"].change_product_variant(
                sale_subscription_id=sale_subscription_id,
                new_product_id=new_product_id,
                sale_subscription_line=sale_subscription_line,
            )
        return True

    def change_product_variant_wizard(self):
        product = self.product_id
        sale_subscription_line = self.id
        sale_subscription_id = self.sale_subscription_id.id
        available_variants = (
            self.env["product.template"]
            .sudo()
            .search([("id", "=", product.product_tmpl_id.id)])
            .mapped("product_variant_ids")
        )
        view_id = self.env.ref(
            "subscription_line_change_product_variant."
            "subscription_line_change_product_variant_wizard"
        ).id
        wiz = (
            self.env["subscription.line.change.product.variant"]
            .sudo()
            .create(
                {
                    "old_product_id": product.id,
                    "product_id": product.id,
                    "sale_subscription_line": sale_subscription_line,
                    "sale_subscription_id": sale_subscription_id,
                    "available_variants": available_variants,
                }
            )
        )

        return {
            "name": "Change member product",
            "view_mode": "form",
            "res_model": "subscription.line.change.product.variant",
            "view_id": view_id,
            "type": "ir.actions.act_window",
            "res_id": wiz.id,
            "target": "new",
        }
