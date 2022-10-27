from odoo import fields, models


class Contract(models.Model):

    _inherit = "contract.contract"

    partner_shipping_id = fields.Many2one(
        comodel_name="res.partner", string="Delivery Address"
    )

    def _prepare_sale(self, *args, **kwargs):
        # Super will handle ensure_one() and other validation
        res = super(Contract, self)._prepare_sale(*args, **kwargs)

        # Add shipping address id to writable values
        if self.partner_shipping_id:
            res["partner_shipping_id"] = self.partner_shipping_id.id

        return res

    def _prepare_invoice(self, *args, **kwargs):
        # Super will handle ensure_one() and other validation
        invoice_vals, move_form = super()._prepare_invoice(*args, **kwargs)

        # Add shipping address to writable values
        if self.partner_shipping_id:
            invoice_vals["partner_shipping_id"] = self.partner_shipping_id.id

        return invoice_vals, move_form
