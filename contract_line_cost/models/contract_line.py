from odoo import api, fields, models


class ContractLine(models.Model):
    _inherit = "contract.line"

    purchase_price = fields.Float(
        string="Cost",
        compute="_compute_purchase_price",
        store=True,
        readonly=False,
        digits="Product Price",
    )

    def _get_purchase_price(self):
        # Override this method if you want to use a custom value as purchase price
        self.ensure_one()
        return self.product_id.standard_price

    @api.depends("product_id", "uom_id")
    def _compute_purchase_price(self):
        for line in self:
            purchase_price = line._get_purchase_price()

            if line.uom_id != line.product_id.uom_id:
                purchase_price = line.product_id.uom_id._compute_price(
                    purchase_price, line.uom_id
                )
            line.purchase_price = purchase_price

    def _prepare_invoice_line(self, move_form):
        res = super()._prepare_invoice_line(move_form)

        res["purchase_price"] = self.purchase_price

        return res
