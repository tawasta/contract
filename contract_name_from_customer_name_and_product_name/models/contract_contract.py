
from odoo import api, models


class ContractContract(models.Model):

    _inherit = 'contract.contract'

    @api.onchange('partner_id', 'contract_line_ids')
    def contract_name_onchange(self):
        lines = self.contract_line_ids
        product_name = lines[0].product_id.name if lines else ""
        self.name = "%s%s%s" % (self.partner_id.display_name, ' - ' if
                                product_name else '', product_name)
