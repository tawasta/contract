from odoo import api, fields, models
import logging

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def create_subscription(self, lines, subscription_tmpl):
        results = super().create_subscription(lines, subscription_tmpl)

        # Find a subscription object
        subscription = self.subscription_ids and self.subscription_ids[0] or False

        if not subscription:
            return results

        for line in self.order_line:
            if line.product_id.free_subscription_product_id:
                # Create a free subscription line
                free_subscription_line = self._prepare_free_subscription_line(
                    line, subscription
                )
                if free_subscription_line:
                    self.env["sale.subscription.line"].create(free_subscription_line)

        # Palautetaan tulos
        return results

    def _prepare_free_subscription_line(self, line, subscription):
        """Valmistellaan yrityksen subscription-rivi"""

        # Tarkistetaan, onko ilmaisia tuotteita ja sama varianttiyhtiö
        free_product = False
        free_subscription_product = (
            line.product_id.product_tmpl_id.free_subscription_product_id
        )
        if free_subscription_product:
            possible_variants = free_subscription_product.product_variant_ids.filtered(
                lambda p: p.variant_company_id == line.product_id.variant_company_id
            )
            # TODO: how to decide from multiple found variants?
            if possible_variants:
                free_product = possible_variants[0]

        if not free_product:
            # Free product was not found
            return

        # Haetaan tuotteen verot ja mahdolliset alennukset core-logiikan mukaisesti
        fpos = (
            subscription.fiscal_position_id
            or subscription.partner_id.property_account_position_id
        )
        taxes = free_product.taxes_id.filtered(
            lambda tax: tax.company_id == subscription.company_id
        )
        taxes = fpos.map_tax(taxes) if fpos else taxes

        if line.product_id.subscription_commercial:
            partner = self.partner_id.commercial_partner_id
        else:
            partner = self.partner_id

        return {
            "sale_subscription_id": subscription.id,
            "product_id": free_product.id,
            "name": free_product.name,
            "price_unit": free_product.lst_price,
            "product_uom_qty": 1.0,
            "tax_ids": [(6, 0, taxes.ids)],
            "currency_id": self.currency_id.id,
            "partner_id": partner.id,
        }
