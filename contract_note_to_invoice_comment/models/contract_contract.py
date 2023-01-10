from odoo import models


class ContractContract(models.Model):

    _inherit = "contract.contract"

    def _prepare_invoice(self, *args, **kwargs):
        invoice_vals, move_form = super()._prepare_invoice(*args, **kwargs)
        comment = invoice_vals.get("comment", "")
        if self.note:
            invoice_vals["narration"] = "{}{}{}".format(
                self.note, "\n" if comment else "", comment
            )
        return invoice_vals, move_form
