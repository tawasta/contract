from odoo import api, models


class ContractContract(models.Model):
    _inherit = "contract.contract"

    @api.onchange("partner_id", "contract_line_ids")
    def contract_name_onchange(self):
        lines = self.contract_line_ids
        product_name = lines[0].product_id.name if lines else ""
        partner_name = self.partner_id.display_name or ""
        self.name = "{}{}{}".format(
            partner_name, " - " if (product_name and partner_name) else "", product_name
        )
