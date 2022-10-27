from odoo import fields, models


class ContractContract(models.Model):
    _inherit = "contract.contract"

    comment = fields.Text(
        string="Comment", help="Comment for invoice. This will be sent to customer"
    )

    def _prepare_sale(self, date_ref):
        # Super will handle ensure_one() and other validation
        res = super()._prepare_sale(date_ref)

        # Add comment to writable values
        if self.comment:
            res["note"] = self.comment

        return res

    def _prepare_invoice(self, date_invoice):
        # Super will handle ensure_one() and other validation
        invoice_vals, move_form = super()._prepare_invoice(date_invoice)

        # Add comment to writable values
        if self.comment:
            invoice_vals["narration"] = self.comment

        return invoice_vals, move_form
