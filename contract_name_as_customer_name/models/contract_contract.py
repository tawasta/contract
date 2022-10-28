from odoo import api, models


class ContractContract(models.Model):

    _inherit = "contract.contract"

    @api.onchange("partner_id")
    def contract_name_onchange(self):
        for record in self:
            record.name = record.partner_id.display_name
