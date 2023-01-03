from odoo import api
from odoo import models


class ContractLine(models.Model):

    _inherit = "contract.line"

    @api.onchange("product_id")
    def _onchange_product_id_update_name(self):
        for record in self:
            vals = {}

            if record.product_id and record.contract_id.show_period_on_lines:
                vals["name"] = "{} (#START# - #END#)".format(
                    self.product_id.get_product_multiline_description_sale()
                )
            record.update(vals)
