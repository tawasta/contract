from odoo import fields, models


class Contract(models.Model):

    _inherit = "contract.contract"

    header_text = fields.Char(string="Header", help="Header or title of the Invoice")

    def _prepare_invoice(self, *args, **kwargs):
        # Super will handle ensure_one() and other validation
        invoice_vals, move_form = super()._prepare_invoice(*args, **kwargs)

        # Add header to writable values
        if self.header_text:
            invoice_vals["header_text"] = self.header_text

        return invoice_vals, move_form
