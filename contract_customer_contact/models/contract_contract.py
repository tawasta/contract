from odoo import fields, models


class ContractContract(models.Model):

    _inherit = "contract.contract"

    partner_contact_id = fields.Many2one(
        comodel_name="res.partner",
        string="Contact person",
        domain=[("is_company", "=", False)],
    )

    def _prepare_sale(self, date_ref):
        # Super will handle ensure_one() and other validation
        res = super()._prepare_sale(date_ref)

        # Add customer_contact to writable values
        if self.partner_contact_id:
            res["customer_contact_id"] = self.partner_contact_id.id

        return res

    def _prepare_invoice(self, date_invoice):
        # Super will handle ensure_one() and other validation
        invoice_vals, move_form = super()._prepare_invoice(date_invoice)

        # Add customer contact to writable values
        if self.partner_contact_id:
            invoice_vals["customer_contact_id"] = self.partner_contact_id.id

        return invoice_vals, move_form
