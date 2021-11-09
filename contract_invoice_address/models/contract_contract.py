from odoo import fields, models


class Contract(models.Model):

    _inherit = "contract.contract"

    partner_invoice_id = fields.Many2one(
        comodel_name="res.partner", string="Invoice Address"
    )

    def _prepare_invoice(self, *args, **kwargs):
        # Super will handle ensure_one() and other validation
        invoice_vals, move_form = super()._prepare_invoice(*args, **kwargs)

        # Add shipping address to writable values
        if self.partner_invoice_id:
            invoice_vals["partner_id"] = self.partner_invoice_id.id

        return invoice_vals, move_form
