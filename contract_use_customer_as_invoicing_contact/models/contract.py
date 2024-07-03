from odoo import api, models


class ContractContract(models.Model):
    _inherit = "contract.contract"

    @api.onchange("partner_id")
    def _get_invoicing_contact_value(self):
        if self.partner_id:
            self.invoice_partner_id = self.partner_id
