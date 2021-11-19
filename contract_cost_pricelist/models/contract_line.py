from odoo import fields
from odoo import models


class ContractLine(models.Model):
    _inherit = "contract.line"

    def _get_purchase_price(self):
        res = super()._get_purchase_price()

        if self.product_id and self.contract_id.purchase_pricelist_id:
            pricelist = self.contract_id.purchase_pricelist_id
            product = self.product_id
            uom = self.uom_id
            quantity = self.quantity
            partner = self.contract_id.partner_id

            rule = pricelist._compute_price_rule(
                [(product, quantity, partner)],
                fields.Date.context_today(self),
                uom.id,
            )
            if rule.get(product.id):
                rule_id = rule[product.id][1]
                pricelist_item = self.env["product.pricelist.item"].browse([rule_id])

                res = pricelist_item._compute_price(
                    res, uom, product, quantity, partner
                )

        return res
