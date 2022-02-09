from odoo import fields, models


class ContractLine(models.Model):
    _inherit = "contract.line"

    def _prepare_invoice_line(self, move_form):
        res = super()._prepare_invoice_line(move_form)

        if (
            self.product_id
            and self.contract_id.purchase_pricelist_id
            and res.get("purchase_price")
        ):
            price = res["purchase_price"]
            pricelist = self.contract_id.purchase_pricelist_id
            product = self.product_id
            uom = self.uom_id
            quantity = self.quantity
            partner = self.contract_id.partner_id

            rule = pricelist._compute_price_rule(
                [(product, quantity, partner)], fields.Date.context_today(self), uom.id
            )
            if rule.get(product.id):
                rule_id = rule[product.id][1]
                pricelist_item = self.env["product.pricelist.item"].browse([rule_id])

                res["purchase_price"] = pricelist_item._compute_price(
                    price, uom, product, quantity, partner
                )

        return res
