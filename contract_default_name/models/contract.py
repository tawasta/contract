from odoo import api, models


class ContractContract(models.Model):
    _inherit = "contract.contract"

    @api.onchange("partner_id")
    def _onchange_partner_id(self):
        if self.partner_id:
            if self.partner_id.firstname and self.partner_id.lastname:
                self.name = self.partner_id.lastname + " " + self.partner_id.firstname
            else:
                self.name = self.partner_id.name
